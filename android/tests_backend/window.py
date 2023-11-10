import pytest
from androidx.appcompat import R as appcompat_R

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    def __init__(self, app, window):
        super().__init__(app)
        self.native = self.app._impl.native

    async def wait_for_window(self, message, minimize=False, full_screen=False):
        await self.redraw(message)

    @property
    def content_size(self):
        return (
            self.root_view.getWidth() / self.scale_factor,
            self.root_view.getHeight() / self.scale_factor,
        )

    async def close_info_dialog(self, dialog):
        dialog_view = self.get_dialog_view()
        self.assert_dialog_buttons(dialog_view, ["OK"])
        await self.press_dialog_button(dialog_view, "OK")

    async def close_question_dialog(self, dialog, result):
        dialog_view = self.get_dialog_view()
        self.assert_dialog_buttons(dialog_view, ["No", "Yes"])
        await self.press_dialog_button(dialog_view, "Yes" if result else "No")

    async def close_confirm_dialog(self, dialog, result):
        dialog_view = self.get_dialog_view()
        self.assert_dialog_buttons(dialog_view, ["Cancel", "OK"])
        await self.press_dialog_button(dialog_view, "OK" if result else "Cancel")

    async def close_error_dialog(self, dialog):
        dialog_view = self.get_dialog_view()
        self.assert_dialog_buttons(dialog_view, ["OK"])
        await self.press_dialog_button(dialog_view, "OK")

    async def close_stack_trace_dialog(self, dialog, result):
        pytest.skip("Stack Trace dialog not implemented on Android")

    async def close_save_file_dialog(self, dialog, result):
        pytest.skip("Save File dialog not implemented on Android")

    async def close_open_file_dialog(self, dialog, result, multiple_select):
        pytest.skip("Open File dialog not implemented on Android")

    async def close_select_folder_dialog(self, dialog, result, multiple_select):
        pytest.skip("Select Folder dialog not implemented on Android")

    def _native_menu(self):
        return self.native.findViewById(appcompat_R.id.action_bar).getMenu()

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
