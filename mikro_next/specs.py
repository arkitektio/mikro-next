"""Spec types: what a lens structurally *is*, as importable Annotated aliases.

An action that convolves a z-stack does not accept "a Lens" — it accepts a
volume. These aliases say so in the signature, in the same vocabulary
``ADatasetSpec`` uses server-side::

    from mikro_next.specs import Volume, TimelapseVolume

    @register
    def deconvolve(image: Volume) -> Volume: ...

Each alias wraps :class:`~mikro_next.api.schema.Lens` in a mirrored
``Requires``/``Provides`` pair over the axis-count vocabulary below. Rekuest
keeps only the side a port can carry — ``requires`` on arguments, ``provides``
on returns — so the same alias works in both positions, and the constraints
become wiring information: a ``Volume`` argument only matches candidates whose
descriptors satisfy it, and a ``Volume`` return advertises what it produced.

The vocabulary counts axes by :class:`~mikro_next.api.schema.AxisType` rather
than naming positions (``axis_0_kind``), because axis position is not stable
across specs: canonical order puts time and channel *before* space, so the
three SPACE axes of a plain volume sit at 0–2 but at 2–4 in a TCZYX timelapse.
Counts make specs stack the way ``ADatasetSpec`` says they do — a 3D timelapse
is VOLUME, TIMESERIES and MULTICHANNEL at once::

    TimelapseVolume = Annotated[Volume, *at_least(N_TIME_AXES, 1)]

A lens never drops or reorders an axis — it only crops, steps and pins, so it
changes *extents*, and only ever downward. That splits the vocabulary into two
kinds of keys with different wiring meaning:

- **Invariant** (the ``n_*_axes`` counts): no lens over a dataset can change
  them. A mismatch filters the dataset out — it is fundamentally not that
  kind of data.
- **Adjustable** (the extents in ``ADJUSTABLE_KEYS``: ``n_channels``,
  ``n_timepoints``): a mismatch is a *conversion target*. A frontend can
  satisfy ``n_channels <= 1`` on a two-channel dataset by pinning one channel
  — and which channel is exactly the choice to render as a picker. The
  composed Lens IS the conversion: actions take ``@mikro/lens``, so passing
  the composed view converts on the fly without touching the data.

``compose`` is the reference composer: it partitions a spec's constraints into
invariant failures and required pins, and ``fit_lens`` turns choices into the
fitted lens. State specs in adjustable terms whenever a lens could fix them —
"single channel" is ``n_channels <= 1`` (pinnable), never "no channel axis"
(unfixable).

"Returns the same as the input" has two honest levels, and needs no more: the
signature promises the *class* (``def f(image: SingleChannelVolume) ->
SingleChannelVolume``), and the derivation edge records the *instance* — a
``derive_identity()`` edge says "same grid as that very input". A Provides
whose value references an argument's descriptors (parametric specs) would need
server support; until then nothing here pretends to it.

Three rules, each protecting against a silent failure:

- Aliases are plain assignments, never PEP 695 ``type`` statements. A ``type``
  alias wraps the Annotated in a ``TypeAliasType`` that rekuest's definition
  machinery does not unwrap, so every marker is dropped without an error.
- Aliases here carry no ``Description``: it is single-valued, so a base type
  that had one could never be refined ("Multiple descriptions found"). Add
  yours at the leaf: ``Annotated[Volume, Description("...")]``.
- ``LabelMask`` is provenance, not structure. Nothing structural distinguishes
  a label map from an image (``BootstrapLayerKind.LABEL`` is override-only for
  the same reason), so its key is *provided* by producers and never inferred —
  ``lens_descriptors`` deliberately omits it.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Annotated, Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union, get_args

from rekuest_next.annotations import Provides, Requires
from rekuest_next.api.schema import RequiresInput

from mikro_next.api.schema import AxisInput, Lens
from mikro_next.traits import _default_axis_type

# Descriptor keys, namespaced like the other @mikro structure identifiers.
# One vocabulary drives both sides: the aliases below constrain on these keys,
# and `lens_descriptors` computes them for a candidate lens.
N_SPACE_AXES = "@mikro/n_space_axes"
N_TIME_AXES = "@mikro/n_time_axes"
N_CHANNEL_AXES = "@mikro/n_channel_axes"
N_SPECTRUM_AXES = "@mikro/n_spectrum_axes"
N_MICROTIME_AXES = "@mikro/n_microtime_axes"
N_CHANNELS = "@mikro/n_channels"
N_TIMEPOINTS = "@mikro/n_timepoints"
VALUE_KIND = "@mikro/value_kind"

_KEY_BY_AXIS_TYPE = {
    "SPACE": N_SPACE_AXES,
    "TIME": N_TIME_AXES,
    "CHANNEL": N_CHANNEL_AXES,
    "SPECTRUM": N_SPECTRUM_AXES,
    "MICROTIME": N_MICROTIME_AXES,
}

# The adjustability contract, mirrored by frontend composers: each key measures
# the total extent along one axis type, so a lens can shrink it (pin, crop) but
# never grow it. Every key not listed here is lens-invariant.
ADJUSTABLE_KEYS: Dict[str, str] = {
    N_CHANNELS: "CHANNEL",
    N_TIMEPOINTS: "TIME",
}


def constrain(key: str, operator: str, value: Any) -> Tuple[Requires, Provides]:
    """A mirrored Requires/Provides pair for one constraint.

    Both directions carry the same statement so one alias serves argument and
    return positions; the port converter keeps the applicable side and drops
    the other. Operators are the `RequiresOperator` members ("EQUALS", "GTE",
    "LTE", "MATCHES", ...).
    """
    return (
        Requires(key=key, operator=operator, value=value),
        Provides(key=key, operator=operator, value=value),
    )


def exactly(key: str, value: Any) -> Tuple[Requires, Provides]:
    """Constrain a descriptor key to exactly a value."""
    return constrain(key, "EQUALS", value)


def at_least(key: str, value: Any) -> Tuple[Requires, Provides]:
    """Constrain a descriptor key to at least a value."""
    return constrain(key, "GTE", value)


def at_most(key: str, value: Any) -> Tuple[Requires, Provides]:
    """Constrain a descriptor key to at most a value."""
    return constrain(key, "LTE", value)


def refine(base: Any, *markers: Any) -> Any:
    """Stack more markers onto a spec type, building it dynamically.

    ``Annotated`` flattens on nesting and Requires/Provides accumulate, so a
    refined spec carries the base's constraints plus the new ones. For an
    alias you will write in signatures, prefer the literal spelling — static
    checkers reject a call result in type position but accept the literal::

        DualColorVolume = Annotated[Volume, *exactly(N_CHANNELS, 2)]

    Reach for ``refine`` when the spec is assembled programmatically (markers
    in a variable, specs built in a loop).
    """
    if not markers:
        return base
    return Annotated[base, *markers]


# --- Spatial specs: exactly one of these holds for any lens. ----------------

Scalar = Annotated[Lens, *exactly(N_SPACE_AXES, 0)]
"""No spatial extent: no SPACE axis at all."""

Profile = Annotated[Lens, *exactly(N_SPACE_AXES, 1)]
"""One spatial axis — a line profile, a depth trace."""

Image = Annotated[Lens, *exactly(N_SPACE_AXES, 2)]
"""Two spatial axes: a plane. The ordinary micrograph."""

Volume = Annotated[Lens, *exactly(N_SPACE_AXES, 3)]
"""Three spatial axes: a stack — even one whose z holds a single plane."""

Hypervolume = Annotated[Lens, *at_least(N_SPACE_AXES, 4)]
"""Four or more spatial axes."""

# --- Presence modifiers: any subset may hold alongside a spatial spec. ------

Timeseries = Annotated[Lens, *at_least(N_TIME_AXES, 1)]
"""Carries a TIME axis. Presence only: a single-frame time axis counts."""

Multichannel = Annotated[Lens, *at_least(N_CHANNEL_AXES, 1)]
"""Carries a CHANNEL axis. Presence only: a one-channel axis counts."""

Spectral = Annotated[Lens, *at_least(N_SPECTRUM_AXES, 1)]
"""Carries a SPECTRUM axis: a spectrally resolved acquisition."""

Flim = Annotated[Lens, *at_least(N_MICROTIME_AXES, 1)]
"""Carries a MICROTIME axis: fluorescence-lifetime arrival-time bins."""

Still = Annotated[Lens, *at_most(N_TIMEPOINTS, 1)]
"""At most one timepoint of data. Extent-based on purpose: a timelapse
satisfies it after a composer pins a timepoint — which timepoint is the
frontend's slider."""

