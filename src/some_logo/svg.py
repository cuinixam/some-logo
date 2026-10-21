"""SVG generation for some_logo."""

import math

from some_logo.core import GeometryMode, LogoOptions, Shape

# Canvas constants
_PADDING = 20
_SHAPE_SIZE = 80
_TEXT_FONT_SIZE = 56

# The six colour bars of the real PM5544 card, at 75 % amplitude
_PM5544_COLORS = [(191, 191, 0), (0, 191, 191), (0, 191, 0), (191, 0, 191), (191, 0, 0), (0, 0, 191)]


def _rgb_to_css(color: tuple[int, int, int]) -> str:
    return f"rgb({color[0]},{color[1]},{color[2]})"


def generate_svg(shapes: list[Shape], options: LogoOptions) -> str:
    """Generate an SVG string for the given shapes and options."""
    if options.mode == GeometryMode.SQUARE:
        return _render_square_layout(shapes, options)
    if options.mode == GeometryMode.POLYGON:
        return _render_polygon_layout(shapes, options)
    if options.mode == GeometryMode.PM5544:
        return _render_pm5544_layout(shapes, options)
    return _render_circle_layout(shapes, options)


# ---------------------------------------------------------------------------
# Square mode
# ---------------------------------------------------------------------------


def _grid_dimensions(count: int) -> tuple[int, int]:
    """Return (rows, cols) for the most square-like grid that fits count shapes."""
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols) if cols else 0
    return rows, cols


def _render_square_layout(shapes: list[Shape], options: LogoOptions) -> str:
    """Render shapes as a best-fitting grid of squares."""
    count = len(shapes)
    if count == 0:
        return _svg_document(2 * _PADDING, 2 * _PADDING, [])

    rows, cols = _grid_dimensions(count)
    total_width = cols * _SHAPE_SIZE + (cols + 1) * _PADDING
    total_height = rows * _SHAPE_SIZE + (rows + 1) * _PADDING

    elements: list[str] = []

    if options.add_frame:
        elements.append(_rect(0, 0, total_width, total_height, "none", stroke="black", stroke_width=2))

    for index, shape in enumerate(shapes):
        row = index // cols
        col = index % cols
        x_pos = _PADDING + col * (_SHAPE_SIZE + _PADDING)
        y_pos = _PADDING + row * (_SHAPE_SIZE + _PADDING)

        if not shape.is_empty:
            if options.transparent_background:
                elements.append(_rect(x_pos, y_pos, _SHAPE_SIZE, _SHAPE_SIZE, fill="none", stroke=_rgb_to_css(shape.color), stroke_width=2))
            else:
                elements.append(_rect(x_pos, y_pos, _SHAPE_SIZE, _SHAPE_SIZE, fill=_rgb_to_css(shape.color)))

            if options.add_text:
                cx = x_pos + _SHAPE_SIZE // 2
                cy = y_pos + _SHAPE_SIZE // 2
                elements.append(_text(shape.character, cx, cy, options))

    return _svg_document(total_width, total_height, elements)


# ---------------------------------------------------------------------------
# Circle mode
# ---------------------------------------------------------------------------


