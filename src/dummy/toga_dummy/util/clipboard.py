class Clipboard():
    _clipdata = None  # store clipdata in this class

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def get_clipdata(self):
        return self._clipdata

    def set_clipdata(self, data):
        self._clipdata = data
