"""Tests for SVG generation."""

import pytest

from some_logo.core import GeometryMode, LogoOptions, generate_shapes
from some_logo.svg import _grid_dimensions, generate_svg


@pytest.mark.parametrize(
    ("count", "expected"),
    [
        (1, (1, 1)),
        (2, (1, 2)),
        (3, (2, 2)),
        (4, (2, 2)),
        (5, (2, 3)),
        (6, (2, 3)),
        (7, (3, 3)),
        (9, (3, 3)),
    ],
)
def test_grid_dimensions(count: int, expected: tuple[int, int]) -> None:
    assert _grid_dimensions(count) == expected


def _make_options(
    text: str = "ab",
    mode: GeometryMode = GeometryMode.SQUARE,
    add_frame: bool = False,
    add_text: bool = False,
) -> LogoOptions:
    return LogoOptions(text=text, mode=mode, add_frame=add_frame, add_text=add_text)


def test_square_mode_produces_rect_elements() -> None:
    opts = _make_options(mode=GeometryMode.SQUARE)
    shapes = generate_shapes("ab", opts)
    svg = generate_svg(shapes, opts)
    assert "<rect" in svg
    assert "<circle" not in svg


def test_circle_mode_produces_circle_elements() -> None:
    opts = _make_options(mode=GeometryMode.CIRCLE)
    shapes = generate_shapes("ab", opts)
    svg = generate_svg(shapes, opts)
    assert "<circle" in svg


def test_square_with_frame_has_outer_rect() -> None:
    opts = _make_options(add_frame=True)
    shapes = generate_shapes("ab", opts)
    svg = generate_svg(shapes, opts)
    assert 'stroke="black"' in svg


def test_circle_with_frame_has_outer_circle() -> None:
    opts = _make_options(mode=GeometryMode.CIRCLE, add_frame=True)
    shapes = generate_shapes("ab", opts)
    svg = generate_svg(shapes, opts)
    assert 'stroke="black"' in svg


def test_text_overlay_includes_text_elements() -> None:
    opts = _make_options(add_text=True)
    shapes = generate_shapes("hi", opts)
    svg = generate_svg(shapes, opts)
    assert "<text" in svg
    assert "h" in svg
    assert "i" in svg


def test_no_text_overlay_excludes_text_elements() -> None:
    opts = _make_options(add_text=False)
    shapes = generate_shapes("hi", opts)
    svg = generate_svg(shapes, opts)
    assert "<text" not in svg


def test_empty_text_produces_valid_svg() -> None:
    opts = _make_options(text="", mode=GeometryMode.CIRCLE)
    shapes = generate_shapes("", opts)
    svg = generate_svg(shapes, opts)
    assert svg.startswith("<svg")


def test_svg_output_is_valid_xml_snippet() -> None:
    opts = _make_options(text="x")
    shapes = generate_shapes("x", opts)
    svg = generate_svg(shapes, opts)
    assert svg.startswith("<svg")
    assert svg.strip().endswith("</svg>")


def test_polygon_mode_produces_polygon_elements() -> None:
    opts = _make_options(mode=GeometryMode.POLYGON)
    shapes = generate_shapes("ab", opts)
    svg = generate_svg(shapes, opts)
    assert "<polygon" in svg


@pytest.mark.parametrize("mode", [GeometryMode.SQUARE, GeometryMode.CIRCLE, GeometryMode.POLYGON])
def test_shape_colors_encoded_in_svg(mode: GeometryMode) -> None:
    opts = _make_options(text="A", mode=mode)
    shapes = generate_shapes("A", opts)
    svg = generate_svg(shapes, opts)
    assert "rgb(46,230,65)" in svg
