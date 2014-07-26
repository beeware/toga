from ..libs import *

from .icon import Icon


class Dialog(object):
    @staticmethod
    def info(title, message):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSInformationalAlertStyle)
        alert.setMessageText_(get_NSString(title))
        alert.setInformativeText_(get_NSString(message))

        alert.runModal()

    @staticmethod
    def question(title, message):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSInformationalAlertStyle)
        alert.setMessageText_(get_NSString(title))
        alert.setInformativeText_(get_NSString(message))

        alert.addButtonWithTitle_(get_NSString('Yes'))
        alert.addButtonWithTitle_(get_NSString('No'))

        result = alert.runModal()
        return result == NSAlertFirstButtonReturn

    @staticmethod
    def confirm(title, message):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSWarningAlertStyle)
        alert.setMessageText_(get_NSString(title))
        alert.setInformativeText_(get_NSString(message))

        alert.addButtonWithTitle_(get_NSString('OK'))
        alert.addButtonWithTitle_(get_NSString('Cancel'))

        result = alert.runModal()
        return result == NSAlertFirstButtonReturn

    @staticmethod
    def error(title, message):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSCriticalAlertStyle)
        alert.setMessageText_(get_NSString(title))
        alert.setInformativeText_(get_NSString(message))

        alert.runModal()

    @staticmethod
    def stack_trace(title, message, content, retry=False):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSCriticalAlertStyle)
        alert.setMessageText_(get_NSString(title))
        alert.setInformativeText_(get_NSString(message))

        scroll = NSScrollView.alloc().initWithFrame_(NSMakeRect(0,0,350,200))
        scroll.setHasVerticalScroller_(True)
        scroll.setHasHorizontalScroller_(False)
        scroll.setAutohidesScrollers_(False)
        scroll.setBorderType_(NSBezelBorder)

        trace = NSTextView.alloc().init()
        trace.insertText_(get_NSString(content))
        trace.setEditable_(False)
        trace.setVerticallyResizable_(True)
        trace.setHorizontallyResizable_(True)

        scroll.setDocumentView_(trace)
        alert.setAccessoryView_(scroll)

        if retry:
            alert.addButtonWithTitle_(get_NSString('Retry'))
            alert.addButtonWithTitle_(get_NSString('Cancel'))
            result = alert.runModal()
            return result == NSAlertFirstButtonReturn
        else:
            alert.runModal()
