from pathlib import Path

import System.Windows.Forms as WinForms
from System.Drawing import Image

from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = WinForms.PictureBox()
        self.native.Image = Image.FromFile(
            str(Path(__file__).parent.parent / "resources" / "spinner.gif")
        )
        self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom
        self.running = True

    def set_hidden(self, hidden):
        self.native.Visible = (not self.running) or hidden

    def is_running(self):
        return self.running

    def start(self):
        self.native.Visible = True
        self.running = True

    def stop(self):
        self.native.Visible = False
        self.running = False

    def rehint(self):
        self.interface.intrinsic.width = 32
        self.interface.intrinsic.height = 32
