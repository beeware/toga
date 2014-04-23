from gi.repository import Gtk, cairo

from tailor.constraint import Constraint
from tailor.cassowary import SimplexSolver, StayConstraint, WEAK, STRONG, REQUIRED, Equation, Inequality, Expression, approx_equal
from .base import Widget


class LayoutManager(SimplexSolver):
    def __init__(self, bounding_box):
        super(LayoutManager, self).__init__()
        self.bounding_box = bounding_box

        self.children = {}

        # Enforce a hard constraint that the container starts at 0,0
        self.add_constraint(StayConstraint(self.bounding_box.x, strength=REQUIRED))
        self.add_constraint(StayConstraint(self.bounding_box.y, strength=REQUIRED))

        # # Add a weak constraint for the bounds of the container.
        self.width_constraint = StayConstraint(self.bounding_box.width, strength=WEAK)
        self.height_constraint = StayConstraint(self.bounding_box.height, strength=WEAK)

        self.add_constraint(self.width_constraint)
        self.add_constraint(self.height_constraint)

    def add_constraint(self, constraint):
        print constraint
        return super(LayoutManager, self).add_constraint(constraint)

    def add_widget(self, widget):
        constraints = set()

        min_width, preferred_width = widget._width_hint
        min_height, preferred_height = widget._height_hint

        print min_width, preferred_width
        print min_height, preferred_height
        # REQUIRED: Widget width must exceed minimum.
        constraints.add(self.add_constraint(
            Inequality(
                Expression(variable=widget._bounding_box.width),
                Inequality.GEQ,
                min_width,
            )
        ))

        # REQUIRED: Widget height must exceed minimum
        constraints.add(self.add_constraint(
            Inequality(
                Expression(variable=widget._bounding_box.height),
                Inequality.GEQ,
                min_height,
            )
        ))

        # STRONG: Adhere to preferred widget width
        constraints.add(self.add_constraint(
            Equation(
                Expression(variable=widget._bounding_box.width),
                preferred_width,
                strength=STRONG
            )
        ))

        # STRONG: Try to adhere to preferred widget height
        constraints.add(self.add_constraint(
            Equation(
                Expression(variable=widget._bounding_box.height),
                preferred_height,
                strength=STRONG
            )
        ))

        print constraints
        self.children[widget] = constraints

    def enforce(self, width, height):
        self.remove_constraint(self.width_constraint)
        self.remove_constraint(self.height_constraint)

        self.bounding_box.width.value = width
        self.bounding_box.height.value = height

        self.width_constraint = StayConstraint(self.bounding_box.width, strength=REQUIRED)
        self.height_constraint = StayConstraint(self.bounding_box.height, strength=REQUIRED)

        self.add_constraint(self.width_constraint)
        self.add_constraint(self.height_constraint)

    def relax(self):
        self.remove_constraint(self.width_constraint)
        self.remove_constraint(self.height_constraint)

        self.bounding_box.width.value = 0
        self.bounding_box.height.value = 0

        self.width_constraint = StayConstraint(self.bounding_box.width, strength=WEAK)
        self.height_constraint = StayConstraint(self.bounding_box.height, strength=WEAK)

        self.add_constraint(self.width_constraint)
        self.add_constraint(self.height_constraint)


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
        print "Size allocate", allocation.width, 'x', allocation.height, ' @ ', allocation.x, 'x', allocation.y

        self.set_allocation(allocation)

        # Temporarily enforce a size requirement based on the allocation
        self.layout_manager.enforce(allocation.width, allocation.height)

        for widget in self.layout_manager.children:
            print widget, widget._bounding_box
            if not widget._impl.get_visible():
                print "CHILD NOT VISIBLE"
            else:
                print "CHILD", widget

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

        # Restore the unbounded allocation
        self.layout_manager.relax()


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

            print 'E1', expr1
            print 'E2', expr2

            if constraint.relation == Constraint.EQUAL:
                self._layout_manager.add_constraint(Equation(expr1, expr2))
            else:
                self._layout_manager.add_constraint(Inequality(expr1, self._RELATION[constraint.relation], expr2))
        else:
            expr = widget._expression(identifier)
            if not approx_equal(constraint.attr.multiplier, 1.0):
                expr = expr * constraint.attr.multiplier

            print 'E', expr

            if constraint.relation == Constraint.EQUAL:
                self._layout_manager.add_constraint(Equation(expr, constraint.attr.constant))
            else:
                self._layout_manager.add_constraint(Equation(expr, self._RELATION[constraint.relation], constraint.attr.constant))
