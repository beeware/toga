
class AbstractVariable(object):
    def __init__(self, name):
        self.name = name
        self.is_dummy = False
        self.is_external = False
        self.is_pivotable = False
        self.is_restricted = False

    def __repr__(self):
        return '%s:abstract' % self.name

class Variable(AbstractVariable):
    def __init__(self, name, value=0.0):
        super(Variable, self).__init__(name)
        self.value = value
        self.is_external = True

    def __repr__(self):
        return '%s:%s' % (self.name, self.value)


class DummyVariable(AbstractVariable):
    def __init__(self, number, prefix):
        super(DummyVariable, self).__init__(name='%s%s' % (prefix, number))
        self.is_dummy = True
        self.is_restricted = True

    def __repr__(self):
        return '%s:dummy' % self.name


class ObjectiveVariable(AbstractVariable):
    def __init__(self, name):
        super(ObjectiveVariable, self).__init__(name)

    def __repr__(self):
        return '%s:obj' % self.name


class SlackVariable(AbstractVariable):
    def __init__(self, number, prefix):
        super(SlackVariable, self).__init__(name='%s%s' % (prefix, number))
        self.is_pivotable = True
        self.is_restricted = True

    def __repr__(self):
        return '%s:slack' % self.name
