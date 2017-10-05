

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
    # TODO
    raise NotImplementedError()


def confirm(window, title, message):
    # TODO
    raise NotImplementedError()


def error(window, title, message):
    # TODO
    raise NotImplementedError()


def stack_trace(window, title, message, content, retry=False):
    # TODO
    raise NotImplementedError()


def save_file(window, title, suggested_filename, file_types):
    # TODO
    raise NotImplementedError()
