from collections.abc import Sequence


class ImmutableList:
    def __init__(self, iterable):
        self._data = list(iterable)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __eq__(self, other):
        return self._data == other

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __reversed__(self):
        return reversed(self._data)

    def index(self, value):
        return self._data.index(value)

    def count(self, value):
        return self._data.count(value)


Sequence.register(ImmutableList)
