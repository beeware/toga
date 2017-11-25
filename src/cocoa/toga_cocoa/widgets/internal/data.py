from rubicon.objc import *


class TogaData(NSObject):
    @objc_method
    def copyWithZone_(self):
        copy = TogaData.alloc().init()
        copy.attrs = self.attrs
        return copy
