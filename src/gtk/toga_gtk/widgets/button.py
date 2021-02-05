from travertino.size import at_least

from ..libs import Gtk
from .base import Widget


class Button(Widget):
    def create(self):
        self.native = Gtk.Button()
        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())
        self.native.connect('clicked', self.gtk_on_press)

    def set_label(self, label):
        self.native.set_label(self.interface.label)
        self.rehint()

    def set_enabled(self, value):
        self.native.set_sensitive(value)

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
                print(style)

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

    def set_color(self, color):
        if color:
            # getting StyleContext of the widget
            style_context = self.native.get_style_context()

            # creating css
            style = (
                ".custom-style {" +
                f"color: rgba({color.r}, {color.g}, {color.b}, {color.a});" +
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
                "background-image: none;" +
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

    def set_on_press(self, handler):
        # No special handling required
        pass

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[1]

    def gtk_on_press(self, event):
        if self.interface.on_press:
            self.interface.on_press(self.interface)
