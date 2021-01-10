from toga.platform import get_platform_factory

class Clipboard():

    def __init__(self, factory=None):
        self.factory = get_platform_factory(factory)
        self._impl = getattr(self.factory, self._CLIPBOARD_CLASS)(interface=self)

    def get_clipdata(self):
        pass

    def set_clipdata(self):
        pass
