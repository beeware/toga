from android.widget import Spinner
from pytest import xfail

from .base import SimpleProbe


class SelectionProbe(SimpleProbe):
    native_class = Spinner
    supports_justify = False

    def assert_resizes_on_content_change(self):
        xfail("Selection doesn't resize on content changes on this backend")

    @property
    def alignment(self):
        xfail("Can't change the alignment of Selection on this backend")

    @property
    def color(self):
        xfail("Can't change the color of Selection on this backend")

    @property
    def typeface(self):
        xfail("Can't change the font of Selection on this backend")

    @property
    def text_size(self):
        xfail("Can't change the font of Selection on this backend")

    @property
    def background_color(self):
        xfail("Can't change the background color of Selection on this backend")

    @property
    def titles(self):
        return [self.native.getItemAtPosition(i) for i in range(self.native.getCount())]

    @property
    def selected_title(self):
        return self.native.getSelectedItem()

    async def select_item(self):
        self.native.setSelection(1)
