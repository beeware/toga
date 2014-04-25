from gi.repository import Gtk, cairo

from tailor.cassowary import LayoutManager, Equation, Inequality, approx_equal
from tailor.constraint import Constraint
from .base import Widget


class TContainer(Gtk.Fixed):
    def __init__(self, layout_manager):
        super(TContainer, self).__init__()
        self.layout_manager = layout_manager

    def do_get_preferred_width(self):
        # Calculate the minimum and natural width of the container.
        width = self.layout_manager.bounding_box.width.value
        # print "PREFERRED WIDTH", width
        return width, width

    def do_get_preferred_height(self):
        # Calculate the minimum and natural height of the container.
        height = self.layout_manager.bounding_box.height.value
        # print "PREFERRED HEIGHT", height
        return height, height

    def do_size_allocate(self, allocation):
        # print "Size allocate", allocation.width, 'x', allocation.height, ' @ ', allocation.x, 'x', allocation.y

        self.set_allocation(allocation)

        # Temporarily enforce a size requirement based on the allocation
        with self.layout_manager.layout(allocation.width, allocation.height):

            for widget in self.layout_manager.children:
                print widget, widget._bounding_box
                if not widget._impl.get_visible():
                    print "CHILD NOT VISIBLE"
                else:
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

                    child_allocation = cairo.RectangleInt()
                    child_allocation.x = x_pos
                    child_allocation.y = y_pos
                    child_allocation.width = width
                    child_allocation.height = height

                    widget._impl.size_allocate(child_allocation)


class Container(Widget):
    _RELATION = {
        Constraint.LTE: Inequality.LEQ,
        Constraint.GTE: Inequality.GEQ
    }

    def __init__(self):
        super(Container, self).__init__()
        self._layout_manager = LayoutManager(self._bounding_box)
        self._impl = TContainer(self._layout_manager)

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
