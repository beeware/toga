from toga.platform import get_platform_factory


class Clipboard:
    # all data types that are currently supported
    data_types = (
        "Text"
    )

    def __init__(self, factory=None):
        self.factory = get_platform_factory(factory)

        # Create a platform specific implementation of the clipboard
        self._impl = self.factory.Clipboard(interface=self)

    def get_clipdata(self, type):
        """
        Get the data currently stored in the clipboard

        :param str type: The data type of the data to get, must be a type listed in Clipboard.data_types
        :returns: The data from the clipboard or None
        """
        if type not in self.data_types:
            raise ValueError('unsupported data type')
        return self._impl.get_clipdata(type)

    def set_clipdata(self, data):
        """
        Put data into the clipboard

        :param data: The data to put into the clipboard. Use None to clear the clipboard
        """
        self._impl.set_clipdata(data)
