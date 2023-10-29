from org.beeware.android import MainActivity


class Command:
    def __init__(self, interface):
        self.interface = interface
        self.native = []

    def set_enabled(self, value):
        MainActivity.singletonThis.invalidateOptionsMenu()
