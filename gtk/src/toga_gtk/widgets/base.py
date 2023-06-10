from abc import abstractmethod

from travertino.size import at_least

from ..libs import get_background_color_css, get_color_css, get_font_css


class Widget:
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self.native = None
        self._container = None
        self._widget_styles = {}
        self.create()

        # Ensure the native widget has links to the interface and impl
        self.native.interface = self.interface
        self.native._impl = self

        # Ensure the native widget has GTK CSS style attributes; create() should
        # ensure any other widgets are also styled appropriately.
        self.native.set_name(f"toga-{self.interface.id}")

        # Ensure initial styles are applied.
        self.interface.style.reapply()

    @property
    def viewport(self):
        # TODO: Remove the use of viewport
        return self._container

    @abstractmethod
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
            assert container is None, "Widget Already have a container"

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
            self.native.set_parent(self._container)
            self.native.set_visible(True)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def get_enabled(self):
        return self.native.get_sensitive()

    def set_enabled(self, value):
        self.native.set_sensitive(value)

    @property
    def has_focus(self):
        return self.native.has_focus()

    def focus(self):
        if not self.has_focus:
            self.native.grab_focus()

    def get_tab_index(self):
        self.interface.factory.not_implemented("Widget.get_tab_index()")

    def set_tab_index(self, tab_index):
        self.interface.factory.not_implemented("Widget.set_tab_index()")

    # CSS tools ===============================================================

    def apply_css(self, property, css):
        """Apply a CSS style controlling a specific property type.

        GTK controls appearance with CSS; each GTK widget can have a unique
        selector that specific for it. This CSS is applied on display at
        once to make effects on widgets.

        Toga maintains a separate CSS for each widget that controlls
        different properties (e.g., color, font, ...). When one of these
        properties is modified by updates or removes, Toga updates this
        property on the CSS and passes this updated CSS to the toplevel
        app which takes the responsibility of appling these changes.

        It is assumed that every Toga widget will have the id attribute
        ``toga-id(widget)`` that gives unique access to the widget style.

        :param property: The style property to modify
        :param css: A dictionary of string key-value pairs, describing
            the new CSS for the given property. If ``None``, the Toga
            style for that property will be reset
        """
        # If there's new CSS to apply, install it.
        if css:
            # Update the property
            self._widget_styles[property] = css
        else:
            # Reset the property
            self._widget_styles.pop(property, None)

        # Apply css
        if self.interface.app:
            styles = {
                key: value
                for prop_value in self._widget_styles.values()
                for key, value in prop_value.items()
            }
            css_styles = " ".join(
                f"{key}: {value};" for key, value in styles.items()
            )
            widget_css = (
                f"{self.native.get_css_name()}#{self.native.get_name()}" + " {" + css_styles + "}"
            )
            self.interface.app._impl.apply_styles(widget_css, self.native)

    # APPLICATOR ==============================================================

    def set_bounds(self, x, y, width, height):
        # Any position changes are applied by the container during do_size_allocate.
        self.container.make_dirty()

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        self.native.set_visible(not hidden)

    def set_color(self, color):
        self.apply_css("color", get_color_css(color))

    def set_background_color(self, color):
        self.apply_css("background_color", get_background_color_css(color))

    def set_font(self, font):
        self.apply_css("font", get_font_css(font))

    # INTERFACE ===============================================================

    def add_child(self, child):
        child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def refresh(self):
        # GTK doesn't/can't immediately evaluate the hinted size of the widget.
        # Instead, put the widget onto a dirty list to be rehinted before the
        # next layout.
        if self.container:
            self.container.make_dirty(self)

    def rehint(self):
        # Perform the actual GTK rehint.
        min_size, _ = self.native.get_preferred_size()

        # print("REHINT", self, f"{width_info[0]}x{height_info[0]}")
        self.interface.intrinsic.width = at_least(min_size.width)
        self.interface.intrinsic.height = at_least(min_size.height)
