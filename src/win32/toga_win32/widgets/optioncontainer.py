from __future__ import print_function, absolute_import, division

from .libs import *
from .window import Window


class MainWindow(Window):
    def on_close(self):
        user32.PostQuitMessage(0)

class OptionContainer(Widget):
    def create(self):
        pass
        

    def add_content(self, label, widget):
        pass
