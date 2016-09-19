from gi.repository import Gtk


def info(window, title, message):
    dialog = Gtk.MessageDialog(window._impl, 0, Gtk.MessageType.INFO,
        Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(message)

    dialog.run()
    dialog.destroy()


def question(window, title, message):
    dialog = Gtk.MessageDialog(window._impl, 0, Gtk.MessageType.QUESTION,
        Gtk.ButtonsType.YES_NO, title)
    dialog.format_secondary_text(message)

    result = dialog.run()
    dialog.destroy()

    return result == Gtk.ResponseType.YES


def confirm(window, title, message):
    dialog = Gtk.MessageDialog(window._impl, 0, Gtk.MessageType.WARNING,
        Gtk.ButtonsType.OK_CANCEL, title)
    dialog.format_secondary_text(message)

    result = dialog.run()
    dialog.destroy()

    return result == Gtk.ResponseType.OK


def error(window, title, message):
    dialog = Gtk.MessageDialog(window._impl, 0, Gtk.MessageType.ERROR,
        Gtk.ButtonsType.CANCEL, title)
    dialog.format_secondary_text(message)

    dialog.run()
    dialog.destroy()


def stack_trace(window, title, message, content, retry=False):
    raise NotImplementedError()
