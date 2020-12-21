from .collection_source import CollectionSource
from .row import Row


class StackSource(CollectionSource):
    """A data source to store a stack of multiple data values, in a row-like fashion.

    Support pushing and popping rows and uniqueness
    """

    def __init__(self, accessors, unique=True, size=None):
        super(StackSource, self).__init__(data=[], accessors=accessors)
        self.unique = unique
        self.size = size

    def push(self, *values, **named):
        row = CollectionSource.create_row(
            data=dict(zip(self._accessors, values), **named),
            accessors=self._accessors,
            source=self,
        )
        if self.unique:
            try:
                existing_index = self.index(row)
                del self[existing_index]
            except ValueError:
                pass
        self._data.insert(0, row)
        self._notify('push', item=row)
        if self.size is not None:
            while len(self) > self.size:
                self.pop()
        return row

    def pop(self, ):
        row = self._data[-1]
        del self[-1]
        self._notify('pop', item=row)
        return row