SingleChannel = Annotated[Lens, *at_most(N_CHANNELS, 1)]
"""At most one channel's worth of data — no channel axis, or one pinned to a
single position. Extent-based on purpose: a multichannel dataset satisfies it
after a composer pins a channel — which channel is the frontend's picker.
Action code must tolerate a surviving size-1 channel axis (squeeze it)."""

# --- Common stacks. ---------------------------------------------------------

TimelapseImage = Annotated[Image, *at_least(N_TIME_AXES, 1)]
"""A plane over time."""

TimelapseVolume = Annotated[Volume, *at_least(N_TIME_AXES, 1)]
"""A stack over time."""

MultichannelImage = Annotated[Image, *at_least(N_CHANNEL_AXES, 1)]
"""A plane with a channel axis."""

MultichannelVolume = Annotated[Volume, *at_least(N_CHANNEL_AXES, 1)]
"""A stack with a channel axis."""

SingleChannelImage = Annotated[Image, *at_most(N_CHANNELS, 1)]
"""A plane with at most one channel's worth of data."""

SingleChannelVolume = Annotated[Volume, *at_most(N_CHANNELS, 1)]
"""A stack with at most one channel's worth of data — "a 3D image with one
channel". Composable: any multichannel volume fits after pinning a channel."""

RGBImage = Annotated[Image, *exactly(N_CHANNEL_AXES, 1), *exactly(N_CHANNELS, 3)]
"""A plane whose one channel axis has exactly three positions — a photograph,
a brightfield slide. The same inference rule as ``BootstrapLayerKind.RGB``."""

