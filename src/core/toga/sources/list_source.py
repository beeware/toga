from .collection_source import CollectionSource


class ListSource(CollectionSource):
    """A data source to store a list of multiple data values, in a row-like fashion.

    Support random access, inserting and deleting.
    """

    ######################################################################
    # Utility methods to make ListSources more list-like
    ######################################################################

    def __setitem__(self, index, value):
        row = CollectionSource.create_row(data=value, accessors=self._accessors, source=self)
        self._data[index] = row
        self._notify('insert', index=index, item=row)

    def insert(self, index, *values, **named):
        # Coalesce values and data into a single data dictionary,
        # and use that to create the data row. Explicitly named data override.
        row = CollectionSource.create_row(
            data=dict(zip(self._accessors, values), **named),
            accessors=self._accessors,
            source=self,
        )
        self._data.insert(index, row)
        self._notify('insert', index=index, item=row)
        return row

    def prepend(self, *values, **named):
        return self.insert(0, *values, **named)

    def append(self, *values, **named):
        return self.insert(len(self), *values, **named)

    def remove(self, row):
        i = self._data.index(row)
        del self._data[i]
        self._notify('remove', index=i, item=row)
        return row
