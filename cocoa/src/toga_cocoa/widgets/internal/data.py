from toga_cocoa.libs import NSObject, objc_method


class TogaData(NSObject):
    @objc_method
    def copyWithZone_(self):
        # TogaData is used as an immutable reference to a row
        # so the same object can be returned as a copy. We need
        # to manually `retain` the object before returning because
        # the "copy" methods are assumed to return an object that
        # is owned by the caller.
        self.retain()
        return self
