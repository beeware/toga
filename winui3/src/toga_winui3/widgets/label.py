from travertino.constants import CENTER, JUSTIFY, LEFT, RIGHT
from travertino.size import at_least
from win32more.Microsoft.UI.Xaml import (
    HorizontalAlignment,
    TextAlignment,
    VerticalAlignment,
)
from win32more.Microsoft.UI.Xaml.Controls import Grid, TextBlock

from ..colors import native_brush
from ..libs.misc import column_definition_star, row_definition_auto
from ..libs.nativeevents import EventsHandledMixin
from .base import Widget
from .properties.native import NativeProperties
from .properties.staged import StagedProperties


class LabelText(EventsHandledMixin):
    def __init__(self, label):
        """A class the handles the text part of the `Label` widget.

        :param label: The `Label` widget itself.
        """
        self._label = label

        # Setting native_cls defines self.native and means that events are managed by
        # the nativeevents module.
        self.native_cls = TextBlock

        # LabelText cannot receive input focus, so remove it from the tab sequence.
        self.native.IsTabStop = False

        self._native_properties = NativeProperties(self)
        self._staged_properties = StagedProperties(self)

        # Initial minimum sizes are 0 because the staged properties are delayed, and
        # this allows to the widget to be sized up.
        self._min_width = 0
        self._min_height = 0

        Grid.SetRow(self.native, 0)
        Grid.SetColumn(self.native, 0)
        label.native.Children.Append(self.native)

        self.native.HorizontalAlignment = HorizontalAlignment.Stretch
        self.native.VerticalAlignment = VerticalAlignment.Stretch

    @property
    def container(self):
        return self._label.container

    def rehint(self):
        self._label.rehint()


class Label(Widget):
    """The WinUI 3 `Label` widget implementation.

    This widget is necessarily split into two parts because the WinUI 3 class the widget
    is based on, `Microsoft.UI.Xaml.Controls.TextBlock`, doesn't have a background.
    """

    def create(self):
        # Setting native_cls defines self.native and means that events are managed by
        # the nativeevents module.
        self.native_cls = Grid

        # Label cannot receive input focus, so remove it from the tab sequence.
        self.native.IsTabStop = False

        self._background_properties = self._native_properties

        self.native.ColumnDefinitions.Append(column_definition_star(1))
        self.native.RowDefinitions.Append(row_definition_auto())

        self.label_text = LabelText(self)
        self._native_properties = self.label_text._native_properties
        self._staged_properties = self.label_text._staged_properties

        self._text = ""

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self._staged_properties.Text = self.text

    def text(self):
        return self._text

    ####################################################################################
    # Overrides of methods called by the Toga style applicator.
    ####################################################################################

    def set_background_color(self, color):
        self._background_properties.Background = native_brush(color)

    def set_text_align(self, alignment):
        property_dict = {
            CENTER: "Center",
            JUSTIFY: "Justify",
            LEFT: "Left",
            RIGHT: "Right",
        }
        property = property_dict[alignment]
        native_alignment = getattr(TextAlignment, property)

        self._native_properties.TextAlignment = native_alignment

    ####################################################################################
    # Overrides of other methods called by the Toga core interface.
    ####################################################################################

    def get_enabled(self):
        # Neither TextBlock nor Grid has the IsEnabled property.
        return True

    def set_enabled(self, value):
        # Neither TextBlock nor Grid has the IsEnabled property.
        pass

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.label_text._min_width)
        self.interface.intrinsic.height = self.label_text._min_height
