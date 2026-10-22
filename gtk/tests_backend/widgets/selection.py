from pytest import skip, xfail

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class SelectionProbe(SimpleProbe):
    if GTK_VERSION < (4, 0, 0):
        native_class = Gtk.ComboBoxText
    else:
        native_class = Gtk.DropDown

    def assert_resizes_on_content_change(self):
        pass

    @property
    def shrink_on_resize(self):
        return GTK_VERSION >= (4, 0, 0)

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
        if GTK_VERSION >= (4, 0, 0):
            model = self.native.get_model()
            return [model.get_string(index) for index in range(model.get_n_items())]

        titles = []

        def add_title(model, path, itr):
            titles.append(model.get_value(itr, 0))

        self.native.get_model().foreach(add_title)
        return titles

    @property
    def selected_title(self):
        if GTK_VERSION < (4, 0, 0):
            return self.native.get_active_text()
        else:
            item = self.native.get_selected_item()
            return item.get_string() if item is not None else None

    async def select_item(self):
        if GTK_VERSION < (4, 0, 0):
            self.native.popup()
            self.native.set_active(1)
        else:
            self.native.set_selected(1)
