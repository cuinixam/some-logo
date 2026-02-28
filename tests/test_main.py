"""CLI tests for some_logo main.py."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from some_logo.main import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "some_logo" in result.stdout


def test_run_square_creates_svg(tmp_path: Path) -> None:
    output = tmp_path / "logo.svg"
    result = runner.invoke(app, ["run", "stop", "--output", str(output)])
    assert result.exit_code == 0
    assert output.exists()
    content = output.read_text()
    assert "<svg" in content
    assert "<rect" in content


def test_run_circle_mode(tmp_path: Path) -> None:
    output = tmp_path / "logo.svg"
    result = runner.invoke(app, ["run", "go", "--mode", "circle", "--output", str(output)])
    assert result.exit_code == 0
    content = output.read_text()
    assert "<circle" in content


def test_run_with_frame_and_text(tmp_path: Path) -> None:
    output = tmp_path / "logo.svg"
    result = runner.invoke(app, ["run", "hi", "--frame", "--text", "--output", str(output)])
    assert result.exit_code == 0
    content = output.read_text()
    assert 'stroke="black"' in content
    assert "<text" in content


def test_run_gui() -> None:
    from unittest.mock import patch

    with patch("some_logo.gui.run_gui") as mock_run:
        result = runner.invoke(app, ["gui", "--port", "8000"])
        assert result.exit_code == 0
        assert "Starting Some Logo Web GUI on http://127.0.0.1:8000" in result.stdout
        mock_run.assert_called_once_with(port=8000)


@pytest.mark.parametrize("text_input", ["a", "hello", "ABC123"])
def test_run_various_inputs(tmp_path: Path, text_input: str) -> None:
    output = tmp_path / "logo.svg"
    result = runner.invoke(app, ["run", text_input, "--output", str(output)])
    assert result.exit_code == 0
    assert output.exists()
