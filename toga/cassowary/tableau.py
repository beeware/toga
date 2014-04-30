
class Tableau(object):
    def __init__(self):
        # Map of variable to set of variables
        self.columns = {}

        # Map of variable to LinearExpression
        self.rows = {}

        # Set of Variables
        self.infeasible_rows = set()

        # Set of Variables
        self.external_rows = set()

        # Set of Variables.
        self.external_parametric_vars = set()

    def __repr__(self):
        parts = []
        parts.append('Tableau info:')
        parts.append('Rows: %s (= %s constraints)' % (len(self.rows), len(self.rows) - 1))
        parts.append('Columns: %s' % len(self.columns))
        parts.append('Infeasible rows: %s' % len(self.infeasible_rows))
        parts.append('External basic variables: %s' % len(self.external_rows))
        parts.append('External parametric variables: %s' % len(self.external_parametric_vars))
        return '\n'.join(parts)

    def note_removed_variable(self, var, subject):
        if subject:
            self.columns[var].remove(subject)

    def note_added_variable(self, var, subject):
        if subject:
            self.columns.setdefault(var, set()).add(subject)

    def add_row(self, var, expr):
        # print 'add_row', var, expr
        self.rows[var] = expr

        for clv in expr.terms:
            self.columns.setdefault(clv, set()).add(var)
            if clv.is_external:
                self.external_parametric_vars.add(clv)

        if var.is_external:
            self.external_rows.add(var)

        # print self

    def remove_column(self, var):
        rows = self.columns.pop(var)

        if rows:
            for clv in rows:
                expr = self.rows[clv]
                expr.remove_variable(var)

        if var.is_external:
            try:
                self.external_rows.remove(var)
            except KeyError:
                pass

            try:
                self.external_parametric_vars.remove(var)
            except KeyError:
                pass

    def remove_row(self, var):
        # print "remove_row", var
        expr = self.rows.pop(var)

        for clv in expr.terms.keys():
            varset = self.columns[clv]
            if varset:
                # print "removing from varset", var
                varset.remove(var)

        try:
            self.infeasible_rows.remove(var)
        except KeyError:
            pass
        if var.is_external:
            try:
                self.external_rows.remove(var)
            except KeyError:
                pass
        # print "remove_row returning", expr
        return expr

    def substitute_out(self, oldVar, expr):
        varset = self.columns[oldVar]
        for v in varset:
            row = self.rows[v]
            row.substitute_out(oldVar, expr, v, self)
            if v.is_restricted and row.constant < 0.0:
                self.infeasible_rows.add(v)

        if oldVar.is_external:
            self.external_rows.add(oldVar)
            try:
                self.external_parametric_vars.remove(oldVar)
            except KeyError:
                pass

        del self.columns[oldVar]
