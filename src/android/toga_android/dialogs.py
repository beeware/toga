from .libs.android_widgets import (
    AlertDialog__Builder,
    DialogInterface__OnClickListener
)


class NoOpListener(DialogInterface__OnClickListener):
    def onClick(self, dialog, which):
        pass


def info(window, title, message):
    builder = AlertDialog__Builder(window.app.native)
    builder.setTitle(title)
    builder.setMessage(message)
    builder.setPositiveButton("OK", NoOpListener())
    builder.show()


def question(window, title, message):
    window.platform.not_implemented("dialogs.question()")


def confirm(window, title, message):
    window.platform.not_implemented("dialogs.confirm()")


def error(window, title, message):
    window.platform.not_implemented("dialogs.error()")


def stack_trace(window, title, message, content, retry=False):
    window.platform.not_implemented("dialogs.stack_trace()")


def save_file(window, title, suggested_filename, file_types):
    window.platform.not_implemented("dialogs.save_file()")
