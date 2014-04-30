from toga.constraint import Attribute, Constraint
from toga.widget import Widget as WidgetBase

from .constraint import Inequality, Equation
from .expression import Expression
from .layout import BoundingBox, LayoutManager

from .utils import approx_equal



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
        raise NotImplemented()

    @property
    def _height_hint(self):
        raise NotImplemented()



class Container(Widget):
    _RELATION = {
        Constraint.LTE: Inequality.LEQ,
        Constraint.GTE: Inequality.GEQ
    }

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
