from .constraint import StayConstraint, EditConstraint
from .edit_info import EditInfo
from .error import RequiredFailure, ConstraintNotFound, InternalError
from .expression import Expression
from .strength import STRONG, WEAK
from .tableau import Tableau
from .variable import ObjectiveVariable, SlackVariable, DummyVariable
from .utils import approx_equal, EPSILON


class SimplexSolver(Tableau):
    def __init__(self):
        super(SimplexSolver, self).__init__()

        self.stay_error_vars = []

        self.error_vars = {}
        self.marker_vars = {}

        self.objective = ObjectiveVariable('Z')
        self.edit_var_map = {}

        self.slack_counter = 0
        self.artificial_counter = 0
        self.dummy_counter = 0
        self.auto_solve = True
        self.needs_solving = False

        self.optimize_count = 0

        self.rows[self.objective] = Expression()
        self.edit_variable_stack = [0]

    def __repr__(self):
        parts = []
        parts.append('stay_error_vars: %s' % self.stay_error_vars)
        parts.append('edit_var_map: %s' % self.edit_var_map)
        return super(SimplexSolver, self).__repr__() + '\n' + '\n'.join(parts)

    def add_constraints(self, *constraints):
        for constraint in constraints:
            self.add_constraint(constraint)

    def new_expression(self, cn):
        # print "* new_expression", cn
        # print "cn.is_inequality == ", cn.is_inequality
        # print "cn.is_required == ", cn.is_required
        expr = Expression(constant=cn.expression.constant)
        eplus = None
        eminus = None
        prev_edit_constant = None
        for v, c in cn.expression.terms.items():
            e = self.rows.get(v)
            if not e:
                expr.add_variable(v, c)
            else:
                expr.add_expression(e, c)

        if cn.is_inequality:
            # print "Inequality, adding slack"
            self.slack_counter = self.slack_counter + 1
            slack_var = SlackVariable(number=self.slack_counter, prefix='s')
            expr.set_variable(slack_var, -1)

            self.marker_vars[cn] = slack_var
            if not cn.is_required:
                self.slack_counter = self.slack_counter + 1
                eminus = SlackVariable(number=self.slack_counter, prefix='em')
                expr.set_variable(eminus, 1)
                z_row = self.rows[self.objective]
                z_row.set_variable(eminus, cn.strength * cn.weight)
                self.insert_error_var(cn, eminus)
                self.note_added_variable(eminus, self.objective)
        else:
            if cn.is_required:
                # print "Equality, required"
                self.dummy_counter = self.dummy_counter + 1
                dummy_var = DummyVariable(number=self.dummy_counter, prefix='d')
                eplus = dummy_var
                eminus = dummy_var
                prev_edit_constant = cn.expression.constant
                expr.set_variable(dummy_var, 1)
                self.marker_vars[cn] = dummy_var
                # print "Adding dummy_var == d%s" % self.dummy_counter
            else:
                # print "Equality, not required"
                self.slack_counter = self.slack_counter + 1
                eplus = SlackVariable(number=self.slack_counter, prefix='ep')
                eminus = SlackVariable(number=self.slack_counter, prefix='em')
                expr.set_variable(eplus, -1)
                expr.set_variable(eminus, 1)
                self.marker_vars[cn] = eplus

                z_row = self.rows[self.objective]
                # print "z_row", z_row
                sw_coeff = cn.strength * cn.weight
                # if sw_coeff == 0:
                    # print "cn ==", cn
                    # print "adding ", eplus, "and", eminus, "with sw_coeff", sw_coeff
                z_row.set_variable(eplus, sw_coeff)
                self.note_added_variable(eplus, self.objective)
                z_row.set_variable(eminus, sw_coeff)
                self.note_added_variable(eminus, self.objective)

                self.insert_error_var(cn, eminus)
                self.insert_error_var(cn, eplus)

                if cn.is_stay_constraint:
                    self.stay_error_vars.append((eplus, eminus))
                elif cn.is_edit_constraint:
                    prev_edit_constant = cn.expression.constant

        # print 'new_expression returning:', expr
        if expr.constant < 0:
            expr.multiply(-1.0)
        return expr, eplus, eminus, prev_edit_constant

    def add_constraint(self, cn):
        # print 'add_constraint', cn
        expr, eplus, eminus, prev_edit_constant = self.new_expression(cn)

        if not self.try_adding_directly(expr):
            self.add_with_artificial_variable(expr)

        self.needs_solving = True

        if cn.is_edit_constraint:
            i = len(self.edit_var_map)

            self.edit_var_map[cn.variable] = EditInfo(cn, eplus, eminus, prev_edit_constant, i)

        if self.auto_solve:
            self.optimize(self.objective)
            self.set_external_variables()

        return cn

    def add_constraint_no_exception(self, cn):
        try:
            self.add_constraint(cn)
            return True
        except RequiredFailure:
            return False

    def add_edit_var(self, v, strength=STRONG):
        # print "add_edit_var", v, strength
        self.add_constraint(EditConstraint(v, strength))

    def remove_edit_var(self, v):
        self.remove_constraint(self.edit_var_map[v].constraint)

    def begin_edit(self):
        assert len(self.edit_var_map) > 0
        self.infeasible_rows.clear()
        self.reset_stay_constants()
        self.edit_variable_stack.append(len(self.edit_var_map))

    def end_edit(self):
        assert len(self.edit_var_map) > 0
        self.resolve()
        self.edit_variable_stack.pop()
        self.remove_edit_vars_to(self.edit_variable_stack[-1])

    def remove_all_edit_vars(self):
        self.remove_edit_vars_to(0)

    def remove_edit_vars_to(self, n):
        try:
            for v, cei in self.edit_var_map.items():
                if cei.index >= n:
                    self.remove_edit_var(v)

            assert len(self.edit_var_map) == n

        except ConstraintNotFound:
            raise InternalError('Constraint not found during internal removal')

    def add_point_stays(self, points):
        # print "add_point_stays", points
        weight = 1.0
        multiplier = 2.0
        for i, point in enumerate(points):
            self.add_stay(point.x, WEAK, weight)
            self.add_stay(point.y, WEAK, weight)
            weight = weight * multiplier

    def add_stay(self, v, strength=WEAK, weight=1.0):
        self.add_constraint(StayConstraint(v, strength, weight))

    def remove_constraint(self, cn):
        # print "removeConstraint", cn
        # print self
        self.needs_solving = True
        self.reset_stay_constants()
        z_row = self.rows[self.objective]

        e_vars = self.error_vars.get(cn)
        # print "e_vars ==", e_vars
        if e_vars:
            for cv in e_vars:
                try:
                    z_row.add_expression(self.rows[cv], -cn.weight * cn.strength, self.objective, self)
                    # print 'add expression', self.rows[cv]
                except KeyError:
                    z_row.add_variable(cv, -cn.weight * cn.strength, self.objective, self)
                    # print 'add variable', cv

        try:
            marker = self.marker_vars.pop(cn)
        except KeyError:
            raise ConstraintNotFound()

        # print "Looking to remove var", marker
        if not self.rows.get(marker):
            col = self.columns[marker]
            # print "Must pivot -- columns are", col
            exit_var = None
            min_ratio = 0.0
            for v in col:
                # print 'check var', v
                if v.is_restricted:
                    # print 'var', v, ' is restricted'
                    expr = self.rows[v]
                    coeff = expr.coefficient_for(marker)
                    # print "Marker", marker, "'s coefficient in", expr, "is", coeff
                    if coeff < 0:
                        r = -expr.constant / coeff
                        if exit_var is None or r < min_ratio: # EXTRA BITS IN JS?
                            # print 'set exit var = ',v,r
                            min_ratio = r
                            exit_var = v

            if exit_var is None:
                # print "exit_var is still None"
                for v in col:
                    # print 'check var', v
                    if v.is_restricted:
                        # print 'var', v, ' is restricted'
                        expr = self.rows[v]
                        coeff = expr.coefficient_for(marker)
                        # print "Marker", marker, "'s coefficient in", expr, "is", coeff
                        r = expr.constant / coeff
                        if exit_var is None or r < min_ratio:
                            # print 'set exit var = ',v,r
                            min_ratio = r
                            exit_var = v

            if exit_var is None:
                # print "exit_var is still None (again)"
                if len(col) == 0:
                    # print 'remove column',marker
                    self.remove_column(marker)
                else:
                    exit_var = [v for v in col if v != self.objective][-1] # ??
                    # print 'set exit var', exit_var

            if exit_var is not None:
                # print 'Pivot', marker, exit_var,
                self.pivot(marker, exit_var)

        if self.rows.get(marker):
            # print 'remove row', marker
            expr = self.remove_row(marker)

        if e_vars:
            # print 'e_vars exist'
            for v in e_vars:
                if v != marker:
                    # print 'remove column',v
                    self.remove_column(v)

        if cn.is_stay_constraint:
            if e_vars:
                # for p_evar, m_evar in self.stay_error_vars:
                remaining = []
                while self.stay_error_vars:
                    p_evar, m_evar = self.stay_error_vars.pop()
                    found = False
                    try:
                        # print 'stay constraint - remove plus evar', p_evar
                        e_vars.remove(p_evar)
                        found = True
                    except KeyError:
                        pass
                    try:
                        # print 'stay constraint - remove minus evar', m_evar
                        e_vars.remove(m_evar)
                        found = True
                    except KeyError:
                        pass
                    if not found:
                        remaining.append((p_evar, m_evar))
                self.stay_error_vars = remaining

        elif cn.is_edit_constraint:
            assert e_vars is not None
            # print 'edit constraint - remove column', self.edit_var_map[cn.variable].edit_minus
            self.remove_column(self.edit_var_map[cn.variable].edit_minus)
            del self.edit_var_map[cn.variable]

        if e_vars:
            for e_var in e_vars:
                # print 'Remove error var', e_var
                del self.error_vars[e_var]

        if self.auto_solve:
            # print 'final auto solve'
            self.optimize(self.objective)
            self.set_external_variables()

    def resolve_array(self, new_edit_constants):
        for v, cei in self.edit_var_map.items():
            self.suggest_value(v, new_edit_constants[cei.index])

        self.resolve()

    def resolve_pair(self, x, y):
        self.suggest_value(self.edit_var_list[0], x)
        self.suggest_value(self.edit_var_list[1], y)
        self.resolve()

    def resolve(self):
        self.dual_optimize()
        self.set_external_variables()
        self.infeasible_rows.clear()
        self.reset_stay_constants()

    def suggest_value(self, v, x):
        cei = self.edit_var_map.get(v)
        if not cei:
            raise InternalError("suggestValue for variable " + v + ", but var is not an edit variable")
        # print cei
        delta = x - cei.prev_edit_constant
        cei.prev_edit_constant = x
        self.delta_edit_constant(delta, cei.edit_plus, cei.edit_minus)

    def solve(self):
        if self.needs_solving:
            self.optimize(self.objective)
            self.set_external_variables()

    def set_edited_value(self, v, n):
        if v not in self.columns or v not in self.rows:
            v.value = n

        if not approx_equal(n, v.value):
            self.add_edit_var(v)
            self.begin_edit()

            self.suggest_value(v, n)

            self.end_edit()

    def add_var(self, v):
        if v not in self.columns or v not in self.rows:
            self.add_stay(v)

    def add_with_artificial_variable(self, expr):
        # print "add_with_artificial_variable", expr
        self.artificial_counter = self.artificial_counter + 1
        av = SlackVariable(number=self.artificial_counter, prefix='a')
        az = ObjectiveVariable('az')
        az_row = expr.clone()
        # print 'Before add_rows'
        # print self
        self.add_row(az, az_row)
        self.add_row(av, expr)
        # print 'after add_rows'
        # print self
        self.optimize(az)
        az_tableau_row = self.rows[az]
        # print "azTableauRow.constant =", az_tableau_row.constant
        if not approx_equal(az_tableau_row.constant, 0.0):
            self.remove_row(az)
            self.remove_column(av)
            raise RequiredFailure()

        e = self.rows.get(av)
        if e != None:
            if e.is_constant:
                self.remove_row(av)
                self.remove_row(az)
                return
            entry_var = e.any_pivotable_variable()
            self.pivot(entry_var, av)

        assert av not in self.rows
        self.remove_column(av)
        self.remove_row(az)

    def try_adding_directly(self, expr):
        # print "try_adding_directly", expr
        subject = self.choose_subject(expr)
        if subject is None:
            # print "try_adding_directly returning: False"
            return False

        expr.new_subject(subject)
        if subject in self.columns:
            self.substitute_out(subject, expr)

        self.add_row(subject, expr)
        # print "try_adding_directly returning: True"
        return True

    def choose_subject(self, expr):
        # print 'choose_subject', expr
        subject = None
        found_unrestricted = False
        found_new_restricted = False

        retval_found = False
        retval = None
        for v, c in expr.terms.items(): # CHECK??
            if found_unrestricted:
                if not v.is_restricted:
                    if v not in self.columns:
                        retval_found = True
                        retval = v
                        break
            else:
                if v.is_restricted:
                    if not found_new_restricted and not v.is_dummy and c < 0:
                        col = self.columns.get(v)
                        if col == None or (len(col) == 1 and self.objective in self.columns):
                            subject = v
                            found_new_restricted = True
                else:
                    subject = v
                    found_unrestricted = True

        if retval_found:
            return retval

        if subject:
            return subject

        coeff = 0.0
        for v, c in expr.terms.items():
            if not v.is_dummy:
                retval_found = True
                retval = None
                break
            if not v in self.columns:
                subject = v
                coeff = c

        if retval_found:
            return retval

        if not approx_equal(expr.constant, 0.0):
            raise RequiredFailure()

        if coeff > 0:
            expr = expr * -1

        return subject

    def delta_edit_constant(self, delta, plus_error_var, minus_error_var):
        expr_plus = self.rows.get(plus_error_var)
        if expr_plus is not None:
            expr_plus.constant = expr_plus.constant + delta
            if expr_plus.constant < 0.0:
                self.infeasible_rows.add(plus_error_var)
            return

        expr_minus = self.rows.get(minus_error_var)
        if expr_minus is not None:
            expr_minus.constant = expr_minus.constant - delta
            if expr_minus.constant < 0:
                self.infeasible_rows.add(minus_error_var)
            return

        try:
            for basic_var in self.columns[minus_error_var]:
                expr = self.rows[basic_var]
                c = expr.coefficient_for(minus_error_var)
                expr.constant = expr.constant + (c * delta)
                if basic_var.is_restricted and expr.constant < 0:
                    self.infeasible_rows.add(basic_var)
        except KeyError:
            pass

    def dual_optimize(self):
        z_row = self.rows.get(self.objective)
        while self.infeasible_rows:
            exit_var = self.infeasible_rows.pop(0)
            entry_var = None
            expr = self.rows.get(exit_var)
            if expr:
                if expr.constant < 0:
                    ratio = float('inf')
                    for v, cd in expr.terms.items():
                        if cd > 0 and v.is_pivotable:
                            zc = z_row.coefficient_for(v)
                            r = zc / cd
                            if r < ratio: # JS difference?
                                entry_var = v
                                ratio = r
                    if ratio == float('inf'):
                        raise InternalError("ratio == nil (MAX_VALUE) in dual_optimize")
                    self.pivot(entry_var, exit_var)

    def optimize(self, z_var):
        # print "optimize", z_var
        # print self
        self.optimize_count = self.optimize_count + 1

        z_row = self.rows[z_var]
        entry_var = None
        exit_var = None

        # print self.objective
        # print z_var
        # print self.rows[self.objective]
        # print self.rows[z_var]

        while True:
            objective_coeff = 0.0

            for v, c in z_row.terms.items():
                # print v, v.is_pivotable, c
                if v.is_pivotable and c < objective_coeff:
                    objective_coeff = c
                    entry_var = v

            if objective_coeff >= -EPSILON or entry_var is None:
                return

            # print 'entry_var:', entry_var
            # print "objective_coeff:", objective_coeff

            min_ratio = float('inf')
            r = 0

            for v in self.columns[entry_var]:
                # print "checking", v
                if v.is_pivotable:
                    expr = self.rows[v]
                    coeff = expr.coefficient_for(entry_var)
                    # print 'pivotable, coeff =', coeff
                    if coeff < 0:
                        r = -expr.constant / coeff
                        if r < min_ratio:
                            min_ratio = r
                            exit_var = v

            if min_ratio == float('inf'):
                raise RequiredFailure('Objective function is unbounded')

            self.pivot(entry_var, exit_var)

            # print self

    def pivot(self, entry_var, exit_var):
        # print 'pivot:',entry_var, exit_var
        if entry_var is None:
            print "WARN - entry_var is None"
        if exit_var is None:
            print "WARN - exit_var is None"

        p_expr = self.remove_row(exit_var)
        p_expr.change_subject(exit_var, entry_var)
        self.substitute_out(entry_var, p_expr)
        self.add_row(entry_var, p_expr)

    def reset_stay_constants(self):
        # print "reset_stay_constants"
        for p_var, m_var in self.stay_error_vars:
            expr = self.rows.get(p_var)
            if expr is None:
                expr = self.rows.get(m_var)
            if expr:
                expr.constant = 0.0

    def set_external_variables(self):
        # print "set_external_variables"
        # print self
        for v in self.external_parametric_vars:
            if self.rows.get(v):
                # print "Variable %s in external_parametric_vars is basic" % v
                continue
            v.value = 0.0

        for v in self.external_rows:
            expr = self.rows[v]
            v.value = expr.constant

        self.needs_solving = False

    def insert_error_var(self, cn, var):
        # print 'insert_error_var', cn, var
        constraint_set = self.error_vars.get(var)
        if not constraint_set:
            constraint_set = set()
            self.error_vars[cn] = constraint_set

        constraint_set.add(var)

        self.error_vars.setdefault(var, set()).add(var)
