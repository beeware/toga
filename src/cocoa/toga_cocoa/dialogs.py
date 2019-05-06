from .libs import *


def info(window, title, message):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon.bind(window.factory).native
    alert.setAlertStyle_(NSInformationalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.runModal()


def question(window, title, message):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon.bind(window.factory).native
    alert.setAlertStyle_(NSInformationalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.addButtonWithTitle_('Yes')
    alert.addButtonWithTitle_('No')

    result = alert.runModal()
    return result == NSAlertFirstButtonReturn


def confirm(window, title, message):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon.bind(window.factory).native
    alert.setAlertStyle_(NSWarningAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.addButtonWithTitle_('OK')
    alert.addButtonWithTitle_('Cancel')

    result = alert.runModal()
    return result == NSAlertFirstButtonReturn


def error(window, title, message):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon.bind(window.factory).native
    alert.setAlertStyle_(NSCriticalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.runModal()


def stack_trace(window, title, message, content, retry=False):
    alert = NSAlert.alloc().init()
    alert.icon = window.app.icon.bind(window.factory).native
    alert.setAlertStyle_(NSCriticalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    scroll = NSScrollView.alloc().initWithFrame_(NSMakeRect(0, 0, 500, 200))
    scroll.setHasVerticalScroller_(True)
    scroll.setHasHorizontalScroller_(False)
    scroll.setAutohidesScrollers_(False)
    scroll.setBorderType_(NSBezelBorder)

    trace = NSTextView.alloc().init()
    trace.insertText_(content)
    trace.setEditable_(False)
    trace.setVerticallyResizable_(True)
    trace.setHorizontallyResizable_(True)

    scroll.setDocumentView_(trace)
    alert.setAccessoryView_(scroll)

    if retry:
        alert.addButtonWithTitle_('Retry')
        alert.addButtonWithTitle_('Quit')
        result = alert.runModal()
        return result == NSAlertFirstButtonReturn
    else:
        alert.runModal()


def save_file(window, title, suggested_filename, file_types=None):
    panel = NSSavePanel.alloc().init()
    panel.title = title

    if file_types:
        arr = NSArray.alloc().init()
        for x in file_types:
            arr = arr.arrayByAddingObject_(x)
    else:
        arr = None

    panel.allowedFileTypes = arr
    panel.nameFieldStringValue = suggested_filename

    result = panel.runModal()

    if result == NSFileHandlingPanelOKButton:
        return panel.URL.path
    return None


def open_file(window, title, file_types, multiselect):
    """Cocoa open file dialog implementation.

    We restrict the panel invocation to only choose files. We also allow
    creating directories but not selecting directories.

    Args:
        window: The window this dialog belongs to.
        title: Title of the modal.
        file_types: Ignored for now.
        multiselect: Flag to allow multiple file selection.
    Returns:
        The file path on success, None otherwise.
    """

    # Initialize and configure the panel.
    panel = NSOpenPanel.alloc().init()
    panel.title = title
    panel.allowedFileTypes = file_types
    panel.allowsMultipleSelection = multiselect
    panel.canChooseDirectories = False
    panel.canCreateDirectories = True
    panel.canChooseFiles = True

    # Show modal and return file path on success.
    result = panel.runModal()
    if NSFileHandlingPanelOKButton == result:
        paths = [str(url.path) for url in panel.URLs]
        filename_or_filenames = (paths if multiselect else
                                 panel.URL.path)
        return filename_or_filenames
    return None
