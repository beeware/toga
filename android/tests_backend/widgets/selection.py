from pytest import xfail

from android.widget import Spinner

from .base import SimpleProbe


class SelectionProbe(SimpleProbe):
    native_class = Spinner
    supports_justify = False
    default_font_size = 16

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
        return self.impl.native.getSelectedView().getTypeface()

    @property
    def text_size(self):
        return self.impl.native.getSelectedView().getTextSize()

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
