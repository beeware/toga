import re


NON_ACCESSOR_CHARS = re.compile('[^\w ]')
WHITESPACE = re.compile('\s+')

def to_accessor(heading):
    """Convert a human-readable heading into a data attribute accessor

    This won't be infallible; for ambiguous cases, you'll need to manually
    specify the accessors.

    Examples:
        'Heading 1' -> 'heading_1'
        'Heading - Title' -> 'heading_title'
        'Heading!' -> 'heading'

    Args:
        heading (``str``): The column heading.

    Returns:
        the accessor derived from the heading.
    """
    value = WHITESPACE.sub(
        ' ',
        NON_ACCESSOR_CHARS.sub('', heading.lower()),
    ).replace(' ', '_')

    if len(value) == 0 or value[0].isdigit():
        raise ValueError("Unable to automatically generate accessor from heading '{}'.".format(heading))

    return value

def build_accessors(headings, accessors):
    """Convert a list of headings (with accessor overrides) to a finalised list of accessors.

    Args:
        headings: a list of strings to be used as headings
        accessors: the accessor overrides. Can be:
         - A list, same length as headings. Each entry is
           a string providing the override name for the accessor,
           or None, indicating the default accessor should be used.
         - A dictionary from the heading names to the accessor. If
           a heading name isn't present in the dictonary, the default
           accessor will be used
         - Otherwise, a final list of ready-to-use accessors.

    Returns:
        A finalized list of accessors.

    """
    if accessors:
        if isinstance(accessors, dict):
            result = [
                accessors[h] if h in accessors else to_accessor(h)
                for h in headings
            ]
        else:
            if len(headings) != len(accessors):
                raise ValueError('Number of accessors must match number of headings')

            result = [
                a if a is not None else to_accessor(h)
                for h, a in zip(headings, accessors)
            ]
    else:
        result = [to_accessor(h) for h in headings]

    if len(result) != len(set(result)):
        raise ValueError('Data accessors are not unique.')

    return result


class Value:
    def __init__(self, source, value=None, icon=None, **data):
        self._source = None
        self.value = value
        self.icon = icon
        for name, val in data.items():
            setattr(self, name, val)
        self._source = source

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
            if self._source is not None:
                self._source._notify('data_changed')


class Row:
    def __init__(self, source, **data):
        self._source = None
        for name, value in data.items():
            setattr(self, name, value)
        self._source = source

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if not attr.startswith('_'):
            if self._source is not None:
                self._source._notify('data_changed')


class Node(Row):
    def __init__(self, source, **data):
        super().__init__(source, **data)
        self._children = None
        self._parent = None

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, value):
        self._children[index] = self._source._create_node(value)
        self._source._notify('data_changed')

    def __len__(self):
        if self._children is None:
            return 0
        else:
            return len(self._children)

    def __iter__(self):
        return iter(self._children)

    def has_children(self):
        return self._children is not None

    def insert(self, index, *values, **named):
        self._source.insert(self, index, *values, **named)

    def prepend(self, *values, **named):
        self._source.prepend(self, *values, **named)

    def append(self, *values, **named):
        self._source.append(self, *values, **named)

    def remove(self, node):
        self._source.remove(self, node)


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
