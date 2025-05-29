from ctypes import windll
from pathlib import Path

import System.Windows.Forms as WinForms
from System.Drawing import Image

from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = WinForms.PictureBox()
        windll.user32.SetProcessDPIAware()
        if windll.user32.GetDpiForSystem() > 96:
            self.native.Image = Image.FromFile(
                str(Path(__file__).parent.parent / "resources" / "spinner2x.gif")
            )
        else:
            self.native.Image = Image.FromFile(
                str(Path(__file__).parent.parent / "resources" / "spinner.gif")
            )
        self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom
        self.interface.intrinsic.width = 32
        self.interface.intrinsic.height = 32
        self.running = False

    def set_hidden(self, hidden):
        self.native.Visible = self.running and not hidden
        self.hidden = hidden

    def is_running(self):
        return self.running

    def start(self):
        self.running = True
        self.native.Visible = not self.hidden

    def stop(self):
        self.native.Visible = False
        self.running = False

    def rehint(self):
        self.interface.intrinsic.width = 32
        self.interface.intrinsic.height = 32
