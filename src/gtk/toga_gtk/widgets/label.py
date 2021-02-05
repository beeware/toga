from travertino.size import at_least

from ..libs import Gtk, gtk_alignment
from .base import Widget


class Label(Widget):
    def create(self):
        self.native = Gtk.Label()
        self.native.set_line_wrap(False)

        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())

    def set_alignment(self, value):
        self.native.set_alignment(*gtk_alignment(value))

    def set_color(self, value):
        if value:
            # getting StyleContext of the widget
            style_context = self.native.get_style_context()

            # creating css
            style = (
                ".custom-style {" +
                f"color: rgba({value.r}, {value.g}, {value.b}, {value.a});" +
                "}"
                )

            # creating StyleProvider (i.e CssProvider)
            style_provider = Gtk.CssProvider()
            style_provider.load_from_data(style.encode())

            # setting the StyleProvider to StyleContext
            style_context.add_provider(
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER,
                )
            style_context.add_class("custom-style")

    def set_background_color(self, color):
        if color:
            # getting StyleContext of the widget
            style_context = self.native.get_style_context()

            # creating css
            style = (
                ".custom-style {" +
                f"background-color: rgba({color.r}, {color.g}, {color.b}, {color.a});" +
                "}"
                )

            # creating StyleProvider (i.e CssProvider)
            style_provider = Gtk.CssProvider()
            style_provider.load_from_data(style.encode())

            # setting the StyleProvider to StyleContext
            style_context.add_provider(
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER,
                )
            style_context.add_class("custom-style")

    def set_font(self, value):
        if value:

            style = ".custom-style { "

            flag = False
            if value.family != "system":
                style += f"font-family: {value.family}; "
                flag = True
            if value.size != -1:
                style += f"font-size: {value.size}px; "
                flag = True
            if value.style != "normal":
                style += f"font-style: {value.style}; "
                flag = True
            if value.variant != "normal":
                style += f"font-variant: {value.variant}; "
                flag = True
            if value.weight != "normal":
                style += f"font-weight: {value.weight}; "
                flag = True

            if flag:
                style += "}"

                # getting StyleContext of the widget
                style_context = self.native.get_style_context()

                # creating StyleProvider (i.e CssProvider)
                style_provider = Gtk.CssProvider()
                style_provider.load_from_data(style.encode())

                # setting the StyleProvider to StyleContext
                style_context.add_provider(
                    style_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_USER,
                    )
                style_context.add_class("custom-style")

    def set_text(self, value):
        # FIXME after setting the label the label jumps to the top left
        # corner and only jumps back at its place after resizing the window.
        self.native.set_text(self.interface._text)

    def rehint(self):
        # print("REHINT", self,
        #     self.native.get_preferred_width(), self.native.get_preferred_height(),
        #     getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False)
        # )
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[1]
