from .libs import *

from .widgets.icon import Icon


def info(window, title, message, button_label='OK'):
    alert = NSAlert.alloc().init()
    alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSInformationalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.addButtonWithTitle_(button_label)

    alert.runModal()


def question(window, title, message, button_label=('Yes', 'No')):
    alert = NSAlert.alloc().init()
    alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSInformationalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.addButtonWithTitle_(button_label[0])
    alert.addButtonWithTitle_(button_label[1])

    result = alert.runModal()
    return result == NSAlertFirstButtonReturn


def confirm(window, title, message, button_label=('OK', 'Cancel')):
    alert = NSAlert.alloc().init()
    alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSWarningAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.addButtonWithTitle_(button_label[0])
    alert.addButtonWithTitle_(button_label[1])

    result = alert.runModal()
    return result == NSAlertFirstButtonReturn


def error(window, title, message, button_label='OK'):
    alert = NSAlert.alloc().init()
    alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSCriticalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.addButtonWithTitle_(button_label)

    alert.runModal()


def stack_trace(window, title, message, content, retry=False,
                                            button_label=('Retry', 'Cancel')):
    alert = NSAlert.alloc().init()
    alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSCriticalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    scroll = NSScrollView.alloc().initWithFrame_(NSMakeRect(0,0,350,200))
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
        alert.addButtonWithTitle_(button_label[0])
        alert.addButtonWithTitle_(button_label[1])
        result = alert.runModal()
        return result == NSAlertFirstButtonReturn
    else:
        alert.runModal()


def save_file(window, title, suggested_filename, file_types):
    panel = NSSavePanel.alloc().init()
    panel.title = title

    arr = NSArray.alloc().init()

    for x in file_types:
        arr = arr.arrayByAddingObject_(x)

    panel.allowedFileTypes = arr
    panel.nameFieldStringValue = suggested_filename

    result = panel.runModal()

    if result == NSFileHandlingPanelOKButton:
        return panel.URL.path
    return None
