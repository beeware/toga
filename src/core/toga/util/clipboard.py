from toga.platform import get_platform_factory


class Clipboard:

    def __init__(self, factory=None):
        self.factory = get_platform_factory(factory)

        # Create a platform specific implementation of the clipboard
        self._impl = self.factory.Clipboard(interface=self)

    def get_clipdata(self):
        """
        Get the data currently stored in the clipboard

        :returns: The data from the clipboard
        """
        return self._impl.get_clipdata()

    def set_clipdata(self, data):
        """
        Put data into the clipboard

        param data: The data to put into the clipboard
        """
        self._impl.set_clipdata(data)
