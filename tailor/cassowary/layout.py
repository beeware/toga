from .simplex_solver import SimplexSolver
from .constraint import StayConstraint, Equation, Inequality
from .strength import WEAK, STRONG, REQUIRED
from .expression import Expression
from .variable import Variable


class BoundingBox(object):
    def __init__(self):
        self.x = Variable('x', 0.0)
        self.y = Variable('y', 0.0)
        self.width = Variable('width', 0.0)
        self.height = Variable('height', 0.0)

    def __repr__(self):
        return u'%sx%s @ %s,%s' % (self.width.value, self.height.value, self.x.value, self.y.value)


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
        return super(LayoutManager, self).add_constraint(constraint)

    def add_widget(self, widget):
        constraints = set()

        min_width, preferred_width = widget._width_hint
        min_height, preferred_height = widget._height_hint

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
