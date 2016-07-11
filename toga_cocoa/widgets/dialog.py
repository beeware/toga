from ..libs import *

from .icon import Icon


class Dialog(object):
    @staticmethod
    def info(title, message):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSInformationalAlertStyle)
        alert.setMessageText_(title)
        alert.setInformativeText_(message)

        alert.runModal()

    @staticmethod
    def question(title, message):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSInformationalAlertStyle)
        alert.setMessageText_(title)
        alert.setInformativeText_(message)

        alert.addButtonWithTitle_('Yes')
        alert.addButtonWithTitle_('No')

        result = alert.runModal()
        return result == NSAlertFirstButtonReturn

    @staticmethod
    def confirm(title, message):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSWarningAlertStyle)
        alert.setMessageText_(title)
        alert.setInformativeText_(message)

        alert.addButtonWithTitle_('OK')
        alert.addButtonWithTitle_('Cancel')

        result = alert.runModal()
        return result == NSAlertFirstButtonReturn

    @staticmethod
    def error(title, message):
        alert = NSAlert.alloc().init()
        alert.icon = Icon.app_icon._impl
        alert.setAlertStyle_(NSCriticalAlertStyle)
        alert.setMessageText_(title)
        alert.setInformativeText_(message)

        alert.runModal()

    @staticmethod
    def stack_trace(title, message, content, retry=False):
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
            alert.addButtonWithTitle_('Retry')
            alert.addButtonWithTitle_('Cancel')
            result = alert.runModal()
            return result == NSAlertFirstButtonReturn
        else:
            alert.runModal()
