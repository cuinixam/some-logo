"""CLI entry point for some_logo package manager."""

import sys
from pathlib import Path
from typing import Annotated

import typer
from py_app_dev.core.exceptions import UserNotificationException
from py_app_dev.core.logging import logger, setup_logger, time_it

from some_logo import __version__
from some_logo.core import GeometryMode
from some_logo.some_logo import SomeLogo

package_name = "some_logo"


app = typer.Typer(
    name=package_name,
    help="Generate some logo from text if you are too lazy to design a logo yourself.",
    no_args_is_help=True,
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def version(
    version: Annotated[bool, typer.Option("--version", "-v", is_eager=True, help="Show version and exit.")] = False,
) -> None:
    if version:
        typer.echo(f"{package_name} {__version__}")
        raise typer.Exit()


@app.command(help="Generate an SVG logo from TEXT.")
@time_it("run")
def run(
    text: Annotated[str, typer.Argument(help="Input text to generate the logo from.")],
    mode: Annotated[GeometryMode, typer.Option("--mode", "-m", help="Geometry mode: square or circle.")] = GeometryMode.SQUARE,
    frame: Annotated[bool, typer.Option("--frame/--no-frame", help="Add an outer frame around the shapes.")] = False,
    overlay_text: Annotated[bool, typer.Option("--text/--no-text", help="Render each character inside its shape.")] = False,
    random_colors: Annotated[bool, typer.Option("--random/--no-random", help="Use random colors instead of ASCII-derived ones.")] = False,
    empty_spaces: Annotated[bool, typer.Option("--empty-spaces/--no-empty-spaces", help="Render spaces as invisible placeholders.")] = False,
    transparent_background: Annotated[bool, typer.Option("--transparent/--no-transparent", help="Make shape backgrounds transparent with colored outlines.")] = False,
    transparent_text: Annotated[bool, typer.Option("--transparent-text/--no-transparent-text", help="Make text transparent with a white outline.")] = False,
    output: Annotated[Path, typer.Option("--output", "-o", help="Output SVG file path.")] = Path("logo.svg"),
) -> None:
    SomeLogo(
        text=text,
        mode=mode,
        add_frame=frame,
        add_text=overlay_text,
        random_colors=random_colors,
        empty_spaces=empty_spaces,
        transparent_background=transparent_background,
        transparent_text=transparent_text,
        output=output,
    )
    logger.info(f"Logo written to {output}")


@app.command(help="Launch the Web GUI.")
def gui(
    port: Annotated[int, typer.Option("--port", "-p", help="Port to run the GUI on.")] = 8000,
) -> None:
    from some_logo.gui import run_gui

    typer.echo(f"Starting Some Logo Web GUI on http://127.0.0.1:{port}")
    run_gui(port=port)


def main() -> int:
    try:
        setup_logger()
        app()
        return 0
    except UserNotificationException as e:
        logger.error(f"{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
