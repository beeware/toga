from pathlib import Path

import toga_dummy
from toga.fonts import SYSTEM, SYSTEM_DEFAULT_FONT_SIZE

from .base import Widget


class Context:
    def __init__(self, impl):
        self.impl = impl

    # Context management
    def save(self):
        self.impl.draw_instructions.append("save")

    def restore(self):
        self.impl.draw_instructions.append("restore")

    # Setting attributes
    def set_fill_style(self, color):
        self.impl.draw_instructions.append(("set fill style", color))

    def set_line_dash(self, line_dash):
        self.impl.draw_instructions.append(("set line dash", line_dash))

    def set_line_width(self, line_width):
        self.impl.draw_instructions.append(("set line width", line_width))

    def set_stroke_style(self, color):
        self.impl.draw_instructions.append(("set stroke style", color))

    # Basic paths
    def begin_path(self):
        self.impl.draw_instructions.append("begin path")

    def close_path(self):
        self.impl.draw_instructions.append("close path")

    def move_to(self, x, y):
        self.impl.draw_instructions.append(("move to", {"x": x, "y": y}))

    def line_to(self, x, y):
        self.impl.draw_instructions.append(("line to", {"x": x, "y": y}))

    # Basic shapes
    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.impl.draw_instructions.append(
            (
                "bezier curve to",
                {
                    "cp1x": cp1x,
                    "cp1y": cp1y,
                    "cp2x": cp2x,
                    "cp2y": cp2y,
                    "x": x,
                    "y": y,
                },
            )
        )

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self.impl.draw_instructions.append(
            (
                "quadratic curve to",
                {"cpx": cpx, "cpy": cpy, "x": x, "y": y},
            )
        )

    def arc(self, x, y, radius, startangle, endangle, counterclockwise):
        self.impl.draw_instructions.append(
            (
                "arc",
                {
                    "x": x,
                    "y": y,
                    "radius": radius,
                    "startangle": startangle,
                    "endangle": endangle,
                    "counterclockwise": counterclockwise,
                },
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
        counterclockwise,
    ):
        self.impl.draw_instructions.append(
            (
                "ellipse",
                {
                    "x": x,
                    "y": y,
                    "radiusx": radiusx,
                    "radiusy": radiusy,
                    "rotation": rotation,
                    "startangle": startangle,
                    "endangle": endangle,
                    "counterclockwise": counterclockwise,
                },
            )
        )

    def rect(self, x, y, width, height):
        self.impl.draw_instructions.append(
            (
                "rect",
                {"x": x, "y": y, "width": width, "height": height},
            )
        )

    # Drawing Paths
    def fill(self, fill_rule):
        self.impl.draw_instructions.append(("fill", {"fill_rule": fill_rule}))

    def stroke(self):
        self.impl.draw_instructions.append("stroke")

    # Transformations

    def rotate(self, radians):
        self.impl.draw_instructions.append(("rotate", {"radians": radians}))

    def scale(self, sx, sy):
        self.impl.draw_instructions.append(("scale", {"sx": sx, "sy": sy}))

    def translate(self, tx, ty):
        self.impl.draw_instructions.append(("translate", {"tx": tx, "ty": ty}))

    def reset_transform(self):
        self.impl.draw_instructions.append("reset transform")

    # Text

    def write_text(self, text, x, y, font, baseline, line_height):
        self.impl.draw_instructions.append(
            (
                "write text",
                {
                    "text": text,
                    "x": x,
                    "y": y,
                    "font": font,
                    "baseline": baseline,
                    "line_height": line_height,
                },
            )
        )

    # Image

    def draw_image(self, image, x, y, width, height):
        """Draw an Image into the context."""
        self.impl.draw_instructions.append(
            (
                "draw_image",
                {"image": image, "x": x, "y": y, "width": width, "height": height},
            )
        )


class Canvas(Widget):
    def create(self):
        self._action("create Canvas")

    def redraw(self):
        self._action("redraw")
        self.draw_instructions = []
        self.interface.context._draw(Context(self))

    def measure_text(self, text, font, line_height):
        # Assume system font produces characters that have the same width and height as
        # the point size, with a default point size of 12. Any other font is 1.5 times
        # bigger.

        if line_height is None:
            line_height_factor = 1
        else:
            line_height_factor = line_height

        lines = text.count("\n") + 1
        if font.interface.family == SYSTEM:
            if font.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                width = len(text) * 12
                height = lines * line_height_factor * 12
            else:
                width = len(text) * font.interface.size
                height = lines * line_height_factor * font.interface.size
        else:
            if font.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
                width = len(text) * 18
                height = lines * line_height_factor * 18
            else:
                width = int(len(text) * font.interface.size * 1.5)
                height = lines * line_height_factor * int(font.interface.size * 1.5)

        return width, height

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
