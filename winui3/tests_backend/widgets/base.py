from unittest.mock import Mock

from pytest import approx
from win32more.Microsoft.UI.Xaml import FocusState, Visibility
from win32more.Windows.Foundation import Rect
from win32more.Windows.Win32.UI.Input.KeyboardAndMouse import GetFocus

import toga

from ..fonts import FontMixin
from ..probe import BaseProbe
from .properties import brush_to_color


class SimpleProbe(BaseProbe, FontMixin):
    invalid_size_while_hidden = False
    supports_tab_index = True

    def __init__(self, widget):
        self.app = widget.app
        self.widget = widget
        self.impl = widget._impl
        super().__init__(self.impl.native)

        # Check that the native class has been instantiated using events_handled()
        assert self.impl.native_cls == self.native_class
        assert type(self.native).__name__ == self.native_class.__name__ + "Handled"

    def assert_container(self, container):
        assert self.widget._impl.container is container._impl.container
        assert self.native.Parent is not None

        parent_1 = container._impl.container.native
        parent_2_raw = self.native.Parent
        parent_2 = type(parent_1)(value=parent_2_raw.value)

        # Confirm that parent_1 and parent_2 are the same WinUI 3 object. The python
        # objects have different memory addresses, so change the Name property on one
        # and confirm that the other has the same name.
        parent_1.Name = "Parent Name"
        assert parent_1.Name == parent_2.Name == "Parent Name"

        parent_2.Name = "New Parent Name"
        assert parent_1.Name == parent_2.Name == "New Parent Name"

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.Parent is None

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.Parent is not None

        # size and position is as expected.
        assert (self.width, self.height) == approx(size, abs=1)
        assert (self.x, self.y) == approx(position, abs=1)

    def get_hwnd(self, native):
        focus_set = native.Focus(FocusState.Programmatic)
        if not focus_set:
            return -1

        return GetFocus()

    @property
    def _hwnd(self):
        return self.get_hwnd(self.impl.native)

    @property
    def _bounds_screen_coords(self):
        """The bounding Rect(X, Y, Width, Height) of self.native in screen coords."""
        # Get the top left point in coordinates with respect to the XamlRoot element
        # learn.microsoft.com/windows/windows-app-sdk/api/winrt/microsoft.ui.xaml.uielement.transformtovisual # noqa E501
        transform = self.native.TransformToVisual(None)
        bounds = transform.TransformBounds(Rect(0, 0, self.width, self.height))

        # Note that self.native must be added to the visual tree for XamlRoot to exist.
        converter = self.native.XamlRoot.CoordinateConverter
        return converter.ConvertLocalToScreenWithRect(bounds)

    @property
    def _midpoint_screen_coords(self):
        bounds = self._bounds_screen_coords
        return (int(bounds.X + bounds.Width / 2), int(bounds.Y + bounds.Height / 2))

    @property
    def width(self):
        return self.native.ActualWidth

    def assert_width(self, min_width, max_width):
        assert min_width <= self.width <= max_width, (
            f"Width ({self.width}) not in range ({min_width}, {max_width})"
        )

    @property
    def height(self):
        return self.native.ActualHeight

    def assert_height(self, min_height, max_height):
        assert min_height <= self.height <= max_height, (
            f"Height ({self.height}) not in range ({min_height}, {max_height})"
        )

    @property
    def x(self):
        return self.native.ActualOffset.X

    @property
    def y(self):
        return self.native.ActualOffset.Y

    @property
    def is_hidden(self):
        return self.native.Visibility == Visibility.Collapsed

    @property
    def color(self):
        return brush_to_color(self.native.Foreground)

    @property
    def background_color(self):
        return brush_to_color(self.native.Background)

    @property
    def enabled(self):
        return self.native.IsEnabled

    @property
    def shrink_on_resize(self):
        return True

    @property
    def has_focus(self):
        return self.native.FocusState != FocusState.Unfocused

    def assert_native_properties(self):
        """Test whether native properties are reset correctly."""

        # Create a local alias for the native property handler.
        native_properties = self.impl._native_properties

        # Set an unused native dependency property.
        old_value = self.native.Opacity
        native_properties.Opacity = 0.5

        assert self.native.Opacity != old_value

        # Test that the property is reset by setting None.
        native_properties.Opacity = None

        assert self.native.Opacity == old_value

        # Test a native non-dependency property.
        assert self.native.Resources is not None

        native_properties.Resources = None

        # Setting a non-dependency native property to None should result in the property
        # being None.
        assert self.native.Resources is None

    async def assert_staged_properties_containerless(self, staging_area):
        """Test that there is no staging for a widget with no container."""
        mock = Mock()

        def callback_mock(sender, args):
            mock()

        await self.redraw("Creating Label widget.")

        label = toga.Label("Label text")
        staged_properties = label._impl._staged_properties

        # After creating label, but not adding it to a container, there should be no
        # properties being staged.
        assert len(staging_area._staging_clones) == 0
        assert staged_properties._clone is None

        # Adding the label as a child should initiate the label properties being staged.
        self.widget.add(label)
        label_clone = staging_area._staging_clones[0]
        label_clone.native.event_handler.SizeChanged += callback_mock

        assert len(staging_area._staging_clones) == 1
        assert staged_properties._clone == label_clone

        # Immediately remove the label from the widget. The staging process should be
        # removed.
        self.widget.remove(label)
        assert len(staging_area._staging_clones) == 0
        assert staged_properties._clone is None

        # Since the label_clone has been removed from the visual tree, the native
        # SizeChanged event should not fire.
        await self.redraw("Label added to and removed from a container.", delay=0.1)
        mock.assert_not_called()
        mock.reset_mock()

    async def assert_staged_properties_same_value(self, staging_area):
        """Staging property with the same value is a no-op or triggers SizeChanged."""
        # Create a widget and set some style properties.
        properties = {
            "text": "Label text",
            "font_family": "serif",
            "font_size": 20,
            "font_style": "italic",
            "font_weight": "bold",
        }

        def set_property(label, name):
            if name == "text":
                setattr(label, name, properties[name])
            else:
                setattr(label.style, name, properties[name])

        label = toga.Label(text="")
        for name in properties:
            set_property(label, name)

        self.widget.add(label)

        await self.redraw("Label widget created and added to a container.")
        # Staging should be complete.
        assert len(staging_area._staging_clones) == 0

        for name in properties:
            set_property(label, name)

            if name == "text":
                # For `text` the staging process starts and completes.
                assert len(staging_area._staging_clones) == 1

                await self.redraw(f"Label.{name} has re-set to the same value.")
                assert len(staging_area._staging_clones) == 0
            else:
                # For font style attributes the staging process is a no-op.
                assert len(staging_area._staging_clones) == 0

    async def assert_staged_properties_events(self, staging_area):
        await self.redraw("Creating Label widget.")
        label = toga.Label("Label text")
        self.widget.add(label)

        # Get the widget clone from the staging process, and assert that only one
        # SizeChanged callback has been created.
        label_clone = staging_area._staging_clones[0]
        assert label_clone._latest_callback_id == 1

        # Save the current SizeChanged callback.
        native_event = label_clone.native.event_handler.SizeChanged
        _, callback = next(iter(native_event._registry.values()))

        # Staging another property creates a new callback and clears the old.
        label.style.font_weight = "bold"
        _, new_callback = next(iter(native_event._registry.values()))
        assert len(staging_area._staging_clones) == 1
        assert label_clone._latest_callback_id > 1
        assert new_callback != callback

        # Simluate the old callback being called. The could occur if it was already in
        # the queue when the new property was staged. Assert that the staging process
        # is not completed by this call.
        callback(sender=None, args=None)
        assert len(staging_area._staging_clones) == 1

        # Assert that the staging process is finished after a small wait.
        await self.redraw("Staging process completed with extra callback.", delay=0.1)
        assert len(staging_area._staging_clones) == 0

        # Simulate a callback after the staging process is finished. This can occur if
        # a callback was already in the queue when the widget was removed from its
        # container. This call should not result in any errors.
        new_callback(sender=None, args=None)

    async def assert_staged_properties(self):
        """Test whether staged properties are created and deleted correctly."""
        staging_area = self.widget._impl.container.staging_area

        await self.assert_staged_properties_containerless(staging_area)
        await self.assert_staged_properties_same_value(staging_area)
        await self.assert_staged_properties_events(staging_area)

    async def assert_backend_specific_properties(self):
        self.assert_native_properties()

        await self.assert_staged_properties()

    def assert_tab_index(self, widget, other):
        # Unset WinUI 3 tab indices default to Int32_MaxValue.
        Int32_MaxValue = 2**31 - 1
        assert widget.tab_index == Int32_MaxValue
        assert other.tab_index == Int32_MaxValue

        widget.tab_index = 4
        other.tab_index = 2
        assert widget.tab_index == 4
        assert other.tab_index == 2
