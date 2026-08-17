"""Render graphs: what a layer does with the pixels behind it.

A layer's recipe is a small tree — a blend node over one or more channel nodes,
each with its own transfer function. Written out by hand that is three levels of
nesting for the simplest possible "show this in green", so these builders cover
the shapes that actually recur::

    channel_graph(colormap=ColorMap.INFERNO, gamma=0.8)
    composite_graph([ChannelSpec(intensity_index=0, colormap=ColorMap.CYAN),
                     ChannelSpec(intensity_index=1, colormap=ColorMap.MAGENTA)])
    rgb_graph()

For the common cases you may not need a graph at all: passing
``bootstrap_scene=BootstrapSceneInput(kind=...)`` to ``create_array_dataset`` has the
server build the scene, the lens and a default layer for you. Reach for these
when you want something the default recipes do not express — a specific colormap,
a contrast window, a projection mode.
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence, Tuple, Union

from pydantic import BaseModel, ConfigDict

from mikro_next.api.schema import (
    Blending,
    ColorMap,
    LayerNodeInput,
    LayerRenderGraphInput,
    ProjectionMode,
    TransferFunctionInput,
)
from mikro_next.vocabulary import LayerNodeKind

#: A colour as the wire wants it. Three components are completed to RGBA with a
#: full alpha by `RGBAColorInputTrait`; four are passed through.
RGBAColor = Union[Tuple[int, int, int], Tuple[int, int, int, int]]


class ChannelSpec(BaseModel):
    """One channel of a composite: which positions to read, and how to colour them.

    Flat on purpose — the split between the channel node and its transfer
    function is a detail of the wire format, not something worth making a caller
    nest for. `_channel_node` sorts these fields into the two nodes.

    There is deliberately no ``categorical`` here. A transfer function maps a
    continuous intensity to a colour; mapping discrete object ids to distinct
    colours is a different thing entirely, and it lives on a label layer
    (`create_label_layer`, `LabelRenderInput`) rather than on a channel node.
    """

    # -- channel-node settings
    intensity_axis: Optional[str] = "c"
    intensity_index: int = 0
    mode: Optional[ProjectionMode] = None
    label: Optional[str] = None
    visible: Optional[bool] = None

    # -- transfer-function settings
    colormap: Optional[ColorMap] = None
    color: Optional[RGBAColor] = None
    clim_min: Optional[float] = None
    clim_max: Optional[float] = None
    gamma: Optional[float] = None
    opacity: Optional[float] = None
    invert: Optional[bool] = None

    # No `alias` on any field: a ChannelSpec is written in Python, never parsed
    # off the wire, and an alias would make type checkers reject the snake_case
    # spelling the caller actually writes.
    model_config = ConfigDict(frozen=True, extra="forbid")


def _channel_node(spec: ChannelSpec) -> LayerNodeInput:
    """One channel node, with its transfer function, from a spec."""
    kind: LayerNodeKind = "channel"
    return LayerNodeInput(
        kind=kind,
        intensity_axis=spec.intensity_axis,
        intensity_index=spec.intensity_index,
        mode=spec.mode,
        label=spec.label,
        visible=spec.visible,
        transfer=TransferFunctionInput(
            colormap=spec.colormap,
            color=spec.color,
            clim_min=spec.clim_min,
            clim_max=spec.clim_max,
            gamma=spec.gamma,
            opacity=spec.opacity,
            invert=spec.invert,
        ),
    )


def composite_graph(
    specs: Iterable[ChannelSpec],
    blending: Blending = Blending.ADDITIVE,
) -> LayerRenderGraphInput:
    """Composite several channels into one layer.

    Each `ChannelSpec` mixes channel settings (``intensity_axis``,
    ``intensity_index``, ``mode``) with transfer settings (``colormap``,
    ``color``, ``clim_min``/``clim_max``, ``gamma``, ``opacity``, ``invert``);
    they are sorted into the right nodes for you.

        composite_graph([
            ChannelSpec(intensity_index=0, colormap=ColorMap.CYAN),
            ChannelSpec(intensity_index=1, colormap=ColorMap.MAGENTA, opacity=0.7),
        ])
    """
    kind: LayerNodeKind = "blend"
    children = tuple(_channel_node(spec) for spec in specs)
    if not children:
        raise ValueError("A render graph needs at least one channel source")
    return LayerRenderGraphInput(
        root=LayerNodeInput(kind=kind, blending=blending, children=children)
    )


def channel_graph(
    colormap: Optional[ColorMap] = None,
    color: Optional[RGBAColor] = None,
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
            ChannelSpec(
                intensity_axis=intensity_axis,
                intensity_index=intensity_index,
                mode=mode,
                colormap=colormap,
                color=color,
                clim_min=clim_min,
                clim_max=clim_max,
                gamma=gamma,
                opacity=opacity,
                invert=invert,
            )
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
    colors: Tuple[RGBAColor, RGBAColor, RGBAColor] = (
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    )
    return composite_graph(
        [
            ChannelSpec(
                intensity_axis=intensity_axis,
                intensity_index=index,
                color=color,
                colormap=ColorMap.INTENSITY,
                clim_min=clim_min,
                clim_max=clim_max,
            )
            for index, color in zip(channels, colors)
        ]
    )


__all__ = [
    "ChannelSpec",
    "RGBAColor",
    "composite_graph",
    "channel_graph",
    "rgb_graph",
]