def _render_circle_layout(shapes: list[Shape], options: LogoOptions) -> str:
    """Render shapes as inner circles distributed within a bounding circle."""
    count = len(shapes)
    if count == 0:
        return _svg_document(2 * _PADDING, 2 * _PADDING, [])

    # Determine the outer radius based on the number of inner circles.
    # Inner circle radius stays fixed; outer radius is derived from geometry.
    inner_r = _SHAPE_SIZE // 2

    outer_r: float
    if count == 1:
        outer_r = float(inner_r + _PADDING)
    else:
        # Place inner circle centres on a ring of radius `ring_r` inside the outer circle.
        # ring_r = outer_r - inner_r, and the centres must not overlap:
        # 2 * ring_r * sin(pi / count) >= 2 * inner_r
        # => ring_r >= inner_r / sin(pi / count)
        min_ring_r = inner_r / math.sin(math.pi / count)
        ring_r = min_ring_r * 1.05  # 5 % breathing room
        outer_r = ring_r + inner_r + _PADDING

    cx: float = outer_r + _PADDING
    cy: float = outer_r + _PADDING
    total_size = round(2 * (outer_r + _PADDING))

    elements: list[str] = []

    if options.add_frame:
        elements.append(_circle(cx, cy, outer_r, "none", stroke="black", stroke_width=2))

    for index, shape in enumerate(shapes):
        if count == 1:
            shape_cx = cx
            shape_cy = cy
        else:
            ring_r_val = outer_r - inner_r - _PADDING
            angle = 2 * math.pi * index / count - math.pi / 2
            shape_cx = cx + ring_r_val * math.cos(angle)
            shape_cy = cy + ring_r_val * math.sin(angle)

        if not shape.is_empty:
            if options.transparent_background:
                elements.append(_circle(shape_cx, shape_cy, inner_r, fill="none", stroke=_rgb_to_css(shape.color), stroke_width=2))
            else:
                elements.append(_circle(shape_cx, shape_cy, inner_r, fill=_rgb_to_css(shape.color)))

            if options.add_text:
                elements.append(_text(shape.character, shape_cx, shape_cy, options))

    return _svg_document(total_size, total_size, elements)


# ---------------------------------------------------------------------------
# Polygon mode
# ---------------------------------------------------------------------------


def _render_polygon_layout(shapes: list[Shape], options: LogoOptions) -> str:
    """Render shapes as triangular wedges meeting at the center of a regular polygon."""
    count = len(shapes)
    if count == 0:
        return _svg_document(2 * _PADDING, 2 * _PADDING, [])

    sides = max(count, 3)
    # Scale radius so larger polygons occupy a proportional area
    radius = max(_SHAPE_SIZE, _SHAPE_SIZE * math.sqrt(sides) * 0.4)
    total_size = 2 * radius + 2 * _PADDING
    cx = cy = total_size / 2

    elements: list[str] = []

    # Frame is the outer regular polygon outlining the entire shape
    if options.add_frame:
        pts = []
        for index in range(sides):
            a = 2 * math.pi * index / sides - math.pi / 2
            pts.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
        elements.append(_polygon(pts, "none", stroke="black", stroke_width=2))

    for index, shape in enumerate(shapes):
        a1 = 2 * math.pi * index / sides - math.pi / 2
        a2 = 2 * math.pi * (index + 1) / sides - math.pi / 2

        p1x = cx + radius * math.cos(a1)
        p1y = cy + radius * math.sin(a1)

        p2x = cx + radius * math.cos(a2)
        p2y = cy + radius * math.sin(a2)

        if not shape.is_empty:
            wedge_pts = [(cx, cy), (p1x, p1y), (p2x, p2y)]
            if options.transparent_background:
                elements.append(_polygon(wedge_pts, fill="none", stroke=_rgb_to_css(shape.color), stroke_width=2))
            else:
                elements.append(_polygon(wedge_pts, fill=_rgb_to_css(shape.color)))

            if options.add_text:
                text_x = (cx + p1x + p2x) / 3
                text_y = (cy + p1y + p2y) / 3
                elements.append(_text(shape.character, text_x, text_y, options))

    return _svg_document(total_size, total_size, elements)


# ---------------------------------------------------------------------------
# PM5544 mode
# ---------------------------------------------------------------------------


