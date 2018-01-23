

class TogaAlertDialogBuilder(extends=android.app.AlertDialog[Builder]):
    @super({context: android.content.Context})
    def __init__(self, context, message):
        self.setMessage(message)


def info(window, title, message):
    builder = TogaAlertDialogBuilder(window.app._impl, message)
    builder.setPositiveButton("OK", None)
    dialog = builder.create()
    dialog.show()


def question(window, title, message):
    window.platform.not_implemented('dialogs.question()')


def confirm(window, title, message):
    window.platform.not_implemented('dialogs.confirm()')


def error(window, title, message):
    window.platform.not_implemented('dialogs.error()')


def stack_trace(window, title, message, content, retry=False):
    window.platform.not_implemented('dialogs.stack_trace()')


def save_file(window, title, suggested_filename, file_types):
    window.platform.not_implemented('dialogs.save_file()')

