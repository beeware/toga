from .error import InternalError
from .expression import Expression
from .strength import REQUIRED, repr_strength
from .variable import Variable


class Constraint(object):
    def __init__(self, strength, weight=1.0):
        self.strength = strength
        self.weight = weight
        self.is_edit_constraint = False
        self.is_inequality = False
        self.is_stay_constraint = False

    @property
    def is_required(self):
        return self.strength == REQUIRED

    def __repr__(self):
        return u'%s:{%s}(%s)' % (repr_strength(self.strength), self.weight, self.expression)


class EditConstraint(Constraint):
    def __init__(self, variable, strength, weight=1.0):
        super(EditConstraint, self).__init__(strength, weight)
        self.variable = variable
        self.expression = Expression(variable, -1.0, variable.value)
        self.is_edit_constraint = True

    def __repr__(self):
        return u'edit:%s' % super(EditConstraint, self).__repr__()


class StayConstraint(Constraint):
    def __init__(self, variable, strength, weight=1.0):
        super(StayConstraint, self).__init__(strength, weight)
        self.variable = variable
        self.expression = Expression(variable, -1.0, variable.value)
        self.is_stay_constraint=True

    def __repr__(self):
        return u'stay:%s' % super(StayConstraint, self).__repr__()


class LinearConstraint(Constraint):
    def __init__(self, expression, strength=REQUIRED, weight=1.0):
        super(LinearConstraint, self).__init__(strength=strength, weight=weight)
        self.expression = expression

    def __repr__(self):
        return u'linear:%s' % super(LinearConstraint, self).__repr__()


class Inequality(LinearConstraint):
    LEQ = -1
    GEQ = 1

    def __init__(self, param1, operator=None, param2=None, strength=REQUIRED, weight=1.0):
        """Define a new linear inequality.

        param1 may be an expression or variable
        param2 may be an expression, variable, or constant, or may be ommitted entirely.
        If param2 is specified, the operator must be either LEQ or GEQ
        """
        if isinstance(param1, Expression):
            if param2 is None:
                super(Inequality, self).__init__(param1, strength=strength, weight=weight)
            elif isinstance(param2, Expression):
                super(Inequality, self).__init__(param2.clone(), strength=strength, weight=weight)
                if operator == self.LEQ:
                    self.expression.add_expression(param1, -1.0)
                elif operator == self.GEQ:
                    self.expression.multply(-1)
                    self.expression.add_expression(param1, 1.0)
                else:
                    raise InternalError("Invalid operator in Inequality constructor")
            elif isinstance(param2, Variable):
                super(Inequality, self).__init__(param1.clone(), strength=strength, weight=weight)
                if operator == self.LEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param2, 1.0)
                elif operator == self.GEQ:
                    self.expression.add_variable(param2, -1.0)
                else:
                    raise InternalError("Invalid operator in Inequality constructor")

            # elif isinstance(param2, (float, int)):
            else:
                raise InternalError("Invalid parameters to Inequality constructor")

        elif isinstance(param1, Variable):
            if isinstance(param2, Expression):
                super(Inequality, self).__init__(param2.clone(), strength=strength, weight=weight)
                if operator == self.LEQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.GEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param1, 1.0)
                else:
                    raise InternalError("Invalid operator in Inequality constructor")

            elif isinstance(param2, Variable):
                super(Inequality, self).__init__(Expression(variable=param2), strength=strength, weight=weight)
                if operator == self.LEQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.GEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param1, 1.0)
                else:
                    raise InternalError("Invalid operator in Inequality constructor")

            elif isinstance(param2, (float, int)):
                super(Inequality, self).__init__(Expression(constant=param2), strength=strength, weight=weight)
                if operator == self.LEQ:
                    self.expression.add_variable(param1, -1.0)
                elif operator == self.GEQ:
                    self.expression.multiply(-1.0)
                    self.expression.add_variable(param1, 1.0)
                else:
                    raise InternalError("Invalid operator in Inequality constructor")
            else:
                raise InternalError("Invalid parameters to Inequality constructor")
        else:
            raise InternalError("Invalid parameters to Inequality constructor")

        self.is_inequality = True


class Equation(LinearConstraint):
    def __init__(self, param1, param2=None, strength=REQUIRED, weight=1.0):
        """Define a new linear inequality.

        param1 may be an expression or variable
        param2 may be an expression, variable, or constant, or may be ommitted entirely.
        """
        if isinstance(param1, Expression):
            if param2 is None:
                super(Equation, self).__init__(param1, strength=strength, weight=weight)
            elif isinstance(param2, Expression):
                super(Equation, self).__init__(param1.clone(), strength=strength, weight=weight)
                self.expression.add_expression(param2, -1.0)
            elif isinstance(param2, Variable):
                super(Equation, self).__init__(param1.clone(), strength=strength, weight=weight)
                self.expression.add_variable(param2, -1.0)
            # elif isinstance(param2, (float, int)):
            else:
                raise InternalError("Invalid parameters to Equation constructor")

        elif isinstance(param1, Variable):
            if isinstance(param2, Expression):
                super(Equation, self).__init__(param2, strength=strength, weight=weight)
                self.expression.add_variable(param1, -1.0)
            elif isinstance(param2, Variable):
                super(Equation, self).__init__(Expression(variable=param2), strength=strength, weight=weight)
            elif isinstance(param2, (float, int)):
                super(Equation, self).__init__(Expression(value=param2), strength=strength, weight=weight)
                self.expression.add_variable(param1, -1.0)
            else:
                raise InternalError("Invalid parameters to Equation constructor")
        else:
            raise InternalError("Invalid parameters to Equation constructor")
