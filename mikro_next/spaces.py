"""Constructors for the coordinate systems data gets registered into.

A physical space is not something a dataset owns. It is an ordinary coordinate
system — a node of the transformation graph, belonging to nobody — plus an edge
claiming that some data sits in it. Those are two facts, and they read best
written as two steps::

    from mikro_next import space_3d

    world = space_3d("stage", unit="micrometer")
    world.register(dataset, scale={"z": 1.0, "y": 0.2, "x": 0.2})

The space outlives every dataset registered into it and every scene composed
over it, which is exactly why it is created on its own line: a hundred tiles
acquired on one stage can share one, and `world.stage()` renders whatever has
been registered there.

These helpers cover the first step only. They exist because the axes of a
physical space are nearly always the same handful of shapes, and spelling out a
``PhysicalAxisInput`` per axis obscures the one thing that varies — the unit.
Reach for `create_space` when the shape is not one of them.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Union

from .traits import _default_axis_type

if TYPE_CHECKING:
    from datetime import datetime

    from mikro_next.api.schema import (
        CoordinateSystem,
        PhysicalAxisInput,
        RegistrationPathInput,
    )
    from mikro_next.rath import MikroNextRath

# RFC-5 orders a system's axes by type: time first, then the categorical and
# custom types, then space. The array's dimension order IS this order, so a
# space whose axes disagree describes a different array than the one meant.
_AXIS_TYPE_ORDER: Dict[str, int] = {
    "TIME": 0,
    "CHANNEL": 1,
    "MICROTIME": 1,
    "SPECTRUM": 1,
    "COORDINATE": 1,
    "DISPLACEMENT": 1,
    "INDEX": 1,
    "SPACE": 2,
}

#: How `create_space` will take its axes: name-to-unit, or the inputs themselves.
AxisSpec = Union[Mapping[str, str], Sequence["PhysicalAxisInput"]]


def _axis_type_rank(axis: "PhysicalAxisInput") -> int:
    """The RFC-5 group an axis sorts into. Unknown types sort with the
    categorical ones, which is where every non-space, non-time type belongs."""
    # `use_enum_values` means the field may hold either the enum or its value.
    kind: Any = axis.type
    return _AXIS_TYPE_ORDER.get(str(getattr(kind, "value", kind)), 1)


def _canonical_axes(axes: Sequence["PhysicalAxisInput"]) -> List["PhysicalAxisInput"]:
    """Sort axis inputs into RFC-5 order, stably.

    Stable, because order *within* a group is the caller's to state: ``(z, y, x)``
    and ``(x, y, z)`` are different spaces, and neither is more canonical.
    """
    return sorted(axes, key=_axis_type_rank)


def create_space(
    name: str,
    axes: AxisSpec,
    *,
    epoch: Optional["datetime"] = None,
    registrations: Optional[Sequence["RegistrationPathInput"]] = None,
    rath: Optional["MikroNextRath"] = None,
) -> "CoordinateSystem":
    """Create a shared coordinate system: a reference frame owned by nobody.

    Args:
        name: What to call the space — "stage", "atlas", "well A1".
        axes: Either a mapping of axis name to unit
            (``{"z": "micrometer", "y": "micrometer", "x": "micrometer"}``),
            whose axis types are inferred from the names, or a sequence of
            `PhysicalAxisInput` when a name does not imply its type. Axes are
            put into RFC-5 order (time, then categorical, then space); the order
            *within* each group is kept as given, because ``(z, y, x)`` and
            ``(x, y, z)`` are genuinely different spaces.
        epoch: The wall-clock instant a TIME axis has its origin at. A property
            of the space; leave it out and the time axis is still a perfectly
            composable relative coordinate.
        registrations: `RegistrationPathInput` entries to author in the same
            call. Usually left out — `space.register(source, ...)` afterwards
            says the same thing with the source in hand.
        rath: The mikro rath client.

    Returns:
        The created coordinate system.

    Raises:
        ValueError: If no axes are given.
    """
    from kanne.scalars import Unit

    from mikro_next.api.schema import AxisType, PhysicalAxisInput, create_coordinate_system

    axis_inputs: List[PhysicalAxisInput]
    if isinstance(axes, Mapping):
        axis_inputs = [
            PhysicalAxisInput(
                name=axis,
                type=AxisType(_default_axis_type(axis)),
                unit=Unit(unit),
            )
            for axis, unit in axes.items()
        ]
    else:
        axis_inputs = list(axes)

    if not axis_inputs:
        raise ValueError(f"A coordinate system needs at least one axis, {name!r} has none")

    kwargs: Dict[str, Any] = {}
    if epoch is not None:
        kwargs["epoch"] = epoch

    return create_coordinate_system(
        name=name,
        axes=_canonical_axes(axis_inputs),
        registrations=list(registrations) if registrations is not None else [],
        rath=rath,
        **kwargs,
    )


def space_2d(
    name: str = "space",
    *,
    unit: str = "micrometer",
    axes: Sequence[str] = ("y", "x"),
    rath: Optional["MikroNextRath"] = None,
) -> "CoordinateSystem":
    """A flat physical space: ``(y, x)``, one length unit for both axes.

        plane = space_2d("slide", unit="micrometer")
        plane.register(dataset, scale={"y": 0.2, "x": 0.2})

    Args:
        name: What to call the space.
        unit: The length unit both axes carry.
        axes: The axis names, in array order.
        rath: The mikro rath client.

    Returns:
        The created coordinate system.
    """
    return create_space(name, {axis: unit for axis in axes}, rath=rath)


def space_3d(
    name: str = "space",
    *,
    unit: str = "micrometer",
    axes: Sequence[str] = ("z", "y", "x"),
    rath: Optional["MikroNextRath"] = None,
) -> "CoordinateSystem":
    """A volumetric physical space: ``(z, y, x)``, one length unit for all three.

    The usual world to register a z-stack into. An anisotropic voxel is not a
    property of the space — every axis here is in the same unit — it is the
    per-axis scale of the edge that registers the data::

        world = space_3d("stage", unit="micrometer")
        world.register(dataset, scale={"z": 1.0, "y": 0.2, "x": 0.2})

    Args:
        name: What to call the space.
        unit: The length unit all three axes carry.
        axes: The axis names, in array order.
        rath: The mikro rath client.

    Returns:
        The created coordinate system.
    """
    return create_space(name, {axis: unit for axis in axes}, rath=rath)


def timelapse_3d(
    name: str = "space",
    *,
    unit: str = "micrometer",
    time_unit: str = "second",
    axes: Sequence[str] = ("z", "y", "x"),
    epoch: Optional["datetime"] = None,
    rath: Optional["MikroNextRath"] = None,
) -> "CoordinateSystem":
    """A volumetric space with a time axis: ``(t, z, y, x)``.

    Pass `epoch` to anchor the clock — the wall-clock instant ``t = 0`` means —
    which is what lets two acquisitions be lined up in absolute time. Without
    it the time axis is relative, and still composes perfectly well.

    Args:
        name: What to call the space.
        unit: The length unit the spatial axes carry.
        time_unit: The duration unit the time axis carries.
        axes: The spatial axis names, in array order.
        epoch: The wall-clock instant ``t = 0`` denotes.
        rath: The mikro rath client.

    Returns:
        The created coordinate system.
    """
    return create_space(
        name,
        {"t": time_unit, **{axis: unit for axis in axes}},
        epoch=epoch,
        rath=rath,
    )
