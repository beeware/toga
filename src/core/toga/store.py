from .platform import get_platform_factory


class Store:
    """ Store is a unencrypted, persistent, key-value storage system.
    The key-value pairs are saved in a platform native way and are
    persisted over app launches.

    Examples:
        >>> store = toga.Store(app=app)
        >>> value = 'I want to save this'
        >>> store.set_item('my_key', value)
        >>> store.get_item('my_key')
        'I want to save this'
        >>> # Listen for changes
        >>> def my_callback(key, value):
        >>>     print(key, 'changed to', value)
        >>> store.add_listener('my_key', my_callback)
    """

    def __init__(self, app, factory=None):
        self.app = app
        self.factory = get_platform_factory(factory)
        self._keys = []
        self._listeners = {}
        self._impl = self.factory.Store(interface=self)

    def set_item(self, key: str, value: str):
        self._keys.append(str(key))
        self._impl.set(key, value)

    def get_item(self, key: str) -> str:
        return self._impl.get(key)

    def remove_item(self, key: str):
        self._keys.remove(str(key))
        self._impl.remove(str(key))

    @property
    def get_keys(self) -> list:
        return self._keys

    def clear(self):
        self._keys.clear()
        self._impl.clear()

    def add_listener(self, key: str, listener: callable):
        """ Add a function to be invoked when the value for the given key changes.

        Args:
            key: The key to listen to.
            listener: A function to be invoked on key value change.
        """
        if key in self._listeners.keys():
            self._listeners[key].append(listener)
        else:
            self._listeners[key] = [listener]
        self._impl.add_listener()

    def get_listener(self, key: str):
        """ The listeners of the given key.

        Returns:
            A list of ``callable`` which are invoked on value change.
        """
        self._listeners[key]

    def remove_listener(self, key: str, listener: callable):
        listeners = self._listeners[key]
        if listener in listeners:
            if len(listeners) <= 1:
                del self._listeners[key]
            else:
                listeners.remove(listener)
