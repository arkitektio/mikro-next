"""Render graphs: what a layer does with the pixels behind it.

A layer's recipe is a small tree — a blend node over one or more channel nodes,
each with its own transfer function. Written out by hand that is three levels of
nesting for the simplest possible "show this in green", so these builders cover
the shapes that actually recur::

    channel_graph(colormap=ColorMap.INFERNO, gamma=0.8)
    composite_graph([{"intensity_index": 0, "colormap": ColorMap.CYAN},
                     {"intensity_index": 1, "colormap": ColorMap.MAGENTA}])
    rgb_graph()

For the common cases you may not need a graph at all: passing
``bootstrap_scene=BootstrapSceneInput(kind=...)`` to ``create_a_dataset`` has the
server build the scene, the lens and a default layer for you. Reach for these
when you want something the default recipes do not express — a specific colormap,
a contrast window, a projection mode.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional, Sequence, Tuple

from mikro_next.api.schema import (
    Blending,
    ColorMap,
    LayerNodeInput,
    LayerRenderGraphInput,
    ProjectionMode,
    TransferFunctionInput,
)

# The transfer-function keys `composite_graph` accepts in a channel spec;
# everything else in a spec belongs to the channel node itself.
#
# There is deliberately no `categorical` here. A transfer function maps a
# continuous intensity to a colour; mapping discrete object ids to distinct
# colours is a different thing entirely, and it lives on a label layer
# (`create_label_layer`, `LabelRenderInput`) rather than on a channel node.
_TRANSFER_KEYS = (
    "colormap",
    "color",
    "clim_min",
    "clim_max",
    "gamma",
    "opacity",
    "invert",
)

_CHANNEL_KEYS = ("intensity_axis", "intensity_index", "mode", "label", "visible")


def _channel_node(spec: Mapping[str, Any]) -> LayerNodeInput:
    """One channel node from a flat spec of channel + transfer settings."""
    unknown = set(spec) - set(_TRANSFER_KEYS) - set(_CHANNEL_KEYS)
    if unknown:
        raise ValueError(
            f"Unknown channel spec keys {sorted(unknown)}. Channel keys are "
            f"{list(_CHANNEL_KEYS)}; transfer keys are {list(_TRANSFER_KEYS)}."
        )
    return LayerNodeInput(
        kind="channel",
        intensity_axis=spec.get("intensity_axis", "c"),
        intensity_index=spec.get("intensity_index", 0),
        mode=spec.get("mode"),
        label=spec.get("label"),
        visible=spec.get("visible"),
        transfer=TransferFunctionInput(
            **{key: spec[key] for key in _TRANSFER_KEYS if key in spec}
        ),
    )


def composite_graph(
    specs: Iterable[Mapping[str, Any]],
    blending: Blending = Blending.ADDITIVE,
) -> LayerRenderGraphInput:
    """Composite several channels into one layer.

    Each spec is a flat mapping mixing channel settings (``intensity_axis``,
    ``intensity_index``, ``mode``) with transfer settings (``colormap``,
    ``color``, ``clim_min``/``clim_max``, ``gamma``, ``opacity``, ``invert``);
    they are sorted into the right nodes for you.

        composite_graph([
            {"intensity_index": 0, "colormap": ColorMap.CYAN},
            {"intensity_index": 1, "colormap": ColorMap.MAGENTA, "opacity": 0.7},
        ])
    """
    children = tuple(_channel_node(spec) for spec in specs)
    if not children:
        raise ValueError("A render graph needs at least one channel source")
    return LayerRenderGraphInput(
        root=LayerNodeInput(kind="blend", blending=blending, children=children)
    )


def channel_graph(
    colormap: Optional[ColorMap] = None,
    color: Optional[Tuple[int, int, int]] = None,
    intensity_axis: Optional[str] = "c",
    intensity_index: int = 0,
    clim_min: Optional[float] = None,
    clim_max: Optional[float] = None,
    gamma: Optional[float] = None,
    opacity: Optional[float] = None,
    invert: Optional[bool] = None,
    mode: Optional[ProjectionMode] = None,
    blending: Blending = Blending.ADDITIVE,
) -> LayerRenderGraphInput:
    """A single channel with a fully specified transfer function.

    ``intensity_axis`` names the axis whose positions are composited *together*
    as separate colour channels, so it has to be a CHANNEL axis — the server
    rejects a TIME or SPACE axis outright, and for good reason: pointing it at
    ``t`` stacks every frame of a timelapse on top of each other at once and
    consumes the axis the time slider would have walked.

    Pass ``intensity_axis=None`` for data that is single-valued per rendered
    plane — a bare z-stack, a time series. The projection ``mode`` and the time
    slider already know which axis they walk.
    """
    return composite_graph(
        [
            {
                "intensity_axis": intensity_axis,
                "intensity_index": intensity_index,
                "mode": mode,
                "colormap": colormap,
                "color": color,
                "clim_min": clim_min,
                "clim_max": clim_max,
                "gamma": gamma,
                "opacity": opacity,
                "invert": invert,
            }
        ],
        blending=blending,
    )


def rgb_graph(
    clim_min: float = 0.0,
    clim_max: float = 255.0,
    intensity_axis: str = "c",
    channels: Sequence[int] = (0, 1, 2),
) -> LayerRenderGraphInput:
    """Three channels composited as red, green and blue — a photograph, a
    brightfield slide, anything already in display colour.

    The contrast window defaults to a full 8-bit range rather than being read
    off the data: an RGB image is already display-referred, so stretching it
    would change the colours it was authored with.
    """
    if len(channels) != 3:
        raise ValueError(f"An RGB graph needs exactly three channels, got {len(channels)}")
    colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255))
    return composite_graph(
        [
            {
                "intensity_axis": intensity_axis,
                "intensity_index": index,
                "color": color,
                "colormap": ColorMap.INTENSITY,
                "clim_min": clim_min,
                "clim_max": clim_max,
            }
            for index, color in zip(channels, colors)
        ]
    )
