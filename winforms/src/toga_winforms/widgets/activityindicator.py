import System.Windows.Forms as WinForms

from toga_winforms.resources.antialias_spinner import antialias_spinner

from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = WinForms.PictureBox()
        self.native.Image = antialias_spinner(
            (self.native.BackColor.R, self.native.BackColor.G, self.native.BackColor.B)
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
