from ..libs import *

from gi.repository import Gtk


class Dialog(object):
    @staticmethod
    def info(title, message):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(message)

        dialog.run()
        dialog.destroy()

    @staticmethod
    def question(title, message):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, title)
        dialog.format_secondary_text(message)

        result = dialog.run()
        dialog.destroy()

        return result == Gtk.ResponseType.YES

    @staticmethod
    def confirm(title, message):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, title)
        dialog.format_secondary_text(message)

        result = dialog.run()
        dialog.destroy()

        return result == Gtk.ResponseType.OK

    @staticmethod
    def error(title, message):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, title)
        dialog.format_secondary_text(message)

        dialog.run()
        dialog.destroy()

    @staticmethod
    def stack_trace(title, message, content, retry=False):
        raise NotImplementedError()
