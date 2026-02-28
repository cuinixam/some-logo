"""Core data structures and logic for some_logo generation."""

import colorsys
import secrets
from dataclasses import dataclass
from enum import Enum

import grapheme

_ASCII_MIN = 32  # space
_ASCII_MAX = 126  # tilde (~)
_ASCII_RANGE = _ASCII_MAX - _ASCII_MIN


class GeometryMode(str, Enum):
    """The geometric shape used to represent each character."""

    SQUARE = "square"
    CIRCLE = "circle"
    POLYGON = "polygon"


@dataclass
class LogoOptions:
    """Options controlling logo generation."""

    text: str
    mode: GeometryMode = GeometryMode.SQUARE
    add_frame: bool = False
    add_text: bool = False
    random_colors: bool = False
    empty_spaces: bool = False
    transparent_background: bool = False
    transparent_text: bool = False


@dataclass
class Shape:
    """A single colored shape derived from a character."""

    character: str
    color: tuple[int, int, int]
    is_empty: bool = False


def char_to_color(char: str) -> tuple[int, int, int]:
    """
    Convert a character or grapheme cluster to a visually distinct RGB color.

    The first character's ASCII value is normalised against the printable ASCII range
    (32-126) and mapped to a hue angle covering the full color wheel, so that
    every character receives a unique, saturated color with maximum spread.
    Values outside the printable range are clamped to [0.0, 1.0].
    """
    first_code_point = ord(char[0]) if char else 0
    hue = max(0.0, min(1.0, (first_code_point - _ASCII_MIN) / _ASCII_RANGE))
    red_f, green_f, blue_f = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
    return round(red_f * 255), round(green_f * 255), round(blue_f * 255)


def random_color() -> tuple[int, int, int]:
    """Generate a random vivid RGB color using a cryptographically random hue."""
    hue = secrets.randbelow(1000) / 1000
    red_f, green_f, blue_f = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
    return round(red_f * 255), round(green_f * 255), round(blue_f * 255)


def generate_shapes(text: str, options: LogoOptions) -> list[Shape]:
    """Generate a list of shapes from the input text using grapheme clusters for proper emoji support."""
    shapes = []
    for char in grapheme.graphemes(text):
        if char == " " and options.empty_spaces:
            shapes.append(Shape(character=char, color=(0, 0, 0), is_empty=True))
        else:
            shapes.append(
                Shape(
                    character=char,
                    color=random_color() if options.random_colors else char_to_color(char),
                    is_empty=False,
                )
            )
    return shapes
