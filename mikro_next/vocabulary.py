"""The closed vocabularies the library speaks, as types rather than strings.

Every name here was a bare ``str`` somewhere else first — an axis type inferred
from a dimension name, a transformation kind dispatched on by equality, a
reduction looked up in a dict. Each of those had a runtime guard and a test
asserting the guard fired, which is the tell: the set of legal values was known
all along, just not written down anywhere a type checker could read it.

This module is a leaf on purpose. It imports nothing from ``mikro_next``, so
:mod:`~mikro_next.traits` (which :mod:`~mikro_next.api.schema` imports at module
level, and which therefore cannot import the schema back) can use it as freely
as anything downstream. That is also why the axis-type and transform-kind
vocabularies are spelled as ``Literal`` unions rather than reusing the generated
enums: the generated models all set ``use_enum_values=True``, so a field read
back off a model holds the plain value, not the enum member. A ``Literal``
describes what is actually there. The enums stay for *construction* sites, where
they are what the model wants.

Because the Literals mirror generated enums that ``turms`` regenerates, they can
drift. ``tests/test_vocabulary.py`` asserts the two stay in step.
"""

from __future__ import annotations

from typing import Final, Literal, Mapping, NamedTuple, Optional, Tuple, Union

from kanne.scalars import Unit

# --- Axis types -------------------------------------------------------------

#: The semantic kind of an axis, mirroring ``api.schema.AxisType``.
AxisTypeName = Literal[
    "SPACE",
    "TIME",
    "CHANNEL",
    "COORDINATE",
    "DISPLACEMENT",
    "MICROTIME",
    "SPECTRUM",
    "INDEX",
]

#: The bare-name convention: ``t``/``time`` -> TIME, ``c``/``channel`` ->
#: CHANNEL, everything else SPACE. Only consulted when nothing better is known.
_AXIS_TYPE_BY_NAME: Final[Mapping[str, AxisTypeName]] = {
    "t": "TIME",
    "time": "TIME",
    "c": "CHANNEL",
    "channel": "CHANNEL",
}


def default_axis_type(name: str) -> AxisTypeName:
    """The conventional axis type for a bare axis name.

    ``t``/``time`` -> TIME, ``c``/``channel`` -> CHANNEL, everything else ->
    SPACE. Pass a full input object instead of a bare name when the convention
    does not apply.
    """
    return _AXIS_TYPE_BY_NAME.get(name.lower(), "SPACE")


# RFC-5 orders a system's axes by type: time first, then the categorical and
# custom types, then space. The array's dimension order IS this order, so a
# space whose axes disagree describes a different array than the one meant.
AXIS_TYPE_ORDER: Final[Mapping[AxisTypeName, int]] = {
    "TIME": 0,
    "CHANNEL": 1,
    "MICROTIME": 1,
    "SPECTRUM": 1,
    "COORDINATE": 1,
    "DISPLACEMENT": 1,
    "INDEX": 1,
    "SPACE": 2,
}

#: Axis types a pyramid may re-bin. Halving a CHANNEL or INDEX axis would invent
#: a position halfway between two acquisitions — or two object ids — which is
#: not a thing, and the server rejects a pyramid whose categorical axes change
#: extent.
COARSENABLE_AXIS_TYPES: Final[frozenset[AxisTypeName]] = frozenset(
    {"SPACE", "TIME", "MICROTIME"}
)


def axis_type_rank(axis_type: AxisTypeName) -> int:
    """The RFC-5 group an axis sorts into.

    Unknown types sort with the categorical ones, which is where every
    non-space, non-time type belongs.
    """
    return AXIS_TYPE_ORDER.get(axis_type, 1)


# --- Transformation kinds ---------------------------------------------------

#: The kinds a caller can *build* — one per member of the ``TransformInput``
#: tagged union.
TransformKind = Literal[
    "IDENTITY",
    "SCALE",
    "TRANSLATION",
    "AFFINE",
    "ROTATION",
    "MAP_AXIS",
    "BY_DIMENSION",
    "FIELD",
    "UNMAPPABLE",
]

