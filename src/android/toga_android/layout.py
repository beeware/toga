
class TogaLayout:
    # TODO: Extend `android.view.ViewGroup`. Provide app as `context`.
    def __init__(self, context, interface):
        self.interface = interface

    def shouldDelayChildPressedState(self) -> bool:
        return False

    def onMeasure(self, width: int, height: int):
        # print("ON MEASURE %sx%s" % (width, height))
        self.measureChildren(width, height)
        self.interface.rehint()
        self.setMeasuredDimension(width, height)

    def onLayout(self, changed: bool, left: int, top: int, right: int, bottom: int) -> None:
        # print("ON LAYOUT %s %sx%s -> %sx%s" % (changed, left, top, right, bottom))
        device_scale = self.interface.app._impl.device_scale

        self.interface._update_layout(
            width=(right - left) / device_scale,
            height=(bottom - top) / device_scale,
        )
        self.interface.style.apply()

        count = self.getChildCount()
        # print("LAYOUT: There are %d children" % count)
        for i in range(0, count):
            child = self.getChildAt(i)
            # See "Size, padding and margins" at https://developer.android.com/reference/android/view/View
            # for reference information on `height`, `getMeasuredHeight()`, etc.
            child.layout(
                child.interface.layout.absolute.left * device_scale,
                child.interface.layout.absolute.top * device_scale,
                (child.interface.layout.absolute.left + child.interface.layout.width) * device_scale,
                (child.interface.layout.absolute.top + child.interface.layout.height) * device_scale,
            )

    # def onSizeChanged(self, left: int, top: int, right: int, bottom: int) -> void:
    #     print("ON SIZE CHANGE %sx%s -> %sx%s" % (left, top, right, bottom))

    #     count = self.getChildCount()
    #     print("CHANGE: There are %d children" % count)
    #     for i in range(0, count):
    #         child = self.getChildAt(i)
    #         print("    child: %s" % child)
