import pytest
from pytest import skip, xfail

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class SelectionProbe(SimpleProbe):
    if GTK_VERSION < (4, 0, 0):
        native_class = Gtk.ComboBoxText
    else:
        native_class = Gtk.DropDown
        pytest.skip("GTK4 doesn't support selection probes yet")

    def assert_resizes_on_content_change(self):
        pass

    @property
    def shrink_on_resize(self):
        return False

    @property
    def text_align(self):
        xfail("Can't change the text alignment of Selection on GTK")

    @property
    def color(self):
        # Skip, because this *should* be possible to fix
        skip("Can't change the color of Selection on GTK")

    @property
    def background_color(self):
        # Skip, because this *should* be possible to fix
        skip("Can't change the background color of Selection on GTK")

    @property
    def titles(self):
        titles = []

        def add_title(model, path, itr):
            titles.append(model.get_value(itr, 0))

        self.native.get_model().foreach(add_title)
        return titles

    @property
    def selected_title(self):
        return self.native.get_active_text()

    async def select_item(self):
        self.native.popup()
        self.native.set_active(1)
