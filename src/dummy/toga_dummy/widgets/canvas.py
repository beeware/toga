from .base import Widget


class Canvas(Widget):
    def create(self):
        self._action("create Canvas")

    def redraw(self):
        self._action("redraw")
        self.interface._draw(self)

    # Basic paths

    def new_path(self, *args, **kwargs):
        self._action("new path")

    def closed_path(self, x, y, *args, **kwargs):
        self._action("closed path", x=x, y=y)

    def move_to(self, x, y, *args, **kwargs):
        self._action("move to", x=x, y=y)

    def line_to(self, x, y, *args, **kwargs):
        self._action("line to", x=x, y=y)

    # Basic shapes

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y, *args, **kwargs):
        self._action(
            "bezier curve to", cp1x=cp1x, cp1y=cp1y, cp2x=cp2x, cp2y=cp2y, x=x, y=y
        )

    def quadratic_curve_to(self, cpx, cpy, x, y, *args, **kwargs):
        self._action("quadratic curve to", cpx=cpx, cpy=cpy, x=x, y=y)

    def arc(self, x, y, radius, startangle, endangle, anticlockwise, *args, **kwargs):
        self._action(
            "arc",
            x=x,
            y=y,
            radius=radius,
            startangle=startangle,
            endangle=endangle,
            anticlockwise=anticlockwise,
        )

    def ellipse(
        self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise, *args, **kwargs
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
        )

    def rect(self, x, y, width, height, *args, **kwargs):
        self._action("rect", x=x, y=y, width=width, height=height)

    # Drawing Paths

    def fill(self, color, fill_rule, preserve, *args, **kwargs):
        self._action("fill", color=color, fill_rule=fill_rule, preserve=preserve)

    def stroke(self, color, line_width, line_dash, *args, **kwargs):
        self._action("stroke", color=color, line_width=line_width, line_dash=line_dash)

    # Transformations

    def rotate(self, radians, *args, **kwargs):
        self._action("rotate", radians=radians)

    def scale(self, sx, sy, *args, **kwargs):
        self._action("scale", sx=sx, sy=sy)

    def translate(self, tx, ty, *args, **kwargs):
        self._action("translate", tx=tx, ty=ty)

    def reset_transform(self, *args, **kwargs):
        self._action("reset transform")

    # Text

    def write_text(self, text, x, y, font, *args, **kwargs):
        self._action("write text", text=text, x=x, y=y, font=font)

    def measure_text(self, text, font, tight=False):
        self._action("measure text", text=text, font=font, tight=tight)

    # Rehint

    def set_on_resize(self, handler):
        self._set_value('on_resize', handler)

    # 'Mouse' button handlers

    def set_on_press(self, handler):
        """Ensure the correct handler is invoked."""
        self._set_value("on_press", handler)

    def set_on_alt_press(self, handler):
        """Ensure the correct handler is invoked."""
        self._set_value("on_alt_press", handler)

    def set_on_release(self, handler):
        """Ensure the correct handler is invoked."""
        self._set_value("on_release", handler)

    def set_on_alt_release(self, handler):
        """Ensure the correct handler is invoked."""
        self._set_value("on_alt_release", handler)

    def set_on_drag(self, handler):
        """Ensure the correct handler is invoked."""
        self._set_value("on_drag", handler)

    def set_on_alt_drag(self, handler):
        """Ensure the correct handler is invoked."""
        self._set_value("on_alt_drag", handler)
