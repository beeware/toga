from __future__ import annotations

import sys
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Protocol, overload

import toga
from toga.handlers import wrapped_handler
from toga.platform import get_platform_factory

from .base import StyleT, Widget

if TYPE_CHECKING:
    if sys.version_info < (3, 10):
        from typing_extensions import TypeAlias
    else:
        from typing import TypeAlias
    from toga.icons import IconContentT

    OptionContainerContentT: TypeAlias = (
        tuple[str, Widget]
        | tuple[str, Widget, IconContentT | None]
        | tuple[str, Widget, IconContentT | None, bool]
        | toga.OptionItem
    )


class OnSelectHandler(Protocol):
    def __call__(self, widget: OptionContainer, /, **kwargs: Any) -> None:
        """A handler that will be invoked when a new tab is selected in the OptionContainer.

        :param widget: The OptionContainer that had a selection change.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class OptionItem:
    def __init__(
        self,
        text: str,
        content: Widget,
        *,
        icon: IconContentT | None = None,
        enabled: bool = True,
    ):
        """A tab of content in an OptionContainer.

        :param text: The text label for the new tab.
        :param content: The content widget to use for the new tab.
        :param icon: The :any:`icon content <IconContentT>` to use to represent the tab.
        :param enabled: Should the new tab be enabled?
        """
        if content is None:
            raise ValueError("Content widget cannot be None.")

        self._content = content
        # These properties only exist while the item is in construction. Once the tab is
        # actual content, these attributes will be deleted and the native implementation
        # will become the source of truth. Initially prime the attributes with None (so
        # that the attribute exists), then use the setter to enforce validation on the
        # provided values.
        self._text: str = None
        self._icon: toga.Icon = None
        self._enabled: bool = None

        self.text = text
        self.icon = icon
        self.enabled = enabled

        # Prime the attributes for properties that will be set when the OptionItem is
        # set as content.
        self._interface: OptionContainer = None
        self._index: int = None

    @property
    def interface(self) -> OptionContainer:
        """The OptionContainer that contains this tab.

        Returns ``None`` if the tab isn't currently part of an OptionContainer.
        """
        return self._interface

    @property
    def enabled(self) -> bool:
        """Is the panel of content available for selection?"""
        try:
            return self._enabled
        except AttributeError:
            return self._interface._impl.is_option_enabled(self.index)

    @enabled.setter
    def enabled(self, value: object) -> None:
        enable = bool(value)
        if hasattr(self, "_enabled"):
            self._enabled = enable
        else:
            if (
                not enable
                and self.index == self._interface._impl.get_current_tab_index()
            ):
                raise ValueError("The currently selected tab cannot be disabled.")

            self._interface._impl.set_option_enabled(self.index, enable)

    @property
    def text(self) -> str:
        """The label for the tab of content."""
        try:
            return self._text
        except AttributeError:
            return self._interface._impl.get_option_text(self.index)

    @text.setter
    def text(self, value: object) -> None:
        if value is None:
            raise ValueError("Item text cannot be None")

        text = str(value)
        if not text:
            raise ValueError("Item text cannot be blank")

        if hasattr(self, "_text"):
            self._text = text
        else:
            self._interface._impl.set_option_text(self.index, text)

    @property
    def icon(self) -> toga.Icon:
        """The Icon for the tab of content.

        Can be specified as any valid :any:`icon content <IconContentT>`.

        If the platform does not support the display of icons, this property
        will return ``None`` regardless of any value provided.
        """
        try:
            return self._icon
        except AttributeError:
            return self._interface._impl.get_option_icon(self.index)

    @icon.setter
    def icon(self, icon_or_name: IconContentT | None) -> None:
        if get_platform_factory().OptionContainer.uses_icons:
            if icon_or_name is None:
                icon = None
            elif isinstance(icon_or_name, toga.Icon):
                icon = icon_or_name
            else:
                icon = toga.Icon(icon_or_name)

            if hasattr(self, "_icon"):
                self._icon = icon
            else:
                self._interface._impl.set_option_icon(self.index, icon)

    @property
    def index(self) -> int | None:
        """The index of the tab in the OptionContainer.

        Returns ``None`` if the tab isn't currently part of an OptionContainer.
        """
        return self._index

    @property
    def content(self) -> Widget:
        """The content widget displayed in this tab of the OptionContainer."""
        return self._content

    def _preserve_option(self) -> None:
        # Move the ground truth back to the OptionItem instance
        self._text = self.text
        self._icon = self.icon
        self._enabled = self.enabled

        # Clear
        self._index = None
        self._interface = None

    def _add_as_option(self, index: int, interface: OptionContainer) -> None:
        text = self._text
        del self._text

        icon = self._icon
        del self._icon

        enabled = self._enabled
        del self._enabled

        self._index = index
        self._interface = interface
        interface._impl.add_option(index, text, self.content._impl, icon)

        # The option now exists on the implementation; finalize the display properties
        # that can't be resolved until the implementation exists.
        interface.refresh()
        self.enabled = enabled


class OptionList:
    def __init__(self, interface: Any):
        self.interface = interface
        self._options: list[OptionItem] = []

    def __repr__(self) -> str:
        items = ", ".join(repr(option.text) for option in self)
        return f"<OptionList {items}>"

    def __getitem__(self, index: int | str | OptionItem) -> OptionItem:
        """Obtain a specific tab of content."""
        return self._options[self.index(index)]

    def __delitem__(self, index: int | str | OptionItem) -> None:
        """Same as :any:`remove`."""
        self.remove(index)

    def remove(self, index: int | str | OptionItem) -> None:
        """Remove the specified tab of content.

        The currently selected item cannot be deleted.

        :param index: The index where the new tab should be inserted.
        """
        index = self.index(index)
        if index == self.interface._impl.get_current_tab_index():
            raise ValueError("The currently selected tab cannot be deleted.")

        # Ensure that the current ground truth of the item to be deleted is preserved as
        # attributes on the item
        deleted_item = self._options[index]
        deleted_item._preserve_option()

        self.interface._impl.remove_option(index)
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

    def index(self, value: str | int | OptionItem) -> int:
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

    @overload
    def append(
        self,
        text_or_item: OptionItem,
    ) -> None: ...

    @overload
    def append(
        self,
        text_or_item: str,
        content: Widget,
        *,
        icon: IconContentT | None = None,
        enabled: bool | None = True,
    ) -> None: ...

    def append(
        self,
        text_or_item: str | OptionItem,
        content: Widget | None = None,
        *,
        icon: IconContentT | None = None,
        enabled: bool | None = None,
    ) -> None:
        """Add a new tab of content to the OptionContainer.

        The new tab can be specified as an existing :any:`OptionItem` instance, or by
        specifying the full details of the new tab of content. If an :any:`OptionItem`
        is provided, specifying ``content``, ``icon`` or ``enabled`` will raise an
        error.

        :param text_or_item: An :any:`OptionItem`; or, the text label for the new tab.
        :param content: The content widget to use for the new tab.
        :param icon: The :any:`icon content <IconContentT>` to use to represent the tab.
        :param enabled: Should the new tab be enabled? (Default: ``True``)
        """
        self.insert(len(self), text_or_item, content, icon=icon, enabled=enabled)

    @overload
    def insert(
        self,
        index: int | str | OptionItem,
        text_or_item: OptionItem,
    ) -> None: ...

    @overload
    def insert(
        self,
        index: int | str | OptionItem,
        text_or_item: str,
        content: Widget,
        *,
        icon: IconContentT | None = None,
        enabled: bool | None = True,
    ) -> None: ...

    def insert(
        self,
        index: int | str | OptionItem,
        text_or_item: str | OptionItem,
        content: Widget | None = None,
        *,
        icon: IconContentT | None = None,
        enabled: bool | None = None,
    ) -> None:
        """Insert a new tab of content to the OptionContainer at the specified index.

        The new tab can be specified as an existing :any:`OptionItem` instance, or by
        specifying the full details of the new tab of content. If an :any:`OptionItem`
        is provided, specifying ``content``, ``icon`` or ``enabled`` will raise an
        error.

        :param index: The index where the new tab should be inserted.
        :param text_or_item: An :any:`OptionItem`; or, the text label for the new tab.
        :param content: The content widget to use for the new tab.
        :param icon: The :any:`icon content <IconContentT>` to use to represent the tab.
        :param enabled: Should the new tab be enabled? (Default: ``True``)
        """
        if isinstance(text_or_item, OptionItem):
            if content is not None:
                raise ValueError(
                    "Cannot specify content if using an OptionItem instance."
                )
            if icon is not None:
                raise ValueError("Cannot specify icon if using an OptionItem instance.")
            if enabled is not None:
                raise ValueError(
                    "Cannot specify enabled if using an OptionItem instance."
                )
            item = text_or_item
        else:
            # Create an interface wrapper for the option.
            item = OptionItem(
                text_or_item,
                content,
                icon=icon,
                enabled=enabled if enabled is not None else True,
            )

        # Convert the index into an integer, and assign to the item.
        index = self.index(index)

        # Add the option to the list maintained on the interface,
        # and increment the index of all items after the one that was added.
        self._options.insert(index, item)
        for option in self._options[index + 1 :]:
            option._index += 1

        # Add the content to the implementation.
        # This will cause the native implementation to be created.
        item._add_as_option(index, self.interface)


class OptionContainer(Widget):
    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        content: Iterable[OptionContainerContentT] | None = None,
        on_select: toga.widgets.optioncontainer.OnSelectHandler | None = None,
    ):
        """Create a new OptionContainer.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param content: The initial :any:`OptionContainer content
            <OptionContainerContentT>` to display in the OptionContainer.
        :param on_select: Initial :any:`on_select` handler.
        """
        super().__init__(id=id, style=style)
        self._content = OptionList(self)
        self.on_select = None

        self._impl = self.factory.OptionContainer(interface=self)

        if content is not None:
            for item in content:
                if isinstance(item, OptionItem):
                    self.content.append(item)
                else:
                    if len(item) == 2:
                        text, widget = item
                        icon = None
                        enabled = True
                    elif len(item) == 3:
                        text, widget, icon = item
                        enabled = True
                    elif len(item) == 4:
                        text, widget, icon, enabled = item
                    else:
                        raise ValueError(
                            "Content items must be an OptionItem instance, or "
                            "tuples of (title, widget), (title, widget, icon), or "
                            "(title, widget, icon, enabled)"
                        )

                    self.content.append(text, widget, enabled=enabled, icon=icon)

        self.on_select = on_select

    @property
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?

        OptionContainer widgets cannot be disabled; this property will always return
        True; any attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    def focus(self) -> None:
        """No-op; OptionContainer cannot accept input focus."""

    @property
    def content(self) -> OptionList:
        """The tabs of content currently managed by the OptionContainer."""
        return self._content

    @property
    def current_tab(self) -> OptionItem | None:
        """The currently selected tab of content, or ``None`` if there are no tabs,
        or the OptionContainer is in a state where no tab is currently selected.

        This property can also be set with an ``int`` index, or a ``str`` label.
        """
        index = self._impl.get_current_tab_index()
        if index is None:
            return None
        return self._content[index]

    @current_tab.setter
    def current_tab(self, value: OptionItem | str | int) -> None:
        index = self._content.index(value)
        if not self._impl.is_option_enabled(index):
            raise ValueError("A disabled tab cannot be made the current tab.")

        self._impl.set_current_tab_index(index)

    @Widget.app.setter
    def app(self, app) -> None:
        # Invoke the superclass property setter
        Widget.app.fset(self, app)

        # Also assign the app to the content in the container
        for item in self._content:
            item._content.app = app

    @Widget.window.setter
    def window(self, window) -> None:
        # Invoke the superclass property setter
        Widget.window.fset(self, window)

        # Also assign the window to the content in the container
        for item in self._content:
            item._content.window = window

    @property
    def on_select(self) -> OnSelectHandler:
        """The callback to invoke when a new tab of content is selected."""
        return self._on_select

    @on_select.setter
    def on_select(self, handler: toga.widgets.optioncontainer.OnSelectHandler) -> None:
        self._on_select = wrapped_handler(self, handler)
