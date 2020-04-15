from toga.handlers import wrapped_handler

from .base import Widget


class OptionItem:
    def __init__(self, label, widget, enabled):
        self._interface = None
        self._index = None
        self._label = label
        self._widget = widget
        self._enabled = enabled

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
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        self._interface._impl.set_option_enabled(self._index, value)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self._interface._impl.set_label(self._index, value)

    def refresh(self):
        self._widget.refresh()


class OptionList:

    def __init__(self, interface):
        self.interface = interface
        self._options = []

    def __repr__(self):
        repr_list = ', '.join([
            '{}(title={})'.format(
                option.__class__.__name__,
                option.label)
            for option in self
        ])
        return '[{}]'.format(repr_list)

    def __setitem__(self, index, option):
        option.index = index
        option.interface = self.inteface
        self._options[index] = option

    def __getitem__(self, index):
        return self._options[index]

    def __delitem__(self, index):
        del self._options[index]
        self._update_indices()

    def __iter__(self):
        return iter(self._options)

    def __len__(self):
        return len(self._options)

    def append(self, label, widget, enabled=True):
        self._insert(len(self), label, widget, enabled)

    def insert(self, index, label, widget, enabled=True):
        self._insert(index, label, widget, enabled)

    def _insert(self, index, label, widget, enabled=True):
        option = OptionItem(label, widget, enabled)
        option.interface = self.interface
        self._options.insert(index, option)
        self._update_indices()

    def _update_indices(self):
        # ensure that all option have a corrrect index
        for i, option in enumerate(self._options):
            option.index = i


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
            A ``list`` of :class:`toga.Widget`. Each element of the list
            is a sub layout of the `SplitContainer`

        Raises:
            ValueError: If the list is less than two elements long.
        """
        return self._content

    def _set_window(self, window):
        if self._content:
            for content in self._content:
                content.window = window

    def add(self, label, widget):
        """ Add a new option to the option container.

        Args:
            label (str): The label for the option.
            widget (:class:`toga.Widget`): The widget to add to the option.
        """
        widget.app = self.app
        widget.window = self.window

        self._content.append(label, widget)
        self._impl.add_content(label, widget._impl)
        widget.refresh()

    def remove(self, index):
        disabled_siblings = not any(
            [
                opt.enabled for opt in self._content
                if opt != self._content[index]
            ]
        )

        if len(self._content) == 1 or disabled_siblings:
            # if sibling options are disabled or there is
            # only one tab in the option container, don't allow
            # remove tab.
            return
        else:
            self._impl.remove_content(index)
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
