from tailor.cassowary import LayoutManager, Equation, Inequality, approx_equal
from tailor.constraint import Constraint

from .base import Widget


class Container(Widget):
    _RELATION = {
        Constraint.LTE: Inequality.LEQ,
        Constraint.GTE: Inequality.GEQ
    }

    def __init__(self):
        super(Container, self).__init__()
        self._layout_manager = LayoutManager(self._bounding_box)
        self._window = None

    def add(self, widget):
        self._layout_manager.add_widget(widget)
        if self._window:
            widget._create(self._window)

    def constrain(self, constraint):
        "Add the given constraint to the widget."
        widget = constraint.attr.widget
        identifier = constraint.attr.identifier

        if constraint.related_attr:
            related_widget = constraint.related_attr.widget
            related_identifier = constraint.related_attr.identifier

            expr1 = widget._expression(identifier)
            if not approx_equal(constraint.attr.multiplier, 1.0):
                expr1 = expr1 * constraint.attr.multiplier
            if not approx_equal(constraint.attr.constant, 0.0):
                expr1 = expr1 + constraint.attr.constant

            expr2 = related_widget._expression(related_identifier)
            if not approx_equal(constraint.related_attr.multiplier, 1.0):
                expr2 = expr2 * constraint.related_attr.multiplier
            if not approx_equal(constraint.related_attr.constant, 0.0):
                expr2 = expr2 + constraint.related_attr.constant

            if constraint.relation == Constraint.EQUAL:
                self._layout_manager.add_constraint(Equation(expr1, expr2))
            else:
                self._layout_manager.add_constraint(Inequality(expr1, self._RELATION[constraint.relation], expr2))
        else:
            expr = widget._expression(identifier)
            if not approx_equal(constraint.attr.multiplier, 1.0):
                expr = expr * constraint.attr.multiplier

            if constraint.relation == Constraint.EQUAL:
                self._layout_manager.add_constraint(Equation(expr, constraint.attr.constant))
            else:
                self._layout_manager.add_constraint(Equation(expr, self._RELATION[constraint.relation], constraint.attr.constant))

    def _create(self, window, x, y, width, height):
        self._window = window
        for widget in self._layout_manager.children:

            min_width, preferred_width = widget._width_hint
            min_height, preferred_height = widget._height_hint

            x_pos = widget._bounding_box.x.value
            if widget._expand_horizontal:
                width = widget._bounding_box.width.value
            else:
                x_pos = x_pos + ((widget._bounding_box.width.value - preferred_width) / 2.0)
                width = preferred_width

            y_pos = widget._bounding_box.y.value
            if widget._expand_vertical:
                height = widget._bounding_box.height.value
            else:
                y_pos = y_pos + ((widget._bounding_box.height.value - preferred_height) / 2.0)
                height = preferred_height

            widget._create(window, x_pos, y_pos, width, height)

    def _resize(self, x, y, width, height):
        self._layout_manager.enforce(width, height)

        for widget in self._layout_manager.children:
            min_width, preferred_width = widget._width_hint
            min_height, preferred_height = widget._height_hint

            x_pos = widget._bounding_box.x.value
            if widget._expand_horizontal:
                width = widget._bounding_box.width.value
            else:
                x_pos = x_pos + ((widget._bounding_box.width.value - preferred_width) / 2.0)
                width = preferred_width

            y_pos = widget._bounding_box.y.value
            if widget._expand_vertical:
                height = widget._bounding_box.height.value
            else:
                y_pos = y_pos + ((widget._bounding_box.height.value - preferred_height) / 2.0)
                height = preferred_height

            widget._resize(x_pos, y_pos, width, height)

        self._layout_manager.relax()

    @property
    def _width_hint(self):
        width = self._layout_manager.bounding_box.width.value
        print "PREFERRED WIDTH", width
        return width, width

    @property
    def _height_hint(self):
        height = self._layout_manager.bounding_box.height.value
        print "PREFERRED HEIGHT", height
        return height, height
