

class Value:
    def __init__(self, source, value=None, icon=None, **data):
        self._source = source
        self.value = value
        self.icon = icon
        for name, val in data.items():
            setattr(self, name, val)

    def __str__(self):
        if self.value is None:
            return ''
        return str(self.value)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, path_or_icon):
        from toga import Icon
        if path_or_icon:
            self._icon = Icon.load(path_or_icon)
        else:
            self._icon = None

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if not attr.startswith('_'):
            self._source._notify('data_changed')


class Row:
    def __init__(self, source, **data):
        self._source = source
        for name, value in data.items():
            setattr(self, name, value)

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if not attr.startswith('_'):
            self._source._notify('data_changed')


class Node(Row):
    def __init__(self, source, **data):
        super().__init__(source, **data)
        self._children = None
        self.parent = None

    def __getitem__(self, index):
        return self._children[index]

    def __len__(self):
        if self._children is None:
            return 0
        else:
            return len(self._children)

    def has_children(self):
        return self._children is not None


class Source:
    def __init__(self):
        self._listeners = []

    @property
    def listeners(self) -> list:
        """ The listeners of this data source.
        Listeners can be ``callable`` or :obj:``toga.Widget``.

        Returns:
            A list of objects that are listening for data change.
        """
        return self._listeners

    def add_listener(self, listener):
        """
        Args:
            listener: ``callable`` or :obj:``toga.Widget`
        """
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def _notify(self, notification, *args, **kwargs):
        """Invoke a notification function on all listeners that are subscribed to this data source."""
        for listener in self._listeners:
            getattr(listener, notification)(*args, **kwargs)


def to_accessor(heading):
    "Convert a human-readable heading into a data attribute accessor"
    return heading.lower().replace(' ', '_')
