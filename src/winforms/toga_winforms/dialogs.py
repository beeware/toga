from .libs import WinForms


def info(window, title, message):
    WinForms.MessageBox.Show(message, title)


def question(window, title, message):
    result = WinForms.MessageBox.Show(message, title, WinForms.MessageBoxButtons.YesNo)
    return result == WinForms.DialogResult.Yes


def confirm(window, title, message):
    result = WinForms.MessageBox.Show(message, title, WinForms.MessageBoxButtons.OKCancel)
    return result == WinForms.DialogResult.OK


def error(window, title, message):
    WinForms.MessageBox.Show(message, title, WinForms.MessageBoxButtons.OK, WinForms.MessageBoxIcon.Error)


def stack_trace(window, title, message, content, retry=False):
    window.platform.not_implemented('Dialog.set_enabled()')


def save_file(window, title, suggested_filename, file_types):
    window.platform.not_implemented('Dialog.set_enabled()')