#: The kinds an edge can *be* once the server has resolved it. SEQUENCE is
#: deliberately outside `TransformKind`: it is produced by composing edges, so
#: it can come back from a query but can never be passed to a mutation, and a
#: single union would let `_transform_member` statically accept a value its own
#: dispatch rejects at runtime.
ResolvedTransformKind = Union[TransformKind, Literal["SEQUENCE"]]

#: The kinds with a closed-form homogeneous matrix. SEQUENCE has one too, but
#: only after a network round-trip (`resolve_matrix`); the rest have none.
MATRIX_KINDS: Final[frozenset[ResolvedTransformKind]] = frozenset(
    {"IDENTITY", "SCALE", "TRANSLATION", "AFFINE", "ROTATION", "MAP_AXIS"}
)


# --- Pyramids ---------------------------------------------------------------

#: How a pyramid level reduces the level above it, named as xarray names it.
#: `pyramid._REDUCTIONS` maps these onto the server's `ScaleMethod`.
Reduction = Literal["max", "mean", "sum", "min", "nearest"]


# --- Render graphs ----------------------------------------------------------

#: The discriminator of a `LayerNodeInput`. The generated field is an
#: unconstrained `str` because the server does not enumerate it, so this is the
#: only place the four legal spellings are written down.
LayerNodeKind = Literal["channel", "blend", "phasor", "projection"]


# --- Per-axis selections ----------------------------------------------------

#: One axis' worth of a lens selection: an ``int`` pins a single index, a
#: ``slice`` or a ``(start, stop[, step])`` tuple selects a range. ``None`` in a
#: tuple position is open-ended, exactly as in a slice.
AxisSelection = Union[
    int,
    slice,
    Tuple[Optional[int], Optional[int]],
    Tuple[Optional[int], Optional[int], Optional[int]],
]

#: The normalized form: ``(start, stop, step)``, any of which may be ``None``.
SliceBounds = Tuple[Optional[int], Optional[int], Optional[int]]


def normalize_selection(axis: str, selection: AxisSelection) -> SliceBounds:
    """One selection as ``(start, stop, step)``, or a refusal naming the axis.

    The single spelling of the selection contract, shared by
    ``DatasetTrait.lens`` (which turns it into a ``SliceInput``) and
    ``specs._selected_extent`` (which measures what it keeps). Shape only —
    anything needing the axis' extent, including bounds checking, belongs to the
    caller that knows it.

    The ``bool`` rejection is not redundant with the annotation: ``bool`` is a
    subclass of ``int``, so no type can exclude ``dataset.lens(c=True)``, and
    silently reading it as index 1 is worse than refusing it.
    """
    if isinstance(selection, bool):
        raise TypeError(f"Invalid selection for axis {axis!r}: {selection!r}")
    if isinstance(selection, int):
        return (selection, selection + 1, None)
    if isinstance(selection, slice):
        return (selection.start, selection.stop, selection.step)
    if isinstance(selection, (tuple, list)) and 2 <= len(selection) <= 3:
        start, stop = selection[0], selection[1]
        step = selection[2] if len(selection) == 3 else None
        return (start, stop, step)
    raise TypeError(
        f"Invalid selection for axis {axis!r}: {selection!r}. Pass an int, a "
        f"slice(), or a (start, stop[, step]) tuple"
    )


# --- Calibration ------------------------------------------------------------


class Calibration(NamedTuple):
    """How far one pixel step goes along an axis, and in what.

    What ``DatasetTrait.calibrate`` takes per axis. A pair rather than two
    parallel sequences because the factor is meaningless without the unit, and
    a named pair rather than a bare tuple because ``(0.2, "micrometer")`` and
    ``("micrometer", 0.2)`` are equally plausible spellings of the same thought
    and only one of them works.
    """

    factor: float
    unit: Unit


__all__ = [
    "AxisTypeName",
    "default_axis_type",
    "AXIS_TYPE_ORDER",
    "COARSENABLE_AXIS_TYPES",
    "axis_type_rank",
    "TransformKind",
    "ResolvedTransformKind",
    "MATRIX_KINDS",
    "Reduction",
    "LayerNodeKind",
    "AxisSelection",
    "SliceBounds",
    "normalize_selection",
    "Calibration",
]
