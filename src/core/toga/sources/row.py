
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

    @classmethod
    def create_row(cls, data, accessors, source=None):
        """Create a Row object from the given data.
        Args:
            data (any): The type of `data` determines how it is handled
                ``dict``: each key corresponds to a column accessor
                iterables, except ``str`` and ``dict``: each item corresponds to a column
                all else: `data` will fill the first column
            accessors (`list`): A list of attribute names for accessing the value
                in each column of the row.
            source (any): A source to attach to the row
        """

        if isinstance(data, dict):
            row = Row(**data)
        elif hasattr(data, '__iter__') and not isinstance(data, str):
            row = Row(**dict(zip(accessors, data)))
        else:
            row = Row(**{accessors[0]: data})
        if source is not None:
            row._source = source
        return row
