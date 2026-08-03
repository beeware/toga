from abc import ABC, abstractmethod

from travertino.size import at_least
from win32more.Microsoft.UI.Xaml import FocusState, Visibility
from win32more.Microsoft.UI.Xaml.Controls import Canvas

from ..colors import native_brush
from ..libs.nativeevents import EventsHandledMixin
from .properties.native import NativeProperties
from .properties.staged import StagedProperties


class Widget(EventsHandledMixin, ABC):
    ####################################################################################
    # Widget creation.
    ####################################################################################

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.native = None

        self._container = None

        self._native_properties = NativeProperties(self)
        self._staged_properties = StagedProperties(self)

        self._min_width = self.interface._MIN_WIDTH
        self._min_height = self.interface._MIN_HEIGHT

        self.create()

    @abstractmethod
    def create(self): ...

    def set_app(self, app):
        # Everything is already handled by the Toga core interface.
        pass

    def set_window(self, window):
        # Everything is already handled by the Toga core interface.
        pass

    ####################################################################################
    # Methods relating to the container.
    ####################################################################################

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self._container:
            self._container.widgets.remove(self)

        self._container = container
        if container:
            container.widgets.add(self)
            self._staged_properties.refresh()

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    ####################################################################################
    # Methods relating to children.
    ####################################################################################

    def add_child(self, child):
        child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    ####################################################################################
    # Methods called by the Toga style applicator.
    ####################################################################################

    def set_background_color(self, color):
        self._native_properties.Background = native_brush(color)

    def set_bounds(self, x, y, width, height):
        self.native.Width = width
        self.native.Height = height
        Canvas.SetLeft(self.native, x)
        Canvas.SetTop(self.native, y)

    def set_color(self, color):
        self._native_properties.Foreground = native_brush(color)

    def set_font(self, font):
        native_font = font._impl.native
        staged_properties = self._staged_properties

        staged_properties.FontFamily = native_font.FontFamily
        staged_properties.FontSize = native_font.FontSize
        staged_properties.FontStyle = native_font.FontStyle
        staged_properties.FontWeight = native_font.FontWeight

    def set_hidden(self, hidden):
        state = Visibility.Collapsed if hidden else Visibility.Visible
        self.native.Visibility = state

    def set_text_align(self, alignment):
        # Where appropriate, this is implement on a widget by widget basis.
        pass

    ####################################################################################
    # Other methods called by the Toga core interface.
    ####################################################################################

    def get_enabled(self):
        return self.native.IsEnabled

    def set_enabled(self, value):
        self.native.IsEnabled = value

    @property
    def has_focus(self):
        return self.native.FocusState != FocusState.Unfocused

    def focus(self):
        if not self.has_focus:
            self.native.Focus(FocusState.Programmatic)

    def get_tab_index(self):
        return self.native.TabIndex

    def set_tab_index(self, tab_index):
        self.native.TabIndex = tab_index

    def refresh(self):
        self.rehint()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self._min_width)
        self.interface.intrinsic.height = at_least(self._min_height)
