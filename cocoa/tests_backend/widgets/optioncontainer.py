from rubicon.objc import SEL, send_message

from toga_cocoa.libs import NSTabView

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = NSTabView
    max_tabs = None
    disabled_tab_selectable = False

    def assert_supports_content_based_rehint(self):
        pass

    @property
    def width(self):
        return self.native.alignmentRectForFrame(self.native.frame).size.width

    @property
    def height(self):
        return self.native.alignmentRectForFrame(self.native.frame).size.height

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
