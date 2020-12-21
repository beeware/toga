
class Row:
    def __init__(self, **data):
        self._attrs = list(data.keys())
        self._source = None
        for name, value in data.items():
            setattr(self, name, value)

    ######################################################################
    # Utility wrappers
    ######################################################################

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if attr in self._attrs and self._source is not None:
            self._source._notify('change', item=self)

    def __eq__(self, other):
        if not isinstance(other, Row):
            return False
        return self.as_dict() == other.as_dict()

    def __hash__(self):
        return hash(frozenset(self.as_dict().items()))

    def __repr__(self):
        return "[Row: {}]".format(self.as_dict())

    def as_dict(self):
        return {attr: getattr(self, attr) for attr in self._attrs}
