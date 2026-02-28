# Some Logo

<p align="center">
  <a href="https://github.com/cuinixam/some-logo/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/cuinixam/some-logo/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://codecov.io/gh/cuinixam/some-logo">
    <img src="https://img.shields.io/codecov/c/github/cuinixam/some-logo.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/cuinixam/pypeline">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cuinixam/pypeline/refs/heads/main/assets/badge/v0.json" alt="pypeline">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/some-logo/">
    <img src="https://img.shields.io/pypi/v/some-logo.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/some-logo.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/some-logo.svg?style=flat-square" alt="License">
</p>

---

**Source Code**: <a href="https://github.com/cuinixam/some-logo" target="_blank">https://github.com/cuinixam/some-logo </a>

---

Generate some logo from text when I am too lazy to design a logo myself.

## Usage

The easiest way to run the tool without installing it globally is using [`uvx`](https://docs.astral.sh/uv/guides/tools/):

### Web GUI

To launch the interactive web GUI:

```bash
uvx some-logo gui
```

Or with a specific port:

```bash
uvx some-logo gui --port 8080
```

Then navigate to `http://localhost:8000` (or your chosen port) in your browser.

*(If you have installed the package via `pip install` or `uv tool install`, or you are in a development virtual environment, you can run the command directly using `some_logo gui`  instead of `uvx some-logo gui`.)*

### Command Line Interface (CLI)

To generate an SVG logo directly from the CLI:

```bash
uvx some-logo run "MY TEXT"
```

*(Similarly, you can use `some_logo run "MY TEXT"` if the package is already installed).*

#### CLI Options

- `--mode [square|circle|polygon]`: Geometry mode (default: `square`)
- `--frame / --no-frame`: Add an outer frame around the shapes
- `--text / --no-text`: Render each character inside its shape
- `--random / --no-random`: Use random colors instead of ASCII-derived ones
- `--empty-spaces / --no-empty-spaces`: Render spaces as invisible placeholders
- `--transparent / --no-transparent`: Make shape backgrounds transparent with colored outlines
- `--transparent-text / --no-transparent-text`: Make text transparent with a white outline
- `-o, --output PATH`: Output SVG file path (default: `logo.svg`)

Example:

```bash
uvx some-logo run "LOGO" --mode polygon --text --random -o my_logo.svg
```

## Credits

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