LabelMask = Annotated[Lens, *exactly(VALUE_KIND, "categorical")]
"""A lens whose values are object ids, not intensities. Never structurally
inferred: only a producer that *made* labels provides this, and only an action
that requires it will be offered them."""


# --- The candidate side: the same vocabulary, computed from a lens. ---------


Candidate = Union[Lens, Any]
"""Anything with ``axis_names``, ``shape`` and a typed system — a Lens
(``coordinate_system``) or an ADataset (``intrinsic_system``)."""


def _axis_table(candidate: Candidate) -> Tuple[Tuple[str, str, int], ...]:
    """``(name, axis_type, extent)`` per axis, in array order.

    Types come from the candidate's coordinate system when it was fetched with
    one; otherwise the bare-name convention (t/time -> TIME, c/channel ->
    CHANNEL, else SPACE).
    """
    names = tuple(candidate.axis_names)
    shape = tuple(candidate.shape)
    system = getattr(candidate, "coordinate_system", None) or getattr(
        candidate, "intrinsic_system", None
    )
    if system is not None:
        axes = sorted(system.axes, key=lambda axis: axis.order)
        types = tuple(str(getattr(axis.type, "value", axis.type)) for axis in axes)
    else:
        types = tuple(_default_axis_type(name) for name in names)
    return tuple(zip(names, types, shape))


def axis_types(candidate: Candidate) -> Tuple[str, ...]:
    """Per-axis semantic types in array order, as AxisType value strings."""
    return tuple(axis_type for _, axis_type, _ in _axis_table(candidate))


def lens_descriptors(candidate: Candidate) -> Dict[str, Any]:
    """The descriptor key/value pairs a lens (or dataset) carries as a match
    candidate.

    Emits every count key of the vocabulary (zero included — `Still` and
    `SingleChannel` match on absence) plus the adjustable extent keys
    (``N_CHANNELS``, ``N_TIMEPOINTS``: total extent across axes of that type).
    ``VALUE_KIND`` is deliberately absent: it is provenance, carried only by a
    producer's ``Provides``.
    """
    table = _axis_table(candidate)
    counts = Counter(axis_type for _, axis_type, _ in table)
    descriptors: Dict[str, Any] = {
        key: counts.get(axis_type, 0) for axis_type, key in _KEY_BY_AXIS_TYPE.items()
    }
    for key, wanted in ADJUSTABLE_KEYS.items():
        descriptors[key] = sum(
            extent for _, axis_type, extent in table if axis_type == wanted
        )
    return descriptors


