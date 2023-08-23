from __future__ import annotations

from toga.handlers import wrapped_handler

from .base import Widget


class OptionItem:
    """A tab of content in an OptionContainer."""

    def __init__(self, interface: OptionContainer, widget, index):
        self._interface = interface
        self._content = widget
        self._index = index

        widget.app = interface.app
        widget.window = interface.window

    @property
    def enabled(self) -> bool:
        "Is the panel of content available for selection?"
        return self._interface._impl.is_option_enabled(self.index)

    @enabled.setter
    def enabled(self, value):
        enable = bool(value)
        if not enable and self.index == self._interface._impl.get_current_tab_index():
            raise ValueError("The currently selected tab cannot be disabled.")

        self._interface._impl.set_option_enabled(self.index, enable)

    @property
    def text(self) -> str:
        "The label for the tab of content."
        return self._interface._impl.get_option_text(self.index)

    @text.setter
    def text(self, value):
        if value is None:
            raise ValueError("Item text cannot be None")

        text = str(value)
        if not text:
            raise ValueError("Item text cannot be blank")

        self._interface._impl.set_option_text(self.index, text)

    @property
    def index(self) -> int:
        """The index of the tab in the OptionContainer."""
        return self._index

    @property
    def content(self) -> Widget:
        """The content widget displayed in this tab of the OptionContainer."""
        return self._content


class OptionList:
    def __init__(self, interface):
        self.interface = interface
        self._options = []

    def __repr__(self):
        items = ", ".join(repr(option.text) for option in self)
        return f"<OptionList {items}>"

    def __getitem__(self, index: int | str | OptionItem) -> OptionItem:
        """Obtain a specific tab of content."""
        return self._options[self.index(index)]

    def __delitem__(self, index: int | str | OptionItem):
        """Same as :any:`remove`."""
        self.remove(index)

    def remove(self, index: int | str | OptionItem):
        """Remove the specified tab of content.

        The currently selected item cannot be deleted.
        """
        index = self.index(index)
        if index == self.interface._impl.get_current_tab_index():
            raise ValueError("The currently selected tab cannot be deleted.")

        self.interface._impl.remove_content(index)
        del self._options[index]
        # Update the index for each of the options
        # after the one that was removed.
        for option in self._options[index:]:
            option._index -= 1

        # Refresh the widget
        self.interface.refresh()

    def __len__(self) -> int:
        """The number of tabs of content in the OptionContainer."""
        return len(self._options)

    def index(self, value: str | int | OptionItem):
        """Find the index of the tab that matches the given value.

        :param value: The value to look for. An integer is returned as-is;
            if an :any:`OptionItem` is provided, that item's index is returned;
            any other value will be converted into a string, and the first
            tab with a label matching that string will be returned.
        :raises ValueError: If no tab matching the value can be found.
        """
        if isinstance(value, int):
            return value
        elif isinstance(value, OptionItem):
            return value.index
        else:
            try:
                return next(filter(lambda item: item.text == str(value), self)).index
            except StopIteration:
                raise ValueError(f"No tab named {value!r}")

    def append(self, text: str, widget: Widget, enabled: bool = True):
        """Add a new tab of content to the OptionContainer.

        :param text: The text label for the new tab
        :param widget: The content widget to use for the new tab.
        """
        self.insert(len(self), text, widget, enabled=enabled)

    def insert(
        self,
        index: int | str | OptionItem,
        text: str,
        widget: Widget,
        enabled: bool = True,
    ):
        """Insert a new tab of content to the OptionContainer at the specified index.

        :param index: The index where the new tab should be inserted.
        :param text: The text label for the new tab.
        :param widget: The content widget to use for the new tab.
        :param enabled: Should the new tab be enabled?
        """
        # Convert the index into an integer
        index = self.index(index)

        # Validate item text
        if text is None:
            raise ValueError("Item text cannot be None")

        text = str(text)
        if not text:
            raise ValueError("Item text cannot be blank")

        # Create an interface wrapper for the option.
        item = OptionItem(self.interface, widget, index)

        # Add the option to the list maintained on the interface,
        # and increment the index of all items after the one that was added.
        self._options.insert(index, item)
        for option in self._options[index + 1 :]:
            option._index += 1

        # Add the content to the implementation.
        # This will cause the native implementation to be created.
        self.interface._impl.add_content(index, text, widget._impl)

        # The option now exists on the implementation;
        # finalize the display properties that can't be resolved until the
        # implementation exists.
        self.interface.refresh()
        item.enabled = enabled


class OptionContainer(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        content: list[tuple[str, Widget]] | None = None,
        on_select: callable | None = None,
    ):
        """Create a new OptionContainer.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param content: The initial content to display in the OptionContainer. A list of
            2-tuples, each of which is the title for the option, and the content widget
            to display for that title.
        :param on_select: Initial :any:`on_select` handler.
        """
        super().__init__(id=id, style=style)
        self._content = OptionList(self)
        self.on_select = None

        self._impl = self.factory.OptionContainer(interface=self)

        if content:
            for text, widget in content:
                self.content.append(text, widget)

        self.on_select = on_select

    @property
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?

        OptionContainer widgets cannot be disabled; this property will always return
        True; any attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value):
        pass

    def focus(self):
        "No-op; OptionContainer cannot accept input focus"
        pass

    @property
    def content(self) -> OptionList:
        """The tabs of content currently managed by the OptionContainer."""
        return self._content

    @property
    def current_tab(self) -> OptionItem | None:
        """The currently selected tab of content, or ``None`` if there are no tabs.

        This property can also be set with an ``int`` index, or a ``str`` label.
        """
        index = self._impl.get_current_tab_index()
        if index is None:
            return None
        return self._content[index]

    @current_tab.setter
    def current_tab(self, value):
        index = self._content.index(value)
        if not self._impl.is_option_enabled(index):
            raise ValueError("A disabled tab cannot be made the current tab.")

        self._impl.set_current_tab_index(index)

    @Widget.app.setter
    def app(self, app):
        # Invoke the superclass property setter
        Widget.app.fset(self, app)

        # Also assign the app to the content in the container
        for item in self._content:
            item._content.app = app

    @Widget.window.setter
    def window(self, window):
        # Invoke the superclass property setter
        Widget.window.fset(self, window)

        # Also assign the window to the content in the container
        for item in self._content:
            item._content.window = window

    @property
    def on_select(self) -> callable:
        """The callback to invoke when a new tab of content is selected."""
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        self._on_select = wrapped_handler(self, handler)
