from toga_gtk.libs import Gtk

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = Gtk.Notebook

    def repaint_needed(self):
        return (
            self.impl.sub_containers[self.native.get_current_page()].needs_redraw
            or super().repaint_needed()
        )

    def select_tab(self, index):
        # Can't select a tab that isn't visible.
        if self.impl.sub_containers[index].get_visible():
            self.native.set_current_page(index)
