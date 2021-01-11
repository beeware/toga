from ..libs import WinForms


class Clipboard():

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def get_clipdata(self):
        IDataObject iData = WinForms.Clipboard.GetDataObject()
        #.Determines whether the data is in a format you can use.
        if(iData.GetDataPresent(DataFormats.Text)):
          # Yes it is, so display it in a text box.
          return str(iData.GetData(DataFormats.Text))
        else:
          return None

    def set_clipdata(self, data):
        WinForms.Clipboard.SetDataObject(data)
        