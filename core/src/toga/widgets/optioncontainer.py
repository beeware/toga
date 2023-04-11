import warnings

from toga.handlers import wrapped_handler

from .base import Widget

# BACKWARDS COMPATIBILITY: a token object that can be used to differentiate
# between an explicitly provided ``None``, and an unspecified value falling
# back to a default.
NOT_PROVIDED = object()


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
    def text(self):
        return self._interface._impl.get_option_text(self.index)

    @text.setter
    def text(self, value):
        self._interface._impl.set_option_text(self.index, value)

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################
    # label replaced with text
    @property
    def label(self):
        """OptionItem text.

        **DEPRECATED: renamed as text**

        Returns:
            The OptionItem text as a ``str``
        """
        warnings.warn(
            "OptionItem.label has been renamed OptionItem.text", DeprecationWarning
        )
        return self.text

    @label.setter
    def label(self, label):
        warnings.warn(
            "OptionItem.label has been renamed OptionItem.text", DeprecationWarning
        )
        self.text = label

    ######################################################################
    # End backwards compatibility.
    ######################################################################


class OptionItem(BaseOptionItem):
    """OptionItem is an interface wrapper for a tab on the OptionContainer."""

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
        repr_optionlist = "{}([{}])"
        repr_items = ", ".join(
            [f"{option.__class__.__name__}(title={option.text})" for option in self]
        )
        return repr_optionlist.format(self.__class__.__name__, repr_items)

    # def __setitem__(self, index, option):
    #     TODO: replace tab content at the given index.
    #     self._options[index] = option
    #     option._index = index

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

    def append(
        self,
        text=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for
        # `label`` is removed
        widget=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for
        # `label`` is removed
        label=None,  # DEPRECATED!
        enabled=True,
    ):
        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################
        # When deleting this block, also delete the NOT_PROVIDED
        # placeholder, and replace its usage in default values.
        missing_arguments = []

        # label replaced with text
        if label is not None:
            if text is not NOT_PROVIDED:
                raise ValueError(
                    "Cannot specify both `label` and `text`; "
                    "`label` has been deprecated, use `text`"
                )
            else:
                warnings.warn("label has been renamed text", DeprecationWarning)
                text = label
        elif text is NOT_PROVIDED:
            missing_arguments.append("text")

        if widget is NOT_PROVIDED:
            missing_arguments.append("widget")

        # This would be raised by Python itself; however, we need to use a placeholder
        # value as part of the migration from text->value.
        if len(missing_arguments) == 1:
            raise TypeError(
                f"OptionList.append missing 1 required positional argument: '{missing_arguments[0]}'"
            )
        elif len(missing_arguments) > 1:
            raise TypeError(
                "OptionList.append missing {} required positional arguments: {}".format(
                    len(missing_arguments),
                    " and ".join([f"'{name}'" for name in missing_arguments]),
                )
            )

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        self._insert(len(self), text, widget, enabled)

    def insert(
        self,
        index,
        text=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for
        # `label`` is removed
        widget=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for
        # `label`` is removed
        label=None,  # DEPRECATED!
        enabled=True,
    ):
        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################
        # When deleting this block, also delete the NOT_PROVIDED
        # placeholder, and replace its usage in default values.
        missing_arguments = []

        # label replaced with text
        if label is not None:
            if text is not NOT_PROVIDED:
                raise ValueError(
                    "Cannot specify both `label` and `text`; "
                    "`label` has been deprecated, use `text`"
                )
            else:
                warnings.warn("label has been renamed text", DeprecationWarning)
                text = label
        elif text is NOT_PROVIDED:
            missing_arguments.append("text")

        if widget is NOT_PROVIDED:
            missing_arguments.append("widget")

        # This would be raised by Python itself; however, we need to use a placeholder
        # value as part of the migration from text->value.
        if len(missing_arguments) == 1:
            raise TypeError(
                f"OptionList.insert missing 1 required positional argument: '{missing_arguments[0]}'"
            )
        elif len(missing_arguments) > 1:
            raise TypeError(
                "OptionList.insert missing {} required positional arguments: {}".format(
                    len(missing_arguments),
                    " and ".join([f"'{name}'" for name in missing_arguments]),
                )
            )

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        self._insert(index, text, widget, enabled)

    def _insert(self, index, text, widget, enabled=True):
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
        widget.refresh()
        item.enabled = enabled


