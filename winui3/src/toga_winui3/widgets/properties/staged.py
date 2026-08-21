from typing import ClassVar

from win32more.Microsoft.UI.Xaml.Controls import RelativePanel
from win32more.Windows.UI.Text import FontStyle

from .native import NativeProperties

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

        self._staging_clones = []

        # Add the container
        self._container = container
        self._container.widgets.add(self)

    def add(self, staging_clone):
        self._staging_clones.append(staging_clone)
        self.native.Children.Append(staging_clone.native)

    def remove(self, staging_clone):
        """Removes a widget and triggers a layout refresh."""
        index = self._staging_clones.index(staging_clone)
        self._staging_clones.remove(staging_clone)
        self.native.Children.RemoveAt(index)


class StagingClone:
    """A facsimile of a widget that resizes to fit its content and reports its size.

    Note that a new SizeChanged callback is created when a property is updated during
    an incomplete staging process. This is because an event callback could already be in
    the queue when a property is updated.
    """

    def __init__(self, widget, properties):
        self._widget = widget
        self._removed = False
        self._latest_callback_id = 0

        self.native = type(self._widget.native)()
        self.native.event_handler.SizeChanged += self.create_size_changed_callback()
        self._native_properties = NativeProperties(self)

        for property, value_creator in properties.items():
            value = value_creator()
            if value is not None:
                setattr(self.native, property, value)

        self._widget.container.staging_area.add(self)

    def stage_property(self, name, value):
        self.native.event_handler.SizeChanged.clear()
        self.native.event_handler.SizeChanged += self.create_size_changed_callback()
        setattr(self._native_properties, name, value())

    def remove(self):
        """Remove the clone from the staging process.

        This method is called by the SizeChanged event and when the associated widget is
        removed from its container.
        """
        self._widget._staged_properties._clone = None
        self._widget.container.staging_area.remove(self)
        self._removed = True

    def create_size_changed_callback(self):
        self._latest_callback_id += 1

        def size_changed_callback(sender, args, callback_id=self._latest_callback_id):
            if callback_id != self._latest_callback_id:
                return

            if self._removed:
                return

            self._widget._min_width = self._adjusted_width(self.native)
            self._widget._min_height = self.native.ActualSize.Y
            self._widget.rehint()
            self._widget.container._content.interface.refresh()

            self.remove()

        return size_changed_callback

    def _adjusted_width(self, native):
        # FIXME: The staging method doesn't calculate a large enough width for italic
        # and oblique font styles. Add 0.25em for each of these.
        if native.FontStyle in {FontStyle.Oblique, FontStyle.Italic}:
            font_size = native.FontSize
            return native.ActualSize.X + round(font_size * 96 / 72 / 4, 0)

        return native.ActualSize.X


class StagedProperties:
    _font_properties: ClassVar = {"FontFamily", "FontSize", "FontStyle", "FontWeight"}

    def __init__(self, widget):
        self._widget = widget
        self._clone = None
        self._properties_dict = {}

        self._initialized = False
        self._active = False

    def __setattr__(self, name, value):
        """Sets the native property value for a name with a capital first character.

        Note that the 'value' of a staged property must be a 'value creator' callable
        that creates a new instance of the desired content.
        """
        if not name[0].isupper():
            super().__setattr__(name, value)
            return

        # Set the property for the widget and add it to the properties dict.
        setattr(self._widget._native_properties, name, value())
        self._properties_dict[name] = value

        # Font properties in the widget base are set using this class, but the widget
        # may not require staging. So, only initialize the staging process if another
        # property has been explicitly staged.
        if not self._initialized:
            if name in self._font_properties:
                return
            else:
                self._initialized = True

        if not self._active:
            return

        # Only one clone of the widget exists at any given time.
        if not self._clone:
            self._clone = StagingClone(self._widget, self._properties_dict)

        self._clone.stage_property(name, value)

    def activate(self):
        self._active = True

        if self._initialized:
            self._clone = StagingClone(self._widget, self._properties_dict)

    def deactivate(self):
        self._active = False

        if self._clone:
            self._clone.remove()
