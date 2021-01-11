from ..libs import WinForms


class Clipboard():

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def get_text(self):
        if WinForms.Clipboard.ContainsText():
            return WinForms.Clipboard.GetText()
        else:
            return None

    def set_text(self, text):
        if text is None:
            WinForms.Clipboard.Clear()
        else:
            WinForms.Clipboard.SetText(text)