def axes_of_type(lens: Lens, axis_type: Any) -> Tuple[str, ...]:
    """The names of the lens' axes of one AxisType, in array order.

    The runtime counterpart of the spec vocabulary: a function typed over
    ``TimelapseVolume`` should reduce over ``axes_of_type(movie, AxisType.TIME)``
    rather than hard-coding ``"t"`` — the spec guarantees the axis exists, not
    what it is called.
    """
    wanted = str(getattr(axis_type, "value", axis_type))
    return tuple(
        name for name, found in zip(lens.axis_names, axis_types(lens)) if found == wanted
    )


def carried_axes(lens: Lens, dims: Sequence[str]) -> List[AxisInput]:
    """AxisInput for a derived array's dims, types carried from the source lens.

    For ``create_a_dataset(axes=...)`` on a dataset computed from this lens:
    an axis that survived the computation keeps the semantic type it had at
    the source instead of being re-guessed from its name, so the derived
    dataset's descriptors — and with them the action's Provides — stay true
    even for unconventionally named axes. A genuinely new dim falls back to
    the bare-name convention.
    """
    types = dict(zip(lens.axis_names, axis_types(lens)))
    return [
        AxisInput(name=dim, type=types.get(dim, _default_axis_type(dim)))
        for dim in dims
    ]


# --- The fulfilment side: guarding a Provides before returning. -------------


class SpecMismatch(Exception):
    """A lens does not fulfil the spec it was about to be returned as."""


def spec_constraints(spec: Any) -> Tuple[RequiresInput, ...]:
    """The constraints a spec type carries.

    Reads the Requires side of the mirrored pairs; since every pair states the
    same thing in both directions, this is also exactly what the spec's
    Provides promise.
    """
    args = get_args(spec)
    return tuple(marker for marker in args[1:] if isinstance(marker, RequiresInput))


def _holds(operator: str, actual: Any, expected: Any, present: bool) -> bool:
    """Evaluate one constraint operator against a descriptor value."""
    if operator == "EXISTS":
        return present
    if not present:
        return False
    if operator == "EQUALS":
        return bool(actual == expected)
    if operator == "NOT_EQUALS":
        return bool(actual != expected)
    if operator == "GTE":
        return bool(actual >= expected)
    if operator == "LTE":
        return bool(actual <= expected)
    if operator == "IN":
        return actual in expected
    if operator == "NOT_IN":
        return actual not in expected
    if operator == "CONTAINS":
        return expected in actual
    if operator == "MATCHES":
        return re.fullmatch(str(expected), str(actual)) is not None
    raise ValueError(f"Unknown constraint operator {operator!r}")


def unfulfilled(
    lens: Lens, spec: Any, declares: Optional[Mapping[str, Any]] = None
) -> Tuple[str, ...]:
    """Every constraint of `spec` this lens does not satisfy, human-readable.

    Structural keys are computed via `lens_descriptors`; provenance keys
    (``VALUE_KIND``) cannot be computed and must be stated via `declares` —
    an absent key fails its constraint rather than being skipped.
    """
    descriptors = lens_descriptors(lens)
    if declares:
        descriptors.update(declares)
    failures: List[str] = []
    for constraint in spec_constraints(spec):
        operator = str(getattr(constraint.operator, "value", constraint.operator))
        present = constraint.key in descriptors
        actual = descriptors.get(constraint.key)
        if not _holds(operator, actual, constraint.value, present):
            failures.append(_describe(constraint, operator, actual, present))
    return tuple(failures)


def _describe(constraint: RequiresInput, operator: str, actual: Any, present: bool) -> str:
    """One unsatisfied constraint, human-readable."""
    detail = f"actual {actual!r}" if present else "key absent — declare it if it is provenance"
    return f"{constraint.key} {operator} {constraint.value!r} ({detail})"


