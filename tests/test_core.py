"""Tests for core data structures and logic."""

import pytest

from some_logo.core import GeometryMode, LogoOptions, Shape, char_to_color, generate_shapes, random_color

_DEFAULT_OPTS = LogoOptions(text="")


@pytest.mark.parametrize(
    ("char", "expected"),
    [
        ("A", (46, 230, 65)),
        ("a", (73, 46, 230)),
        ("s", (230, 46, 175)),
    ],
)
def test_char_to_color(char: str, expected: tuple[int, int, int]) -> None:
    assert char_to_color(char) == expected


def test_generate_shapes_count() -> None:
    shapes = generate_shapes("stop", _DEFAULT_OPTS)
    assert len(shapes) == 4


def test_generate_shapes_characters() -> None:
    shapes = generate_shapes("hi", _DEFAULT_OPTS)
    assert [s.character for s in shapes] == ["h", "i"]


def test_generate_shapes_colors_match_chars() -> None:
    shapes = generate_shapes("ab", _DEFAULT_OPTS)
    assert shapes[0].color == char_to_color("a")
    assert shapes[1].color == char_to_color("b")


def test_generate_shapes_empty() -> None:
    assert generate_shapes("", _DEFAULT_OPTS) == []


def test_shape_dataclass() -> None:
    shape = Shape(character="x", color=(10, 20, 30))
    assert shape.character == "x"
    assert shape.color == (10, 20, 30)


def test_logo_options_defaults() -> None:
    opts = LogoOptions(text="hello")
    assert opts.mode == GeometryMode.SQUARE
    assert opts.add_frame is False
    assert opts.add_text is False
    assert opts.random_colors is False


def test_random_color_returns_valid_rgb() -> None:
    color = random_color()
    assert len(color) == 3
    assert all(0 <= channel <= 255 for channel in color)


def test_generate_shapes_random_mode_produces_valid_colors() -> None:
    opts = LogoOptions(text="abc", random_colors=True)
    shapes = generate_shapes("abc", opts)
    assert len(shapes) == 3
    for shape in shapes:
        assert all(0 <= channel <= 255 for channel in shape.color)


def test_generate_shapes_random_differs_from_deterministic() -> None:
    opts_random = LogoOptions(text="a", random_colors=True)
    shapes_random = generate_shapes("a", opts_random)
    deterministic_color = char_to_color("a")
    # On the vast majority of runs the random color differs from the fixed one.
    # We run several samples to avoid a flaky test on the rare collision.
    colors = {generate_shapes("a", opts_random)[0].color for _ in range(10)}
    assert len(colors) > 1 or shapes_random[0].color != deterministic_color
