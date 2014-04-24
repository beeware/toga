from tailor.cassowary import Expression, BoundingBox
from tailor.constraint import Attribute
from tailor.widget import WidgetBase


def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)
    return _handler


class Widget(WidgetBase):
    def __init__(self):
        super(Widget, self).__init__()
        self._bounding_box = BoundingBox()
        self._expand_horizontal = True
        self._expand_vertical = True

    def _expression(self, identifier):
        if identifier == Attribute.LEFT:
            return Expression(variable=self._bounding_box.x)
        elif identifier == Attribute.RIGHT:
            return Expression(variable=self._bounding_box.x) + Expression(variable=self._bounding_box.width)
        elif identifier == Attribute.TOP:
            return Expression(variable=self._bounding_box.y)
        elif identifier == Attribute.BOTTOM:
            return Expression(variable=self._bounding_box.y) + Expression(variable=self._bounding_box.height)
        elif identifier == Attribute.LEADING:
            return Expression(variable=self._bounding_box.x)
        elif identifier == Attribute.TRAILING:
            return Expression(variable=self._bounding_box.x) + Expression(variable=self._bounding_box.width)
        elif identifier == Attribute.WIDTH:
            return Expression(variable=self._bounding_box.width)
        elif identifier == Attribute.HEIGHT:
            return Expression(variable=self._bounding_box.height)
        elif identifier == Attribute.CENTER_X:
            return Expression(variable=self._bounding_box.x) + (Expression(variable=self._bounding_box.width) / 2)
        elif identifier == Attribute.CENTER_Y:
            return Expression(variable=self._bounding_box.y) + (Expression(variable=self._bounding_box.height) / 2)
        # elif identifier == self.BASELINE:
        #     return ...

    @property
    def _width_hint(self):
        return self._impl.get_preferred_width()

    @property
    def _height_hint(self):
        return self._impl.get_preferred_height()