def fulfills(
    lens: Lens, spec: Any, declares: Optional[Mapping[str, Any]] = None
) -> bool:
    """Whether a lens satisfies every constraint of a spec."""
    return not unfulfilled(lens, spec, declares)


def ensure(lens: Lens, spec: Any, declares: Optional[Mapping[str, Any]] = None) -> Lens:
    """Assert a lens fulfils a spec, then return it — the produce-side guard.

    A Provides is a promise the definition makes statically; nothing checks the
    value an implementation actually returns. Returning through ``ensure``
    closes that gap::

        return ensure(result.lens(), Volume)
        return ensure(result.lens(), LabelMask, declares={VALUE_KIND: "categorical"})

    `declares` states provenance keys the producer vouches for but structure
    cannot show.
    """
    failures = unfulfilled(lens, spec, declares)
    if failures:
        raise SpecMismatch(
            "Lens does not fulfil the promised spec: " + "; ".join(failures)
        )
    return lens


# --- The composer: fitting a dataset to a spec by lensing. ------------------


@dataclass(frozen=True)
class Pin:
    """One adjustable constraint a lens must fix, and its degrees of freedom.

    The frontend affordance follows from ``axis_type``: CHANNEL -> picker,
    TIME -> slider. ``axes`` are the candidate axes (name, current extent);
    the choice is which indices of them to keep so their total extent meets
    ``target`` under ``operator``.
    """

    key: str
    axis_type: str
    axes: Tuple[Tuple[str, int], ...]
    operator: str
    target: int


@dataclass(frozen=True)
class CompositionPlan:
    """What it takes for a candidate to fit a spec through a lens.

    ``failures`` are invariant (or ungrowable) mismatches — nonempty means no
    lens over this candidate can ever fit; filter it out. ``pins`` are the
    adjustable fixes, each one a choice to offer the user.
    """

    failures: Tuple[str, ...]
    pins: Tuple[Pin, ...]

    @property
    def satisfiable(self) -> bool:
        """Whether some lens over the candidate fits the spec."""
        return not self.failures

    @property
    def already_fits(self) -> bool:
        """Whether the candidate fits as-is, no adjustment needed."""
        return not self.failures and not self.pins


def compose(
    candidate: Candidate, spec: Any, declares: Optional[Mapping[str, Any]] = None
) -> CompositionPlan:
    """Plan how a dataset (or lens) could fit a spec — the reference composer.

    Pure and server-free: the same algorithm a frontend runs to decide, for a
    dropped dataset and a port's requires, whether to filter it out, pass it
    through, or offer pickers. A constraint that fails is a `Pin` when its key
    is in ``ADJUSTABLE_KEYS``, its operator is EQUALS/LTE, and the target is
    reachable by shrinking (each axis keeps at least one position); anything
    else that fails is a hard failure — extents never grow, axes never vanish.
    """
    table = _axis_table(candidate)
    descriptors = lens_descriptors(candidate)
    if declares:
        descriptors.update(declares)

    failures: List[str] = []
    pins: List[Pin] = []
    for constraint in spec_constraints(spec):
        operator = str(getattr(constraint.operator, "value", constraint.operator))
        present = constraint.key in descriptors
        actual = descriptors.get(constraint.key)
        if _holds(operator, actual, constraint.value, present):
            continue
        axis_type = ADJUSTABLE_KEYS.get(constraint.key)
        axes = tuple(
            (name, extent) for name, found, extent in table if found == axis_type
        )
        adjustable = (
            axis_type is not None
            and operator in ("EQUALS", "LTE")
            and isinstance(actual, int)
            and isinstance(constraint.value, int)
            and actual > constraint.value >= len(axes)
        )
        if adjustable:
            pins.append(
                Pin(
                    key=constraint.key,
                    axis_type=axis_type,
                    axes=axes,
                    operator=operator,
                    target=constraint.value,
                )
            )
        else:
            failures.append(_describe(constraint, operator, actual, present))
    return CompositionPlan(failures=tuple(failures), pins=tuple(pins))


