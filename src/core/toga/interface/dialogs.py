def info(window, title, message):
    raise NotImplementedError()


def question(window, title, message):
    raise NotImplementedError()


def confirm(window, title, message):
    raise NotImplementedError()


def error(window, title, message):
    raise NotImplementedError()


def stack_trace(window, title, message, content, retry=False):
    raise NotImplementedError()


def save_file(window, title, suggested_filename, file_types):
    raise NotImplementedError()
