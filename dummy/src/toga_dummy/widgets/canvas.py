import random
import uuid
from unittest.mock import Mock

from .base import Widget


class Canvas(Widget):
    def create(self):
        self._action("create Canvas")
        self.native_context = Mock()

    def redraw(self):
        self._action("redraw")
        self.interface._draw(self, native_context=self.native_context)

    # Context management

    def push_context(self, native_context, **kwargs):
        self._action("push context", native_context=native_context)

    def pop_context(self, native_context, **kwargs):
        self._action("pop context", native_context=native_context)

    # Basic paths

    def begin_path(self, native_context, **kwargs):
        self._action("begin path", native_context=native_context)

    def close_path(self, x, y, native_context, **kwargs):
        self._action("close path", x=x, y=y, native_context=native_context)

    def move_to(self, x, y, native_context, **kwargs):
        self._action("move to", x=x, y=y, native_context=native_context)

    def line_to(self, x, y, native_context, **kwargs):
        self._action("line to", x=x, y=y, native_context=native_context)

    # Basic shapes

    def bezier_curve_to(
        self,
        cp1x,
        cp1y,
        cp2x,
        cp2y,
        x,
        y,
        native_context,
        *args,
        **kwargs,
    ):
        self._action(
            "bezier curve to",
            cp1x=cp1x,
            cp1y=cp1y,
            cp2x=cp2x,
            cp2y=cp2y,
            x=x,
            y=y,
            native_context=native_context,
        )

    def quadratic_curve_to(self, cpx, cpy, x, y, native_context, **kwargs):
        self._action(
            "quadratic curve to",
            cpx=cpx,
            cpy=cpy,
            x=x,
            y=y,
            native_context=native_context,
        )

    def arc(
        self,
        x,
        y,
        radius,
        startangle,
        endangle,
        anticlockwise,
        native_context,
        *args,
        **kwargs,
    ):
        self._action(
            "arc",
            x=x,
            y=y,
            radius=radius,
            startangle=startangle,
            endangle=endangle,
            anticlockwise=anticlockwise,
            native_context=native_context,
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
        native_context,
        *args,
        **kwargs,
    ):
        self._action(
            "ellipse",
            x=x,
            y=y,
            radiusx=radiusx,
            radiusy=radiusy,
            rotation=rotation,
            startangle=startangle,
            endangle=endangle,
            anticlockwise=anticlockwise,
            native_context=native_context,
        )

    def rect(self, x, y, width, height, native_context, **kwargs):
        self._action(
            "rect",
            x=x,
            y=y,
            width=width,
            height=height,
            native_context=native_context,
        )

    # Drawing Paths

    def fill(self, color, fill_rule, preserve, native_context, **kwargs):
        self._action(
            "fill",
            color=color,
            fill_rule=fill_rule,
            preserve=preserve,
            native_context=native_context,
        )

    def stroke(self, color, line_width, line_dash, native_context, **kwargs):
        self._action(
            "stroke",
            color=color,
            line_width=line_width,
            line_dash=line_dash,
            native_context=native_context,
        )

    # Transformations

    def rotate(self, radians, native_context, **kwargs):
        self._action("rotate", radians=radians, native_context=native_context)

    def scale(self, sx, sy, native_context, **kwargs):
        self._action("scale", sx=sx, sy=sy, native_context=native_context)

    def translate(self, tx, ty, native_context, **kwargs):
        self._action("translate", tx=tx, ty=ty, native_context=native_context)

    def reset_transform(self, native_context, **kwargs):
        self._action("reset transform", native_context=native_context)

    # Text

    def write_text(self, text, x, y, font, native_context, **kwargs):
        self._action(
            "write text",
            text=text,
            x=x,
            y=y,
            font=font,
            native_context=native_context,
        )

    def measure_text(self, text, font, tight=False):
        self._action("measure text", text=text, font=font, tight=tight)
        return random.randint(100, 300), random.randint(100, 200)

    # Image

    def get_image_data(self):
        """Return a dummy uuid string as the "native" image."""
        self._action("get image data")
        return uuid.uuid4()

    # Resize handlers

    def simulate_resize(self):
        self.interface.on_resize(None)

    # 'Mouse' button handlers

    def simulate_press(self, x, y, click_count):
        self.interface.on_press(None, x=x, y=y, click_count=click_count)

    def simulate_alt_press(self, x, y, click_count):
        self.interface.on_alt_press(None, x=x, y=y, click_count=click_count)

    def simulate_release(self, x, y, click_count):
        self.interface.on_release(None, x=x, y=y, click_count=click_count)

    def simulate_alt_release(self, x, y, click_count):
        self.interface.on_alt_release(None, x=x, y=y, click_count=click_count)

    def simulate_drag(self, x, y, click_count):
        self.interface.on_drag(None, x=x, y=y, click_count=click_count)

    def simulate_alt_drag(self, x, y, click_count):
        self.interface.on_alt_drag(None, x=x, y=y, click_count=click_count)