class OptionContainer(Widget):
    """The option container widget.

    Args:
        id (str):   An identifier for this widget.
        style (:obj:`Style`): an optional style object.
            If no style is provided then a new one will be created for the widget.
        content (``list`` of ``tuple`` (``str``, :class:`~toga.widgets.base.Widget`)):
            Each tuple in the list is composed of a title for the option and
            the widget tree that is displayed in the option.
    """

    class OptionException(ValueError):
        pass

    def __init__(
        self,
        id=None,
        style=None,
        content=None,
        on_select=None,
        factory=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style)
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self._content = OptionList(self)
        self._on_select = None
        self._impl = self.factory.OptionContainer(interface=self)

        self.on_select = on_select
        if content:
            for text, widget in content:
                self.add(text, widget)

        self.on_select = on_select
        # Create a proxy object to represent the currently selected item.
        self._current_tab = CurrentOptionItem(self)

    @property
    def content(self):
        """The sub layouts of the :class:`OptionContainer`.

        Returns:
            A OptionList ``list`` of :class:`~toga.OptionItem`. Each element of the list
            is a sub layout of the `OptionContainer`

        Raises:
            :exp:`ValueError`: If the list is less than two elements long.
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
                    filter(lambda item: item.text == current_tab, self.content)
                )
            except StopIteration:
                raise ValueError(f"No tab named {current_tab}")
        if isinstance(current_tab, OptionItem):
            current_tab = current_tab.index
        self._impl.set_current_tab_index(current_tab)

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

    def add(
        self,
        text=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for
        # `label`` is removed
        widget=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for
        # `label`` is removed
        label=None,  # DEPRECATED!
    ):
        """Add a new option to the option container.

        Args:
            text (str): The text for the option.
            widget (:class:`~toga.widgets.base.Widget`): The widget to add to the option.
        """
        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################
        # When deleting this block, also delete the NOT_PROVIDED
        # placeholder, and replace its usage in default values.
        missing_arguments = []

        # label replaced with text
        if label is not None:
            if text is not NOT_PROVIDED:
                raise ValueError(
                    "Cannot specify both `label` and `text`; "
                    "`label` has been deprecated, use `text`"
                )
            else:
                warnings.warn("label has been renamed text", DeprecationWarning)
                text = label
        elif text is NOT_PROVIDED:
            missing_arguments.append("text")

        if widget is NOT_PROVIDED:
            missing_arguments.append("widget")

        # This would be raised by Python itself; however, we need to use a placeholder
        # value as part of the migration from text->value.
        if len(missing_arguments) == 1:
            raise TypeError(
                f"OptionContainer.add missing 1 required positional argument: '{missing_arguments[0]}'"
            )
        elif len(missing_arguments) > 1:
            raise TypeError(
                "OptionContainer.add missing {} required positional arguments: {}".format(
                    len(missing_arguments),
                    " and ".join([f"'{name}'" for name in missing_arguments]),
                )
            )

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        widget.app = self.app
        widget.window = self.window

        self._content.append(text, widget)

    def insert(self, index, text, widget):
        """Insert a new option at the specified index.

        Args:
            index (int): Index for the option.
            text (str): The text for the option.
            widget (:class:`~toga.widgets.base.Widget`): The widget to add to the option.
        """
        widget.app = self.app
        widget.window = self.window

        self._content.insert(index, text, widget)

    def remove(self, index):
        del self._content[index]

    def refresh_sublayouts(self):
        """Refresh the layout and appearance of this widget."""
        for widget in self._content:
            widget.refresh()

    @property
    def on_select(self):
        """The callback function that is invoked when one of the options is
        selected.

        Returns:
            (``Callable``) The callback function.
        """
        return self._on_select

    @on_select.setter
    def on_select(self, handler):
        """Set the function to be executed on option selection.

        :param handler:     callback function
        :type handler:      ``Callable``
        """
        self._on_select = wrapped_handler(self, handler)
        self._impl.set_on_select(self._on_select)
