import weakref

from win32more.Microsoft.UI.Xaml.Controls import RelativePanel
from win32more.Windows.UI.Text import FontStyle

"""
Overview of content staging

ISSUE: Some Toga widgets (e.g. Button) use minimum size constraints that are based on
their content. The native WinUI 3 widget will resize itself according to this content,
but only if size values have not been manually set. Since the size values are manually
set by the Toga style applicator, the native widget will not resize.

SOLUTION: The work-around used here is to 'stage' the properties that lead to resizing.
In practice, this means that when a property is changed, a copy of the widget is created
in a hidden panel and allowed to resize. Upon resize, the copy is destroyed and the new
minimum size measurements are then sent to the Toga style applicator.
    The main advantage of copying the widget is that flicker is reduced: The displayed
widget will only change appearance when the new size has been calculated.

IMPORTANT: The values of staged properties are set as 'value creator' callables that
create new instances of the desired content. This is because not all native classes can
be children of multiple native classes.
"""


class StagingArea:
    """A class used to calculate content-based constraints for WinUI 3 widgets.

    A StagingArea has a hidden native panel that allows widgets with the staged content
    resize themselves. Every StagingArea is attached to a Container and its hidden
    native panel is a child of a Container's own native panel.
    """

    def __init__(self, container):
        """Create an instance of a StagingArea.

        :param container: The Container where the StagingArea will be attached.
        """
        self.native = RelativePanel()
        self.native.Opacity = 0

        self._native_widgets = []

        # Add the container
        self._container = container
        self._container.widgets.add(self)

    def add(self, native_widget):
        self._native_widgets.append(native_widget)
        self.native.Children.Append(native_widget)

    def remove(self, native_widget):
        """Removes a widget and triggers a layout refresh."""
        index = self._native_widgets.index(native_widget)
        self._native_widgets.remove(native_widget)
        self.native.Children.RemoveAt(index)

        # It is possible that self._container._content was removed during the staging
        # process. It is difficult to reliably create this scenario during testing, so
        # use no branch here.
        if self._container._content:  # pragma: no branch
            self._container._content.interface.refresh()


class StagedProperties:
    def __init__(self, widget):
        self._widget = widget
        self._staged_properties = {}
        self._latest = None

        self._font_keys = {"FontFamily", "FontSize", "FontStyle", "FontWeight"}

    def __setattr__(self, name, value):
        """Sets the native property value for a name with a capital first character.

        Note that the 'value' of a staged property must be a 'value creator' callable
        that creates a new instance of the desired content.
        """
        if not name[0].isupper():
            super().__setattr__(name, value)
            return

        # Set and cache the native property.
        setattr(self._widget._native_properties, name, value())
        self._staged_properties[name] = value

        self.refresh()

    def refresh(self):
        if not self._widget.container:
            return

        # The properties in self._font_keys are only staged if other content such as
        # text is being staged as well.
        if set(self._staged_properties.keys()) - self._font_keys == set():
            return

        widget = self._widget
        clone = type(widget.native)()
        staging_area = widget.container.staging_area
        self._latest = clone

        # Use a weak reference so that the external process doesn't prevent garbage
        # collection.
        clone_weak = weakref.ref(clone)
        area_weak = weakref.ref(staging_area)

        def size_changed(sender, args, clone_weak=clone_weak, area_weak=area_weak):
            self.native_event_size_changed(sender, args, clone_weak, area_weak)

        clone.event_handler.SizeChanged += size_changed

        for attribute, value_creator in self._staged_properties.items():
            value = value_creator()
            if value is not None:
                setattr(clone, attribute, value)

        staging_area.add(clone)

    def native_event_size_changed(self, sender, args, clone_weak, area_weak):
        clone = clone_weak()
        staging_area = area_weak()

        # If the clone or staging area no longer exist then do nothing. This is not
        # reliably hit during testing to use no over.
        if not clone or not staging_area:  # pragma: no cover
            return

        if clone == self._latest:
            self._widget._min_width = self._adjusted_width(clone)
            self._widget._min_height = clone.ActualSize.Y
            self._widget.rehint()

            self._latest = None

        staging_area.remove(clone)

    def _adjusted_width(self, clone):
        # FIXME: The staging method doesn't calculate a large enough width for italic
        # and oblique font styles. Add 0.25em for each of these.
        if clone.FontStyle in {FontStyle.Oblique, FontStyle.Italic}:
            font_size = clone.FontSize
            return clone.ActualSize.X + round(font_size * 96 / 72 / 4, 0)

        return clone.ActualSize.X
