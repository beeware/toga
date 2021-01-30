from toga.platform import get_platform_factory


class Clipboard:

    def __init__(self, factory=None):
        self.factory = get_platform_factory(factory)

        # Create a platform specific implementation of the clipboard
        self._impl = self.factory.Clipboard(interface=self)

    def clear(self):
        """
        Clears the clipboard content
        """
        self._impl.clear()

    def get_text(self):
        """
        Get the text data currently stored in the clipboard

        :returns: The clipboard text data or None
        """
        return self._impl.get_text()

    def set_text(self, text):
        """
        Put text data into the clipboard

        :param text: The text to put into the clipboard. Use None to clear the clipboard
        """
        self._impl.set_text(text)
