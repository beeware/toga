import System.Windows.Forms
from pytest import xfail

from .base import SimpleProbe


class SelectionProbe(SimpleProbe):
    native_class = System.Windows.Forms.ComboBox
    background_supports_alpha = False
    fixed_height = 23

    def assert_resizes_on_content_change(self):
        xfail("Selection doesn't resize on content changes on this backend")

    @property
    def alignment(self):
        xfail("Can't change the alignment of Selection on this backend")

    @property
    def titles(self):
        return list(self.native.Items)

    @property
    def selected_title(self):
        return self.native.SelectedItem

    async def select_item(self):
        self.native.SelectedIndex = 1
