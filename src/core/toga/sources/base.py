

class Datum:
    def __init__(self, value=None, icon=None):
        self.value = value
        self.icon = icon

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


class Row:
    def __init__(self, **data):
        for name, value in data.items():
            setattr(self, name, value)


class Node(Row):
    def __init__(self, **data):
        super().__init__(**data)
        self.parent = None
        self._children = None

    def __len__(self):
        if self._children:
            return len(self._children)
        else:
            return 0

    def __getitem__(self, index):
        return self._children[index]


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
