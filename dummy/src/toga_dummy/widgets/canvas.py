from pathlib import Path

import toga_dummy
from toga.fonts import SYSTEM, SYSTEM_DEFAULT_FONT_SIZE

from .base import Widget


class Canvas(Widget):
    def create(self):
        self._action("create Canvas")

    def redraw(self):
        self._action("redraw")
        self.draw_instructions = []
        self.interface.context._draw(self, draw_instructions=self.draw_instructions)

    # Context management
    def push_context(self, draw_instructions, **kwargs):
        draw_instructions.append(("push context", kwargs))

    def pop_context(self, draw_instructions, **kwargs):
        draw_instructions.append(("pop context", kwargs))

    # Basic paths
    def begin_path(self, draw_instructions, **kwargs):
        draw_instructions.append(("begin path", kwargs))

    def close_path(self, draw_instructions, **kwargs):
        draw_instructions.append(("close path", kwargs))

    def move_to(self, x, y, draw_instructions, **kwargs):
        draw_instructions.append(("move to", dict(**{"x": x, "y": y}, **kwargs)))

    def line_to(self, x, y, draw_instructions, **kwargs):
        draw_instructions.append(("line to", dict(**{"x": x, "y": y}, **kwargs)))

    # Basic shapes
    def bezier_curve_to(
        self,
        cp1x,
        cp1y,
        cp2x,
        cp2y,
        x,
        y,
        draw_instructions,
        *args,
        **kwargs,
    ):
        draw_instructions.append(
            (
                "bezier curve to",
                dict(
                    **{
                        "cp1x": cp1x,
                        "cp1y": cp1y,
                        "cp2x": cp2x,
                        "cp2y": cp2y,
                        "x": x,
                        "y": y,
                    },
                    **kwargs,
                ),
            )
        )

    def quadratic_curve_to(self, cpx, cpy, x, y, draw_instructions, **kwargs):
        draw_instructions.append(
            (
                "quadratic curve to",
                dict(
                    **{
                        "cpx": cpx,
                        "cpy": cpy,
                        "x": x,
                        "y": y,
                    },
                    **kwargs,
                ),
            )
        )

    def arc(
        self,
        x,
        y,
        radius,
        startangle,
        endangle,
        anticlockwise,
        draw_instructions,
        *args,
        **kwargs,
    ):
        draw_instructions.append(
            (
                "arc",
                dict(
                    **{
                        "x": x,
                        "y": y,
                        "radius": radius,
                        "startangle": startangle,
                        "endangle": endangle,
                        "anticlockwise": anticlockwise,
                    },
                    **kwargs,
                ),
            )
        )

    def ellipse(
        self,
        x,
        y,
        radiusx,
        radiusy,
        rotation,
        startangle,
        endangle,
        anticlockwise,
        draw_instructions,
        *args,
        **kwargs,
    ):
        draw_instructions.append(
            (
                "ellipse",
                dict(
                    **{
                        "x": x,
                        "y": y,
                        "radiusx": radiusx,
                        "radiusy": radiusy,
                        "rotation": rotation,
                        "startangle": startangle,
                        "endangle": endangle,
                        "anticlockwise": anticlockwise,
                    },
                    **kwargs,
                ),
            )
        )

    def rect(self, x, y, width, height, draw_instructions, **kwargs):
        draw_instructions.append(
            (
                "rect",
                dict(
                    **{
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height,
                    },
                    **kwargs,
                ),
            )
        )

    # Drawing Paths
    def fill(self, color, fill_rule, draw_instructions, **kwargs):
        draw_instructions.append(
            (
                "fill",
                dict(
                    **{
                        "color": color,
                        "fill_rule": fill_rule,
                    },
                    **kwargs,
                ),
            )
        )

    def stroke(self, color, line_width, line_dash, draw_instructions, **kwargs):
        draw_instructions.append(
            (
                "stroke",
                dict(
                    **{
                        "color": color,
                        "line_width": line_width,
                        "line_dash": line_dash,
                    },
                    **kwargs,
                ),
            )
        )

    # Transformations

    def rotate(self, radians, draw_instructions, **kwargs):
        draw_instructions.append(("rotate", dict(**{"radians": radians}, **kwargs)))

    def scale(self, sx, sy, draw_instructions, **kwargs):
        draw_instructions.append(("scale", dict(**{"sx": sx, "sy": sy}, **kwargs)))

    def translate(self, tx, ty, draw_instructions, **kwargs):
        draw_instructions.append(("translate", dict(**{"tx": tx, "ty": ty}, **kwargs)))

    def reset_transform(self, draw_instructions, **kwargs):
        draw_instructions.append(("reset transform", kwargs))

    # Text

    def write_text(
        self,
        text,
        x,
        y,
        font,
        baseline,
        line_height,
        draw_instructions,
        **kwargs,
    ):
        draw_instructions.append(
            (
                "write text",
                dict(
                    **{
                        "text": text,
                        "x": x,
                        "y": y,
                        "font": font,
                        "baseline": baseline,
                        "line_height": line_height,
                    },
                    **kwargs,
                ),
            )
        )

    def measure_text(self, text, font, line_height):
        # Assume system font produces characters that have the same width and height as
        # the point size, with a default point size of 12. Any other font is 1.5 times
        # bigger.
        lines = text.count("\n") + 1
        if font.interface.family == SYSTEM:
            if font.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                width = len(text) * 12
                height = lines * line_height * 12
            else:
                width = len(text) * font.interface.size
                height = lines * line_height * font.interface.size
        else:
            if font.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                width = len(text) * 18
                height = lines * line_height * 18
            else:
                width = int(len(text) * font.interface.size * 1.5)
                height = lines * line_height * int(font.interface.size * 1.5)

        return width, height

    # Image

    def get_image_data(self):
        """Return the Toga logo as the "native" image."""
        self._action("get image data")
        path = Path(toga_dummy.__file__).parent / "resources/toga.png"
        return path.read_bytes()

    # Resize handlers

    def simulate_resize(self):
        self.interface.on_resize(None)

    # 'Mouse' button handlers

    def simulate_press(self, x, y):
        self.interface.on_press(x=x, y=y)

    def simulate_activate(self, x, y):
        self.interface.on_activate(x=x, y=y)

    def simulate_alt_press(self, x, y):
        self.interface.on_alt_press(x=x, y=y)

    def simulate_release(self, x, y):
        self.interface.on_release(x=x, y=y)

    def simulate_alt_release(self, x, y):
        self.interface.on_alt_release(x=x, y=y)

    def simulate_drag(self, x, y):
        self.interface.on_drag(x=x, y=y)

    def simulate_alt_drag(self, x, y):
        self.interface.on_alt_drag(x=x, y=y)