def _selected_extent(choice: Any, extent: int, axis: str) -> int:
    """The extent an axis keeps under a selection, mirroring DatasetTrait.lens."""
    if isinstance(choice, bool):
        raise TypeError(f"Invalid selection for axis {axis!r}: {choice!r}")
    if isinstance(choice, int):
        if not 0 <= choice < extent:
            raise ValueError(f"Index {choice} out of range for axis {axis!r} (extent {extent})")
        return 1
    if isinstance(choice, slice):
        return len(range(*choice.indices(extent)))
    if isinstance(choice, (tuple, list)) and 2 <= len(choice) <= 3:
        start, stop = choice[0], choice[1]
        step = choice[2] if len(choice) == 3 else 1
        return len(range(start, stop, step or 1))
    raise TypeError(
        f"Invalid selection for axis {axis!r}: {choice!r}. Pass an int, a "
        f"slice(), or a (start, stop[, step]) tuple"
    )


def selections_for(plan: CompositionPlan, **choices: Any) -> Dict[str, Any]:
    """Resolve a plan's pins into per-axis selections for ``dataset.lens(...)``.

    Each choice keyword names an axis of a pin (``c=1`` pins channel 1). Every
    pin must end up satisfied by the choices; leftover choices on axes no pin
    asked about are rejected — they would silently change the data.
    """
    if plan.failures:
        raise SpecMismatch("Plan is unsatisfiable: " + "; ".join(plan.failures))
    remaining = dict(choices)
    selections: Dict[str, Any] = {}
    for pin in plan.pins:
        names = [name for name, _ in pin.axes]
        picked = {name: remaining.pop(name) for name in names if name in remaining}
        if not picked:
            raise ValueError(
                f"{pin.key} must be reduced to {pin.operator} {pin.target}: "
                f"pass a selection for one of the {pin.axis_type} axes {names}"
            )
        achieved = sum(
            _selected_extent(picked[name], extent, name) if name in picked else extent
            for name, extent in pin.axes
        )
        fits = achieved == pin.target if pin.operator == "EQUALS" else achieved <= pin.target
        if not fits:
            raise ValueError(
                f"Choices leave {pin.key} at {achieved}, need {pin.operator} {pin.target}"
            )
        selections.update(picked)
    if remaining:
        raise ValueError(
            f"Choices for axes no pin asked about: {sorted(remaining)} — "
            f"a spec-fitting lens must not silently select beyond the plan"
        )
    return selections


def fit_lens(
    dataset: Any,
    spec: Any,
    declares: Optional[Mapping[str, Any]] = None,
    **choices: Any,
) -> Lens:
    """Compose a lens over a dataset that fits a spec — the conversion itself.

    ``fit_lens(ds, SingleChannelVolume, c=1)`` plans, validates the choices,
    creates the lens via ``dataset.lens(...)`` and re-checks the result::

        lens = fit_lens(timelapse, SingleChannelVolume, c=0)
    """
    plan = compose(dataset, spec, declares)
    if not plan.satisfiable:
        raise SpecMismatch(
            "No lens over this dataset fits the spec: " + "; ".join(plan.failures)
        )
    selections = selections_for(plan, **choices)
    lens = dataset.lens(**selections)
    return ensure(lens, spec, declares)


__all__ = [
    "N_SPACE_AXES",
    "N_TIME_AXES",
    "N_CHANNEL_AXES",
    "N_SPECTRUM_AXES",
    "N_MICROTIME_AXES",
    "N_CHANNELS",
    "N_TIMEPOINTS",
    "VALUE_KIND",
    "ADJUSTABLE_KEYS",
    "constrain",
    "exactly",
    "at_least",
    "at_most",
    "refine",
    "Scalar",
    "Profile",
    "Image",
    "Volume",
    "Hypervolume",
    "Timeseries",
    "Multichannel",
    "Spectral",
    "Flim",
    "Still",
    "SingleChannel",
    "TimelapseImage",
    "TimelapseVolume",
    "MultichannelImage",
    "MultichannelVolume",
    "SingleChannelImage",
    "SingleChannelVolume",
    "RGBImage",
    "LabelMask",
    "axis_types",
    "lens_descriptors",
    "axes_of_type",
    "carried_axes",
    "SpecMismatch",
    "spec_constraints",
    "unfulfilled",
    "fulfills",
    "ensure",
    "Pin",
    "CompositionPlan",
    "compose",
    "selections_for",
    "fit_lens",
]
