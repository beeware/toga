from toga_cocoa.libs import NSObject, objc_method


class TogaData(NSObject):
    @objc_method
    def copyWithZone_(self):
        # TogaData is used as an immutable reference to a row
        # so the same object can be returned as a copy.
        self.retain()
        return self
