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


def save_file(window, title, suggested_filename, file_types):

    filename = None
    dialog = Gtk.FileChooserDialog(
        title, window._impl,
        Gtk.FileChooserAction.SAVE,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

    for x in file_types:
        filter_filetype = Gtk.FileFilter()
        filter_filetype.set_name("." + x + " files")
        filter_filetype.add_pattern("*." + x)
        dialog.add_filter(filter_filetype)

    dialog.set_current_name(suggested_filename + "." + file_types[0])

    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        filename = dialog.get_filename()

    dialog.destroy()
    return filename
