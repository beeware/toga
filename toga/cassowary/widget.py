from __future__ import print_function, unicode_literals, absolute_import, division

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
        raise NotImplemented()

    @property
    def _height_hint(self):
        raise NotImplemented()



class Container(Widget):
    def __init__(self):
        super(Container, self).__init__()
        self._layout_manager = LayoutManager(self._bounding_box)

    def add(self, widget):
        self._impl.add(widget._impl)
        self._layout_manager.add_widget(widget)

    def constrain(self, constraint):
        "Add the given constraint to the widget."
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
