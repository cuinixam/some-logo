"""Logo generation orchestration."""

from pathlib import Path

from some_logo.core import GeometryMode, LogoOptions, generate_shapes
from some_logo.svg import generate_svg


class SomeLogo:
    """Orchestrates logo generation from text to SVG file."""

    def __init__(
        self,
        text: str,
        mode: GeometryMode = GeometryMode.SQUARE,
        add_frame: bool = False,
        add_text: bool = False,
        random_colors: bool = False,
        empty_spaces: bool = False,
        transparent_background: bool = False,
        transparent_text: bool = False,
        output: Path = Path("logo.svg"),
    ) -> None:
        options = LogoOptions(
            text=text,
            mode=mode,
            add_frame=add_frame,
            add_text=add_text,
            random_colors=random_colors,
            empty_spaces=empty_spaces,
            transparent_background=transparent_background,
            transparent_text=transparent_text,
        )
        shapes = generate_shapes(text, options)
        svg_content = generate_svg(shapes, options)
        output.write_text(svg_content, encoding="utf-8")
