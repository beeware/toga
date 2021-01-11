from ..libs import WinForms


class Clipboard():
    data_types = {
        "Text": WinForms.DataFormats.Text
    }

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def get_clipdata(self, type):
        if type not in self.data_types:
            raise ValueError('data type not implemented for this platform.')
        iDataObject = WinForms.Clipboard.GetDataObject()
        # Determines if the data is available in the requested format.
        if iDataObject.GetDataPresent(self.data_types[type]):
            return iDataObject.GetData(self.data_types[type])
        else:
            return None

    def set_clipdata(self, data):
        if data is None:
            WinForms.Clipboard.Clear()
        else:
            # set data persistently (stays in clipboard when app ends)
            WinForms.Clipboard.SetDataObject(data, True)
        