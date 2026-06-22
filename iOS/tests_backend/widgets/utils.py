from rubicon.objc import NSObject, NSPoint, objc_method


# UITouch objects can't be instantiated; but we only care about 1 method, so
# create a mock that satisfies our needs.
class MockTouch(NSObject):
    @objc_method
    def locationInView(self, view) -> NSPoint:
        return self.position
