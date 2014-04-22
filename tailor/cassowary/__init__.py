# Implementation of the Cassowary algorithm
# http://www.cs.washington.edu/research/constraints/cassowary/

from .constraint import Equation, Inequality, StayConstraint, EditConstraint
from .expression import Expression
from .simplex_solver import SimplexSolver
from .strength import REQUIRED, STRONG, MEDIUM, WEAK
from .variable import Variable
from .utils import approx_equal
