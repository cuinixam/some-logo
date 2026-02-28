import threading
import time
import webbrowser
from importlib.resources import files
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from some_logo.core import GeometryMode, LogoOptions, generate_shapes
from some_logo.svg import generate_svg

app = FastAPI(title="Some Logo GUI")

try:
    # If installed as a package
    STATIC_DIR = files("some_logo").joinpath("static")
    if not STATIC_DIR.is_dir():
        STATIC_DIR = Path(__file__).parent / "static"
except Exception:
    STATIC_DIR = Path(__file__).parent / "static"


class GenerateRequest(BaseModel):
    """Payload for generating a logo."""

    text: str
    mode: GeometryMode = GeometryMode.SQUARE
    add_frame: bool = False
    add_text: bool = False
    random_colors: bool = False
    empty_spaces: bool = False
    transparent_background: bool = False
    transparent_text: bool = False


@app.post("/api/generate")
def api_generate(req: GenerateRequest) -> Response:
    options = LogoOptions(
        text=req.text,
        mode=req.mode,
        add_frame=req.add_frame,
        add_text=req.add_text,
        random_colors=req.random_colors,
        empty_spaces=req.empty_spaces,
        transparent_background=req.transparent_background,
        transparent_text=req.transparent_text,
    )
    shapes = generate_shapes(req.text, options)
    svg_content = generate_svg(shapes, options)

    return Response(content=svg_content, media_type="image/svg+xml")


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


def run_gui(host: str = "127.0.0.1", port: int = 8000) -> None:
    def open_browser() -> None:
        time.sleep(1.5)
        webbrowser.open(f"http://{host}:{port}")

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host=host, port=port, log_level="warning")
