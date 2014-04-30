
class EditInfo(object):
    def __init__(self, constraint, edit_plus, edit_minus, prev_edit_constant, index):
        self.constraint = constraint
        self.edit_plus = edit_plus
        self.edit_minus = edit_minus
        self.prev_edit_constant = prev_edit_constant
        self.index = index

    def __repr__(self):
        return u'<cn=%s ep=%s em=%s pec=%s index=%s>' % (
            self.constraint,
            self.edit_plus,
            self.edit_minus,
            self.prev_edit_constant,
            self.index
        )
