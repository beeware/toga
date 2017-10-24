import gi
try:
    gi.require_foreign("cairo")
except ImportError:
    print("Pycairo integration required for Context2D :(")

from .base import Widget


class Matrix(Widget):
    def create(self):
        self.native = cairo.Matrix()
        self.native.interface = self.interface

    def transform_point(self, x, y):
        return self.native.transform_point(x, y)
