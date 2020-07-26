import asyncio

from .libs.android_widgets import (
    AlertDialog__Builder,
    DialogInterface__OnClickListener,
    R__drawable,
)


class OnClickListener(DialogInterface__OnClickListener):
    def __init__(self, fn=None):
        super().__init__()
        self._fn = fn

    def onClick(self, _dialog, _which):
        if self._fn:
            self._fn()


async def _dialog(window, title, message, positive_text, negative_text, icon):
    '''Create Android textual dialog. Parameters:
    - window: Toga Window
    - title: Title of dialog
    - message: Message of dialog
    - positive_text: Button label where clicking it returns True (or None to skip)
    - negative_text: Button label where clicking it returns False (or None to skip)
    - icon: Integer used as an Android resource ID number for dialog icon (or None to skip)'''
    builder = AlertDialog__Builder(window.app.native)
    builder.setCancelable(False)
    builder.setTitle(title)
    builder.setMessage(message)
    if icon is not None:
        builder.setIcon(icon)
    result_future = asyncio.Future()
    if positive_text is not None:
        builder.setPositiveButton(positive_text, OnClickListener(lambda: result_future.set_result(True)))
    if negative_text is not None:
        builder.setNegativeButton(negative_text, OnClickListener(lambda: result_future.set_result(False)))
    builder.show()
    return await result_future


async def info(window, title, message):
    await _dialog(window, title, message, "OK", None, None)


async def question(window, title, message):
    return await _dialog(window, title, message, "Yes", "No", None)


async def confirm(window, title, message):
    return await _dialog(window, title, message, "OK", "Cancel", None)


async def error(window, title, message):
    return await _dialog(window, title, message, "OK", None, R__drawable.ic_dialog_alert)


def stack_trace(window, title, message, content, retry=False):
    window.platform.not_implemented("dialogs.stack_trace()")


def save_file(window, title, suggested_filename, file_types):
    window.platform.not_implemented("dialogs.save_file()")
