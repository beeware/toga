from toga_winforms.libs import WinForms

from .base import Widget


class Canvas(Widget):
    def create(self):
        self.native = WinForms.Control()

    def set_on_draw(self, handler):
        self.interface.factory.not_implemented('Canvas.set_on_draw()')

    def set_context(self, context):
        self.interface.factory.not_implemented('Canvas.set_context()')

    def line_width(self, width=2.0):
        self.interface.factory.not_implemented('Canvas.line_width()')

    def fill_style(self, color=None):
        self.interface.factory.not_implemented('Canvas.fill_style()')

    def stroke_style(self, color=None):
        self.interface.factory.not_implemented('Canvas.stroke_style()')

    def new_path(self):
        self.interface.factory.not_implemented('Canvas.new_path()')

    def close_path(self):
        self.interface.factory.not_implemented('Canvas.close_path()')

    def move_to(self, x, y):
        self.interface.factory.not_implemented('Canvas.move_to()')

    def line_to(self, x, y):
        self.interface.factory.not_implemented('Canvas.line_to()')

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        self.interface.factory.not_implemented('Canvas.bezier_curve_to()')

    def quadratic_curve_to(self, cpx, cpy, x, y):
        self.interface.factory.not_implemented('Canvas.quadratic_curve_to()')

    def arc(self, x, y, radius, startangle, endangle, anticlockwise):
        self.interface.factory.not_implemented('Canvas.arc()')

    def ellipse(self, x, y, radiusx, radiusy, rotation, startangle, endangle, anticlockwise):
        self.interface.factory.not_implemented('Canvas.ellipse()')

    def rect(self, x, y, width, height):
        self.interface.factory.not_implemented('Canvas.rect()')

    # Drawing Paths

    def fill(self, fill_rule, preserve):
        self.interface.factory.not_implemented('Canvas.fill()')

    def stroke(self):
        self.interface.factory.not_implemented('Canvas.stroke()')

    # Transformations

    def rotate(self, radians):
        self.interface.factory.not_implemented('Canvas.rotate()')

    def scale(self, sx, sy):
        self.interface.factory.not_implemented('Canvas.scale()')

    def translate(self, tx, ty):
        self.interface.factory.not_implemented('Canvas.translate()')

    def reset_transform(self):
        self.interface.factory.not_implemented('Canvas.reset_transform()')

    def write_text(self, text, x, y, font):
        self.interface.factory.not_implemented('Canvas.write_text()')

    def measure_text(self, text, font):
        self.interface.factory.not_implemented('Canvas.measure_text()')

    def rehint(self):
        self.interface.factory.not_implemented('Canvas.rehint()')
