import System.Windows.Forms

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = System.Windows.Forms.ProgressBar

    @property
    def is_determinate(self):
        # Winforms doesn't have an explicit flag for describing determinate
        # progress bars; use the shadow flag.
        return self.widget._impl._determinate

    @property
    def is_animating_indeterminate(self):
        # We can use the winforms style to identify animating indeterminates
        return self.native.Style == System.Windows.Forms.ProgressBarStyle.Marquee

    @property
    def position(self):
        return self.native.Value / self.native.Maximum

    async def wait_for_animation(self):
        # WinForms ProgressBar has internal animation handling; no special handling required.
        pass
