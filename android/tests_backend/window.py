import pytest

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    def __init__(self, app, window):
        super().__init__(app)

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
