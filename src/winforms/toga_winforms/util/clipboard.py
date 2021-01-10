class Clipboard():

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def get_clipdata(self):
        pass

    def set_clipdata(self):
        pass
