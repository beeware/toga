def info(window, title, message, button_label='OK'):
    raise NotImplementedError()


def question(window, title, message, button_label=('Yes', 'No')):
    raise NotImplementedError()


def confirm(window, title, message, button_label=('OK', 'Cancel')):
    raise NotImplementedError()


def error(window, title, message, button_label='OK'):
    raise NotImplementedError()


def stack_trace(window, title, message, content, retry=False,
                                            button_label=('Retry', 'Cancel')):
    raise NotImplementedError()


def save_file(window, title, suggested_filename, file_types):
    raise NotImplementedError()
