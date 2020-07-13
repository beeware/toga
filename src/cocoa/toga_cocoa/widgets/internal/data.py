from toga_cocoa.libs import NSObject, objc_method


class TogaData(NSObject):
    @objc_method
    def copyWithZone_(self):
        copy = TogaData.alloc().init()
        copy.attrs = self.attrs
        return copy
