from android.content import Context
from androidx.appcompat import R as appcompat_R

from .dialogs import DialogsMixin
from .probe import BaseProbe


class WindowProbe(BaseProbe, DialogsMixin):
    supports_fullscreen = True
    supports_presentation = True

    def __init__(self, app, window):
        super().__init__(app)
        self.native = self.app._impl.native
        self.window = window
        self.impl = self.window._impl

    async def wait_for_window(
        self,
        message,
        minimize=False,
        full_screen=False,
        state_switch_not_from_normal=False,
    ):
        await self.redraw(
            message,
            delay=(0.5 if (full_screen or state_switch_not_from_normal) else 0.1),
        )

    @property
    def content_size(self):
        return (
            self.root_view.getWidth() / self.scale_factor,
            self.root_view.getHeight() / self.scale_factor,
        )

    @property
    def top_bar_height(self):
        # Android doesn't require explicit allowances for the top bar in content layout;
        # the size of the top bar is the difference between the screen and the root
        # window content size.
        context = self.app._impl.native.getApplicationContext()
        window_manager = context.getSystemService(Context.WINDOW_SERVICE)
        display = window_manager.getDefaultDisplay()
        return (display.getHeight() - self.root_view.getHeight()) / self.scale_factor

    def _native_menu(self):
        return self.native.findViewById(appcompat_R.id.action_bar).getMenu()

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    def _toolbar_items(self):
        result = []
        prev_group = None
        menu = self._native_menu()
        for i_item in range(menu.size()):
            item = menu.getItem(i_item)
            assert not item.requestsActionButton()

            if item.requiresActionButton():
                if prev_group and prev_group != item.getGroupId():
                    # The separator doesn't actually appear, but it keeps the indices
                    # correct for the tests.
                    result.append(None)
                prev_group = item.getGroupId()
                result.append(item)

        return result

    def has_toolbar(self):
        return bool(self._toolbar_items())

    def assert_is_toolbar_separator(self, index, section=False):
        assert self._toolbar_items()[index] is None

    def assert_toolbar_item(self, index, label, tooltip, has_icon, enabled):
        item = self._toolbar_items()[index]
        assert item.getTitle() == label
        # Tooltips are not implemented
        assert (item.getIcon() is not None) == has_icon
        assert item.isEnabled() == enabled

    def press_toolbar_button(self, index):
        self.native.onOptionsItemSelected(self._toolbar_items()[index])
