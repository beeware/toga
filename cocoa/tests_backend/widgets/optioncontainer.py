from rubicon.objc import SEL, send_message

from toga_cocoa.libs import NSTabView

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = NSTabView
    max_tabs = None
    disabled_tab_selectable = False

    # 2023-06-20: This makes no sense, but here we are. If you render an NSTabView with
    # a size constraint of (300, 200), and then ask for the frame size of the native
    # widget, you get (314, 216).
    #
    # If you draw the widget at the origin of a window, the widget reports a frame
    # origin of (-7, -6).
    #
    # If you draw an NSTabView the full size of a 640x480 window, the box containing the
    # widget is 640x452, but the widget reports a frame of 654x458 @ (-7, -6).
    #
    # If you set the NSTabView to be 300x200, then draw a 300 px box below and a 200px
    # box beside the NSTabView to act as rulers, the rulers are the same size as the
    # NSTabView.
    #
    # I can't find any way to reverse engineer the magic left=7, right=7, top=6,
    # bottom=10 offsets from other properties of the NSTabView. So, we'll hard code them
    # and hope for the best.
    LEFT_OFFSET = 7
    RIGHT_OFFSET = 7
    TOP_OFFSET = 6
    BOTTOM_OFFSET = 10

    @property
    def width(self):
        return self.native.frame.size.width - self.LEFT_OFFSET - self.RIGHT_OFFSET

    @property
    def height(self):
        return self.native.frame.size.height - self.TOP_OFFSET - self.BOTTOM_OFFSET

    def select_tab(self, index):
        self.native.selectTabViewItemAtIndex(index)

    async def wait_for_tab(self, message):
        await self.redraw(message)

    def tab_enabled(self, index):
        # _isTabEnabled() is a hidden method, so the naming messes with Rubicon's
        # property lookup mechanism. Invoke it by passing the message directly.
        item = self.native.tabViewItemAtIndex(index)
        return send_message(item, SEL("_isTabEnabled"), restype=bool, argtypes=[])

    def assert_tab_icon(self, index, expected):
        # No tab icons, so if anything is returned, that's an error
        assert self.widget.content[index].icon is None