def _render_pm5544_layout(shapes: list[Shape], options: LogoOptions) -> str:
    """Render a simplified Philips PM5544 test card: colour bars, a black text box and grey steps across a circle."""
    count = len(shapes)
    if count == 0:
        return _svg_document(2 * _PADDING, 2 * _PADDING, [])

    # The minimum radius keeps the text box of short texts inside the circle
    radius = max(_SHAPE_SIZE * 1.5, count * _SHAPE_SIZE * 0.4)
    total_size = 2 * radius + 2 * _PADDING
    cx = cy = total_size / 2
    bar_width = 2 * radius / count
    # Colour bars above and grey steps below the centred text box, mirrored and of equal height
    box_height = _TEXT_FONT_SIZE + _PADDING
    band_height = radius * 0.45
    bars_top = cy - box_height / 2 - _PADDING / 2 - band_height
    steps_top = cy + box_height / 2 + _PADDING / 2

    # White grid lines on grey, with one line through the centre like the real card
    grid_step = radius / 4
    offsets = [cx + step * grid_step for step in range(-6, 7)]
    grid_path = " ".join(f"M{offset:.1f} 0V{total_size:.1f}M0 {offset:.1f}H{total_size:.1f}" for offset in offsets)

    elements: list[str] = [
        _rect(0, 0, total_size, total_size, fill="rgb(128,128,128)"),
        f'<path d="{grid_path}" stroke="white" stroke-width="2"/>',
        _circle(cx, cy, radius, fill="white"),
        f'<clipPath id="pm5544-circle">{_circle(cx, cy, radius, fill="white")}</clipPath>',
    ]

    bars: list[str] = []
    for index, shape in enumerate(shapes):
        if shape.is_empty:
            continue
        x_pos = cx - radius + index * bar_width
        bar_color = shape.color if options.random_colors else _PM5544_COLORS[index % len(_PM5544_COLORS)]
        bars.append(_band(x_pos, bars_top, bar_width, band_height, bar_color, options))
        bars.append(_band(x_pos, steps_top, bar_width, band_height, _grayscale(shape.color), options))
    elements.append(f'<g clip-path="url(#pm5544-circle)">{"".join(bars)}</g>')

    if options.add_frame:
        elements.append(_circle(cx, cy, radius, "none", stroke="black", stroke_width=2))

    if options.add_text:
        box_width = count * _TEXT_FONT_SIZE * 0.6 + _PADDING
        elements.append(_rect(cx - box_width / 2, cy - box_height / 2, box_width, box_height, fill="black"))
        elements.append(_text("".join(shape.character for shape in shapes), cx, cy, options))

    return _svg_document(total_size, total_size, elements)


def _band(x: float, y: float, width: float, height: float, color: tuple[int, int, int], options: LogoOptions) -> str:
    """With a frame every bar and step gets a black outline, also when transparent."""
    fill = "none" if options.transparent_background else _rgb_to_css(color)
    if options.add_frame:
        return _rect(x, y, width, height, fill=fill, stroke="black", stroke_width=2)
    if options.transparent_background:
        return _rect(x, y, width, height, fill=fill, stroke=_rgb_to_css(color), stroke_width=2)
    return _rect(x, y, width, height, fill=fill)


def _grayscale(color: tuple[int, int, int]) -> tuple[int, int, int]:
    """Convert to grey with the ITU-R BT.601 luma weights that PAL television uses."""
    luma = round(0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2])
    return luma, luma, luma


# ---------------------------------------------------------------------------
# SVG primitives
# ---------------------------------------------------------------------------


def _svg_document(width: float, height: float, elements: list[str]) -> str:
    body = "\n  ".join(elements)
    # Using only viewBox without fixed width/height makes the SVG responsive
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">\n  {body}\n</svg>\n'


def _rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    stroke: str = "none",
    stroke_width: int = 0,
) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def _circle(
    cx: float,
    cy: float,
    r: float,
    fill: str,
    stroke: str = "none",
    stroke_width: int = 0,
) -> str:
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def _polygon(
    points: list[tuple[float, float]],
    fill: str,
    stroke: str = "none",
    stroke_width: int = 0,
) -> str:
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{pts_str}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def _text(content: str, cx: float, cy: float, options: LogoOptions) -> str:
    fill_color = "none" if options.transparent_text else "white"
    stroke_color = "black" if not options.transparent_text else "white"
    return (
        f'<text x="{cx:.1f}" y="{cy:.1f}" '
        f'font-size="{_TEXT_FONT_SIZE}" font-family="monospace" '
        f'text-anchor="middle" dominant-baseline="central" '
        f'fill="{fill_color}" stroke="{stroke_color}" stroke-width="1">{content}</text>'
    )
