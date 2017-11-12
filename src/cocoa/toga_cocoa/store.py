from .libs import *


class Store:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.app_id = self.interface.app.app_id
        print('app_id', self.app_id)
        # self.native = NSUserDefaults.initWithSuiteName = self.app_id
        self.native = NSUserDefaults.standardUserDefaults

    def get(self, key: str):
        return self.native.stringForKey_(key)

    def set(self, key: str, value: str):
        self.native.setObject_forKey_(value, key)

    def remove(self, key: str):
        self.native.removeObjectForKey_(key)

    def clear(self):
        pass
