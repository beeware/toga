from toga_gtk.libs import Gtk

from .base import SimpleProbe
from .properties import toga_alignment, toga_color, toga_font


class MultilineTextInputProbe(SimpleProbe):
    native_class = Gtk.ScrolledWindow

    def __init__(self, widget):
        super().__init__(widget)
        self.native_textview = self.impl.native_textview

        # Keypress events must be sent to the inner textview
        self._keypress_target = self.native_textview

    @property
    def value(self):
        return self.impl.buffer.get_text(
            self.impl.buffer.get_start_iter(), self.impl.buffer.get_end_iter(), True
        )

    @property
    def placeholder(self):
        return self.impl.placeholder.get_text(
            self.impl.placeholder.get_start_iter(),
            self.impl.placeholder.get_end_iter(),
            True,
        )

    def placeholder_visible(self):
        return self.native_textview.get_buffer() == self.impl.placeholder

    @property
    def placeholder_hides_on_focus(self):
        return True

    @property
    def color(self):
        # This is a weak test; the widget requires the style to be set
        # on the child ``text`` node, but Gtk doesn't expose that style
        # as something that can be inspected. As a workaround, we check
        # that the style property has been set on the base widget, and
        # that there is a CSS style provider targeting both the base node
        # and the ``text`` child node
        try:
            css_provider = self.impl.style_providers[
                ("color", id(self.native_textview))
            ]
        except KeyError:
            # No style provider exists yet, so defaults will be in effect
            pass
        else:
            assert ".toga {\n" in css_provider.to_string()
            assert ".toga text {\n" in css_provider.to_string()

        sc = self.native_textview.get_style_context()
        return toga_color(sc.get_property("color", sc.get_state()))

    @property
    def background_color(self):
        # This is a weak test; the widget requires the style to be set
        # on the child ``text`` node, but Gtk doesn't expose that style
        # as something that can be inspected. As a workaround, we check
        # that the style property has been set on the base widget, and
        # that there is a CSS style provider targeting both the base node
        # and the ``text`` child node
        try:
            css_provider = self.impl.style_providers[
                ("background_color", id(self.native_textview))
            ]
        except KeyError:
            # No style provider exists yet, so defaults will be in effect
            pass
        else:
            assert ".toga {\n" in css_provider.to_string()
            assert ".toga text {\n" in css_provider.to_string()

        sc = self.native_textview.get_style_context()
        return toga_color(sc.get_property("background-color", sc.get_state()))

    @property
    def font(self):
        sc = self.native_textview.get_style_context()
        return toga_font(sc.get_property("font", sc.get_state()))

    @property
    def alignment(self):
        return toga_alignment(
            self.native_textview.get_justification(),
        )

    @property
    def enabled(self):
        # Enabled is proxied onto readonly on the text view
        return self.native_textview.get_property("editable")

    @property
    def readonly(self):
        return not self.native_textview.get_property("editable")

    @property
    def visible_height(self):
        return self.native.get_allocation().height

    @property
    def visible_width(self):
        return self.native.get_allocation().width

    @property
    def document_height(self):
        return self.native.get_vadjustment().get_upper()

    @property
    def document_width(self):
        return self.native.get_hadjustment().get_upper()

    @property
    def vertical_scroll_position(self):
        return self.native.get_vadjustment().get_value()

    async def wait_for_scroll_completion(self):
        pass
