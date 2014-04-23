# from tailor.cassowary import Expression
# from tailor.constraint import Attribute
from tailor.widget import WidgetBase, BoundingBox


class Widget(WidgetBase):
    def __init__(self):
        super(Widget, self).__init__()
        self._bounding_box = BoundingBox()
