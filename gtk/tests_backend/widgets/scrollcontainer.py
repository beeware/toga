from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = Gtk.ScrolledWindow
    scrollbar_inset = 0

    @property
    def has_content(self):
        return self.impl.document_container.content is not None

    @property
    def document_height(self):
        return self.native.get_vadjustment().get_upper()

    @property
    def document_width(self):
        return self.native.get_hadjustment().get_upper()

    async def scroll(self):
        if self.native.get_policy()[1] == Gtk.PolicyType.NEVER:
            return

        # Fake a vertical scroll
        self.native.get_vadjustment().set_value(200)
        self.native.get_vadjustment().emit("changed")

    def repaint_needed(self):
        return self.impl.document_container.needs_redraw or super().repaint_needed()

    async def wait_for_scroll_completion(self):
        # Scroll isn't animated, so this is a no-op.
        pass
