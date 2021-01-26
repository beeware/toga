from toga.handlers import wrapped_handler

from .base import Widget


class BaseOptionItem:
    def __init__(self, interface):
        self._interface = interface

    @property
    def enabled(self):
        return self._interface._impl.is_option_enabled(self.index)

    @enabled.setter
    def enabled(self, enabled):
        self._interface._impl.set_option_enabled(self.index, enabled)

    @property
    def label(self):
        return self._interface._impl.get_option_label(self.index)

    @label.setter
    def label(self, value):
        self._interface._impl.set_option_label(self.index, value)


class OptionItem(BaseOptionItem):
    """OptionItem is an interface wrapper for a tab on the OptionContainer"""
    def __init__(self, interface, widget, index):
        super().__init__(interface)
        self._content = widget
        self._index = index

    @property
    def index(self):
        return self._index

    @property
    def content(self):
        return self._content

    def refresh(self):
        self._content.refresh()


class CurrentOptionItem(BaseOptionItem):
    """CurrentOptionItem is a proxy for whichever tab is currently selected."""

    @property
    def index(self):
        return self._interface._impl.get_current_tab_index()

    @property
    def content(self):
        return self._interface.content[self.index].content

    def __add__(self, other):
        if not isinstance(other, int):
            raise ValueError("Cannot add non-integer value to OptionItem")
        return self._interface.content[self.index + other]

    def __sub__(self, other):
        if not isinstance(other, int):
            raise ValueError("Cannot add non-integer value to OptionItem")
        return self._interface.content[self.index - other]

    def refresh(self):
        self._interface.content[self.index]._content.refresh()


class OptionList:
    def __init__(self, interface):
        self.interface = interface
        self._options = []

    def __repr__(self):
        repr_optionlist = '{}([{}])'
        repr_items = ', '.join([
            '{}(title={})'.format(
                option.__class__.__name__,
                option.label)
            for option in self
        ])
        return repr_optionlist.format(self.__class__.__name__, repr_items)

    def __setitem__(self, index, option):
        self._options[index] = option
        option._index = index

    def __getitem__(self, index):
        return self._options[index]

    def __delitem__(self, index):
        self.interface._impl.remove_content(index)
        del self._options[index]
        # Update the index for each of the options
        # after the one that was removed.
        for option in self._options[index:]:
            option._index -= 1

    def __iter__(self):
        return iter(self._options)

    def __len__(self):
        return len(self._options)

    def append(self, label, widget, enabled=True):
        self._insert(len(self), label, widget, enabled)

    def insert(self, index, label, widget, enabled=True):
        self._insert(index, label, widget, enabled)

    def _insert(self, index, label, widget, enabled=True):
        # Create an interface wrapper for the option.
        option = OptionItem(self.interface, widget, index)

        # Add the option to the list maintained on the interface,
        # and increment the index of all items after the one that was added.
        self._options.insert(index, option)
        for option in self._options[index + 1:]:
            option._index += 1

        # Add the content to the implementation.
        # This will cause the native implementation to be created.
        self.interface._impl.add_content(label, widget._impl)

        # The option now exists on the implementation;
        # finalize the display properties that can't be resolved until the
        # implementation exists.
        widget.refresh()
        option.enabled = enabled


class OptionContainer(Widget):
    """ The option container widget.

    Args:
        id (str):   An identifier for this widget.
        style (:obj:`Style`): an optional style object.
            If no style is provided then a new one will be created for the widget.
        content (``list`` of ``tuple`` (``str``, :class:`toga.Widget`)):
            Each tuple in the list is composed of a title for the option and
            the widget tree that is displayed in the option.
    """
    class OptionException(ValueError):
        pass

    def __init__(self, id=None, style=None, content=None, on_select=None, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._on_select = None
        self._impl = self.factory.OptionContainer(interface=self)

        self.on_select = on_select
        self._content = OptionList(self)
        if content:
            for label, widget in content:
                self.add(label, widget)

        self.on_select = on_select
        # Create a proxy object to represent the currently selected item.
        self._current_tab = CurrentOptionItem(self)

    @property
    def content(self):
        """ The sub layouts of the `SplitContainer`.

        Returns:
            A OptionList ``list`` of :class:`toga.OptionItem`. Each element of the list
            is a sub layout of the `SplitContainer`

        Raises:
            ValueError: If the list is less than two elements long.
        """
        return self._content

    @property
    def current_tab(self):
        return self._current_tab

    @current_tab.setter
    def current_tab(self, current_tab):
        if isinstance(current_tab, str):
            try:
                current_tab = next(
                    filter(lambda item: item.label == current_tab, self.content)
                )
            except StopIteration:
                raise ValueError("No tab named {}".format(current_tab))
        if isinstance(current_tab, OptionItem):
            current_tab = current_tab.index
        self._impl.set_current_tab_index(current_tab)

    def _set_window(self, window):
        if self._content:
            for content in self._content:
                content._content.window = window

    def add(self, label, widget):
        """ Add a new option to the option container.

        Args:
            label (str): The label for the option.
            widget (:class:`toga.Widget`): The widget to add to the option.
        """
        widget.app = self.app
        widget.window = self.window

        self._content.append(label, widget)

    def remove(self, index):
        del self._content[index]

    def refresh_sublayouts(self):
        """Refresh the layout and appearance of this widget."""
        for widget in self._content:
            widget.refresh()

    @property
    def on_select(self):
        """ The callback function that is invoked when one of the options is selected.

        Returns:
            (``callable``) The callback function.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """
        Set the function to be executed on option selection

        :param handler:     callback function
        :type handler:      ``callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
