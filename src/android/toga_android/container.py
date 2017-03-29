
class CSSLayout(extends=android.view.ViewGroup):
    @super({context: android.content.Context})
    def __init__(self, context, interface):
        self._interface = interface

    def shouldDelayChildPressedState(self) -> bool:
        return False

    def onMeasure(self, width: int, height: int) -> void:
        print("ON MEASURE %sx%s" % (width, height))
        self.measureChildren(width, height)
        self.setMeasuredDimension(width, height)

    def onLayout(self, changed: bool, left: int, top: int, right: int, bottom: int) -> void:
        print("ON LAYOUT %s %sx%s -> %sx%s" % (changed, left, top, right, bottom))

        self._interface._update_layout(
            width=right - left,
            height=bottom - top,
        )

        count = self.getChildCount()
        print("LAYOUT: There are %d children" % count)
        for i in range(0, count):
            child = self.getChildAt(i)
            print("    child: %s" % child, child.getMeasuredHeight(), child.getMeasuredWidth())
            print("    min child: %s" % child, child.getSuggestedMinimumHeight(), child.getSuggestedMinimumWidth())
            print("    layout: %s" % child, child._interface.layout)
            child.layout(
                child._interface.layout.top,
                child._interface.layout.left,
                child.getMeasuredWidth(),
                child.getMeasuredHeight()
            )

    # def onSizeChanged(self, left: int, top: int, right: int, bottom: int) -> void:
    #     print("ON SIZE CHANGE %sx%s -> %sx%s" % (left, top, right, bottom))

    #     count = self.getChildCount()
    #     print("CHANGE: There are %d children" % count)
    #     for i in range(0, count):
    #         child = self.getChildAt(i)
    #         print("    child: %s" % child)


class Container:
    def __init__(self):
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._impl = CSSLayout(widget.app._impl, widget)
        self._content = widget
        self._content._container = self

    @property
    def root_content(self):
        return self._content

    @root_content.setter
    def root_content(self, widget):
        self._impl = CSSLayout(widget.app._impl, widget)
        self._content = widget
        self._content._container = self

    def _update_layout(self, **style):
        if self._content:
            self._content._update_layout(**style)
