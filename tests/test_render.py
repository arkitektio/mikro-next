"""Unit tests for the layer render-graph builders.

A layer's recipe is a small tree -- a blend node over one or more channel nodes,
each with its own transfer function -- and :mod:`mikro_next.render` is what keeps
callers from hand-nesting it. What is worth pinning down offline is the split: a
flat spec mixes channel settings with transfer settings, and the builder has to
sort each field into the right node. Colour completion itself is covered by
``test_rgba_color_validation``.
"""

import pytest
from pydantic import ValidationError

from mikro_next.api.schema import Blending, ColorMap, ProjectionMode
from mikro_next.render import ChannelSpec, channel_graph, composite_graph, rgb_graph


def test_composite_graph_nests_channels_under_a_blend_node() -> None:
    graph = composite_graph(
        [
            ChannelSpec(intensity_index=0, colormap=ColorMap.CYAN),
            ChannelSpec(intensity_index=1),
        ]
    )

    assert graph.root.kind == "blend"
    assert graph.root.children is not None
    assert [child.kind for child in graph.root.children] == ["channel", "channel"]
    assert [child.intensity_index for child in graph.root.children] == [0, 1]


def test_composite_graph_sorts_a_flat_spec_into_the_right_nodes() -> None:
    """Channel fields stay on the node; transfer fields move onto its transfer
    function. A flat spec is the whole point, so the split has to be exact."""
    (node,) = composite_graph(
        [
            ChannelSpec(
                intensity_axis="c",
                intensity_index=2,
                mode=ProjectionMode.MIP,
                label="nuclei",
                visible=False,
                colormap=ColorMap.MAGMA,
                gamma=0.8,
                opacity=0.5,
                clim_min=10.0,
                clim_max=400.0,
                invert=True,
            )
        ]
    ).root.children

    assert (node.intensity_axis, node.intensity_index) == ("c", 2)
    assert (node.label, node.visible) == ("nuclei", False)
    assert node.mode == ProjectionMode.MIP.value
    assert node.transfer is not None
    assert node.transfer.colormap == ColorMap.MAGMA.value
    assert (node.transfer.gamma, node.transfer.opacity) == (0.8, 0.5)
    assert (node.transfer.clim_min, node.transfer.clim_max) == (10.0, 400.0)
    assert node.transfer.invert is True


def test_composite_graph_defaults_to_the_first_position_of_the_channel_axis() -> None:
    (node,) = composite_graph([ChannelSpec()]).root.children
    assert (node.intensity_axis, node.intensity_index) == ("c", 0)


def test_composite_graph_defaults_to_additive_blending() -> None:
    assert composite_graph([ChannelSpec()]).root.blending == Blending.ADDITIVE.value


def test_composite_graph_takes_an_explicit_blending() -> None:
    graph = composite_graph([ChannelSpec()], blending=Blending.NORMAL)
    assert graph.root.blending == Blending.NORMAL.value


def test_composite_graph_rejects_an_empty_spec_list() -> None:
    with pytest.raises(ValueError, match="at least one channel source"):
        composite_graph([])


def test_channel_spec_rejects_an_unknown_field() -> None:
    """A misspelled field would otherwise be silently dropped, and the layer
    would render without the setting the caller thought they had asked for.
    A type checker now catches this too; the model still refuses it at runtime."""
    with pytest.raises(ValidationError, match="colourmap"):
        ChannelSpec(colourmap=ColorMap.VIRIDIS)


def test_channel_spec_rejects_a_categorical_channel() -> None:
    """Mapping discrete object ids to distinct colours is a label layer's job,
    not a transfer function's -- there is no such field on a channel node."""
    with pytest.raises(ValidationError, match="categorical"):
        ChannelSpec(categorical=True)


def test_channel_graph_is_a_single_channel_composite() -> None:
    graph = channel_graph(colormap=ColorMap.INFERNO, gamma=0.8, intensity_index=1)

    assert graph.root.children is not None
    (node,) = graph.root.children
    assert node.intensity_index == 1
    assert node.transfer is not None
    assert node.transfer.colormap == ColorMap.INFERNO.value
    assert node.transfer.gamma == 0.8


def test_channel_graph_leaves_unset_transfer_settings_unset() -> None:
    """Passing nothing means "the viewer decides", not "explicitly none of it"."""
    (node,) = channel_graph().root.children
    assert node.transfer is not None
    assert node.transfer.colormap is None
    assert node.transfer.color is None
    assert node.transfer.gamma is None


def test_channel_graph_accepts_no_intensity_axis() -> None:
    """Data that is single-valued per rendered plane -- a bare z-stack, a time
    series -- has no axis to composite as separate colours."""
    (node,) = channel_graph(intensity_axis=None).root.children
    assert node.intensity_axis is None


def test_rgb_graph_composites_three_display_channels() -> None:
    graph = rgb_graph()

    assert graph.root.children is not None
    assert len(graph.root.children) == 3
    assert [node.intensity_index for node in graph.root.children] == [0, 1, 2]
    assert [node.transfer.color for node in graph.root.children] == [
        (255, 0, 0, 255),
        (0, 255, 0, 255),
        (0, 0, 255, 255),
    ]


def test_rgb_graph_defaults_to_the_full_eight_bit_range() -> None:
    """An RGB image is already display-referred, so stretching it would change
    the colours it was authored with."""
    for node in rgb_graph().root.children:
        assert (node.transfer.clim_min, node.transfer.clim_max) == (0.0, 255.0)


def test_rgb_graph_maps_explicit_channel_positions() -> None:
    graph = rgb_graph(channels=(3, 1, 0))
    assert [node.intensity_index for node in graph.root.children] == [3, 1, 0]


@pytest.mark.parametrize("channels", [(0, 1), (0, 1, 2, 3)])
def test_rgb_graph_rejects_anything_but_three_channels(channels: tuple) -> None:
    with pytest.raises(ValueError, match="exactly three channels"):
        rgb_graph(channels=channels)
