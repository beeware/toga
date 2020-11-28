from toga.handlers import wrapped_handler

from .base import Widget


class OptionItem:
    def __init__(self, widget):
        self._interface = None
        self._index = None
        self._widget = widget

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, interface):
        self._interface = interface

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

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

    @property
    def widget(self):
        return self._widget

    def refresh(self):
        self._widget.refresh()

    def __add__(self, other):
        if not isinstance(other, int):
            raise ValueError("Cannot add non-integer value to OptionItem")
        return self.interface.content[self.index + other]

    def __sub__(self, other):
        if not isinstance(other, int):
            raise ValueError("Cannot add non-integer value to OptionItem")
        return self.interface.content[self.index - other]


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

    def __getitem__(self, index):
        self._options[index].index = index
        return self._options[index]

    def __delitem__(self, index):
        self.interface._impl.remove_content(index)
        del self._options[index]

    def __iter__(self):
        for i, option in enumerate(self._options):
            # sync options index attr
            option.index = i
        return iter(self._options)

    def __len__(self):
        return len(self._options)

    def append(self, label, widget, enabled=True):
        self._insert(len(self), label, widget, enabled)

    def insert(self, index, label, widget, enabled=True):
        self._insert(index, label, widget, enabled)

    def _insert(self, index, label, widget, enabled=True):
        # Create an interface wrapper for the option.
        option = OptionItem(widget)
        option.interface = self.interface
        option.index = index

        # Add the option to the list maintained on the interface
        self._options.insert(index, option)

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
        return self.content[self._impl.get_current_tab_index()]

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
                content.widget.window = window

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
