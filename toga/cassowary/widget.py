from __future__ import print_function, absolute_import, division

from toga.constraint import Attribute, Constraint
from toga.widget import Widget as WidgetBase

from .layout import BoundingBox, LayoutManager


class Widget(WidgetBase):
    def __init__(self):
        super(Widget, self).__init__()
        self._bounding_box = BoundingBox()
        self._expand_horizontal = True
        self._expand_vertical = True

    def _expression(self, identifier):
        if identifier == Attribute.LEFT:
            return self._bounding_box.x
        elif identifier == Attribute.RIGHT:
            return self._bounding_box.x + self._bounding_box.width
        elif identifier == Attribute.TOP:
            return self._bounding_box.y
        elif identifier == Attribute.BOTTOM:
            return self._bounding_box.y + self._bounding_box.height
        elif identifier == Attribute.LEADING:
            return self._bounding_box.x
        elif identifier == Attribute.TRAILING:
            return self._bounding_box.x + self._bounding_box.width
        elif identifier == Attribute.WIDTH:
            return self._bounding_box.width
        elif identifier == Attribute.HEIGHT:
            return self._bounding_box.height
        elif identifier == Attribute.CENTER_X:
            return self._bounding_box.x + (self._bounding_box.width / 2)
        elif identifier == Attribute.CENTER_Y:
            return self._bounding_box.y + (self._bounding_box.height / 2)
        # elif identifier == self.BASELINE:
        #     return ...

    @property
    def _width_hint(self):
        raise NotImplementedError()

    @property
    def _height_hint(self):
        raise NotImplementedError()


class Container(Widget):
    def __init__(self):
        super(Container, self).__init__()
        self.children = []
        self.constraints = {}

        self.startup()

    def startup(self):
        self._layout_manager = LayoutManager(self._bounding_box)
        self._impl = self._create_container()

    def add(self, widget):
        self.children.append(widget)

        # Assign the widget to the same app and window as the container.
        widget.window = self.window
        widget.app = self.app
        self._layout_manager.add_widget(widget)
        self._impl.add(widget._impl)

    def _set_app(self, app):
        for child in self.children:
            child.app = app

    def _set_window(self, window):
        for child in self.children:
            child.window = window

    def constrain(self, constraint):
        "Add the given constraint to the widget."
        if constraint in self.constraints:
            return

        widget = constraint.attr.widget
        identifier = constraint.attr.identifier

        if constraint.related_attr:
            related_widget = constraint.related_attr.widget
            related_identifier = constraint.related_attr.identifier

            expr1 = widget._expression(identifier) * constraint.attr.multiplier + constraint.attr.constant
            expr2 = related_widget._expression(related_identifier) * constraint.related_attr.multiplier + constraint.related_attr.constant

            if constraint.relation == Constraint.EQUAL:
                self._layout_manager.add_constraint(expr1 == expr2)
            elif constraint.relation == Constraint.LTE:
                self._layout_manager.add_constraint(expr1 <= expr2)
            elif constraint.relation == Constraint.GTE:
                self._layout_manager.add_constraint(expr1 >= expr2)

        else:
            expr = widget._expression(identifier) * constraint.attr.multiplier

            if constraint.relation == Constraint.EQUAL:
                self._layout_manager.add_constraint(expr == constraint.attr.constant)
            elif constraint.relation == Constraint.LTE:
                self._layout_manager.add_constraint(expr <= constraint.attr.constant)
            elif constraint.relation == Constraint.GTE:
                self._layout_manager.add_constraint(expr >= constraint.attr.constant)
