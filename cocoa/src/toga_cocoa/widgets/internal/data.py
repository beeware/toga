from toga_cocoa.libs import NSObject, objc_method


class TogaData(NSObject):
    # This method is no-covered because different system APIs requiring
    # a native wrapper object may or may not choose to copy the native
    # objects involved; however, we should still preserve this method
    # as a defensive measure and not remove it from the codebase, as
    # future usages of a data object in native APIs may require copying.
    @objc_method
    def copyWithZone_(self):  # pragma: no cover
        # TogaData is used as an immutable reference to a row
        # so the same object can be returned as a copy. We need
        # to manually `retain` the object before returning because
        # the "copy" methods are assumed to return an object that
        # is owned by the caller.
        self.retain()
        return self
