from travertino.size import at_least

from ..libs import Gtk, get_background_color_css, get_color_css, get_font_css


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.native = None
        self.style_providers = {}
        self.create()
        self.interface.style.reapply()

    @property
    def viewport(self):
        # TODO: Remove the use of viewport
        return self._container

    def create(self):
        pass

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self.container:
            if container:
                raise RuntimeError("Already have a container")
            else:
                # container is set to None, removing self from the container.native
                # Note from pygtk documentation: Note that the container will own a
                # reference to widget, and that this may be the last reference held;
                # so removing a widget from its container can cause that widget to be
                # destroyed. If you want to use widget again, you should add a
                # reference to it.
                self._container.remove(self.native)
                self._container = None
        elif container:
            # setting container, adding self to container.native
            self._container = container
            self._container.add(self.native)
            self.native.show_all()

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.native.set_sensitive(self.interface.enabled)

    def focus(self):
        self.native.grab_focus()

    def get_tab_index(self):
        self.interface.factory.not_implementated("Widget.get_tab_index()")

    def set_tab_index(self, tab_index):
        self.interface.factory.not_implementated("Widget.set_tab_index()")

    ######################################################################
    # CSS tools
    ######################################################################

    def apply_css(self, property, css):
        """Apply a CSS style controlling a specific property type.

        GTK controls appearance with CSS; each GTK widget can have
        an independent style sheet, composed out of multiple providers.

        Toga uses a separate provider for each property that
        needs to be controlled (e.g., color, font, ...). When that
        property is modified, the old provider for that property is
        removed; if new CSS has been provided, a new provider is
        constructed and added to the widget.

        It is assumed that every Toga widget will have the class
        ``toga``.

        :param name: The style property to modify
        :param css: A dictionary of string key-value pairs, describing
            the new CSS for the given property. If ``None``, the Toga
            style for that property will be reset
        """
        style_context = self.native.get_style_context()
        style_provider = self.style_providers.pop(property, None)

        # If there was a previous style provider for the given property, remove
        # it from the GTK widget
        if style_provider:
            style_context.remove_provider(style_provider)

        # If there's new CSS to apply, construct a new provider, and install it.
        if css is not None:
            # Create a new CSS StyleProvider
            style_provider = Gtk.CssProvider()
            styles = " ".join(f"{key}: {value};" for key, value in css.items())
            # print(f"SET {self} {property}={styles}")
            style_provider.load_from_data((".toga {" + styles + "}").encode())

            # Add the provider to the widget
            style_context.add_provider(
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )
            # Store the provider so it can be removed later
            self.style_providers[property] = style_provider

    ######################################################################
    # APPLICATOR
    ######################################################################

    def set_bounds(self, x, y, width, height):
        # If the bounds have changed, we need to queue a resize on the container
        if self.container:
            self.container.make_dirty()

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        return not self.native.set_visible(not hidden)

    def set_color(self, color):
        self.apply_css("color", get_color_css(color))

    def set_background_color(self, color):
        self.apply_css("background_color", get_background_color_css(color))

    def set_font(self, font):
        self.apply_css("font", get_font_css(font))

    ######################################################################
    # INTERFACE
    ######################################################################

    def add_child(self, child):
        child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def rehint(self):
        # GTK doesn't/can't immediately evaluate the hinted size of the widget.
        # Instead, put the widget onto a dirty list to be rehinted before the
        # next layout.
        if self.container:
            self.container.make_dirty(self)

    def gtk_rehint(self):
        # Perform the actual GTK rehint.
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = at_least(height[0])
