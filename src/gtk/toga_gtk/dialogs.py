from gi.repository import Gtk


def _set_filetype_filter(dialog, file_type):
    '''Mutating function that Takes a dialog and inserts a Gtk.FileFilter

    Args:
        dialog: Gtk.FileChooserDialog to apply the filter
        file_type: (str) the file type to filter
    '''
    filter_filetype = Gtk.FileFilter()
    filter_filetype.set_name("." + file_type + " files")
    filter_filetype.add_pattern("*." + file_type)
    dialog.add_filter(filter_filetype)


def info(window, title, message):
    dialog = Gtk.MessageDialog(
        transient_for=window._impl.native,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    dialog.format_secondary_text(message)

    dialog.run()
    dialog.destroy()


def question(window, title, message):
    dialog = Gtk.MessageDialog(
        transient_for=window._impl.native,
        flags=0,
        message_type=Gtk.MessageType.QUESTION,
        buttons=Gtk.ButtonsType.YES_NO,
        text=title
    )
    dialog.format_secondary_text(message)

    result = dialog.run()
    dialog.destroy()

    return result == Gtk.ResponseType.YES


def confirm(window, title, message):
    dialog = Gtk.MessageDialog(
        transient_for=window._impl.native,
        flags=0,
        message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.OK_CANCEL,
        text=title
    )
    dialog.format_secondary_text(message)

    result = dialog.run()
    dialog.destroy()

    return result == Gtk.ResponseType.OK


def error(window, title, message):
    dialog = Gtk.MessageDialog(
        transient_for=window._impl.native,
        flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.CANCEL,
        text=title
    )
    dialog.format_secondary_text(message)

    dialog.run()
    dialog.destroy()


def stack_trace(window, title, message, content, retry=False):
    window.platform.not_implemented('dialogs.stack_trace()')


def save_file(window, title, suggested_filename, file_types):

    filename = None
    dialog = Gtk.FileChooserDialog(
        title=title,
        transient_for=window._impl.native,
        action=Gtk.FileChooserAction.SAVE,
    )
    dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
    dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.OK)

    for file_type in file_types or []:
        _set_filetype_filter(dialog, file_type)

    dialog.set_current_name(suggested_filename if not file_types else
                            suggested_filename + "." + file_types[0])

    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        filename = dialog.get_filename()

    dialog.destroy()
    return filename


def open_file(window, title, file_types, multiselect):
    filename_or_filenames = None
    dialog = Gtk.FileChooserDialog(
        title=title,
        transient_for=window._impl.native,
        action=Gtk.FileChooserAction.OPEN,
    )
    dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
    dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

    for file_type in file_types or []:
        _set_filetype_filter(dialog, file_type)
    if multiselect:
        dialog.set_select_multiple(True)

    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        filename_or_filenames = (dialog.get_filenames() if multiselect else
                                 dialog.get_filename())
    dialog.destroy()
    if filename_or_filenames is None:
        raise ValueError('No filename provided in the open file dialog')
    return filename_or_filenames


def select_folder(window, title, multiselect):
    '''This function is very similar to the open_file function but more limited
    in scope. If broadening scope here, or aligning features with the other
    dialogs, consider refactoring around a common base function or set of
    functions'''
    filename = None
    dialog = Gtk.FileChooserDialog(
        title=title,
        transient_for=window._impl.native,
        action=Gtk.FileChooserAction.SELECT_FOLDER,
    )
    dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
    dialog.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        filename = dialog.get_filename()
    dialog.destroy()
    if filename is None:
        raise ValueError("No folder provided in the select folder dialog")
    return [filename]
