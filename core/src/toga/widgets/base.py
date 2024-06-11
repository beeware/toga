from __future__ import annotations

from builtins import id as identifier
from typing import TYPE_CHECKING, Any, TypeVar

from travertino.declaration import BaseStyle
from travertino.node import Node

from toga.platform import get_platform_factory
from toga.style import Pack, TogaApplicator

if TYPE_CHECKING:
    from toga.app import App
    from toga.window import Window

StyleT = TypeVar("StyleT", bound=BaseStyle)


class Widget(Node):
    _MIN_WIDTH = 100
    _MIN_HEIGHT = 100

    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
    ):
        """Create a base Toga widget.

        This is an abstract base class; it cannot be instantiated.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        """
        super().__init__(
            style=style if style else Pack(),
            applicator=TogaApplicator(self),
        )

        self._id = str(id if id else identifier(self))
        self._window: Window | None = None
        self._app: App | None = None
        self._impl: Any = None

        self.factory = get_platform_factory()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:0x{identifier(self):x}>"

    def __lt__(self, other: Widget) -> bool:
        return self.id < other.id

    @property
    def id(self) -> str:
        """The DOM identifier for the widget.

        This id can be used to target CSS directives.
        """
        return self._id

    @property
    def tab_index(self) -> int | None:
        """The position of the widget in the focus chain for the window.

        .. note::

            This is a beta feature. The ``tab_index`` API may change in the future.
        """
        return self._impl.get_tab_index()

    @tab_index.setter
    def tab_index(self, tab_index: int) -> None:
        self._impl.set_tab_index(tab_index)

    def _assert_can_have_children(self) -> None:
        if not self.can_have_children:
            raise ValueError(f"{type(self).__name__} cannot have children")

    def add(self, *children: Widget) -> None:
        """Add the provided widgets as children of this widget.

        If a child widget already has a parent, it will be re-parented as a
        child of this widget. If the child widget is already a child of this
        widget, there is no change.

        :param children: The widgets to add as children of this widget.
        :raises ValueError: If this widget cannot have children.
        """
        self._assert_can_have_children()
        for child in children:
            if child.parent is not self:
                # remove from old parent
                if child.parent:
                    child.parent.remove(child)

                # Set app and window. This is done *before* changing any parenting
                # relationships, so that the widget registry can verify the widget ID is
                # unique. App must be set before window to ensure the widget registry
                # can be found.
                child.app = self.app
                child.window = self.window

                # add to new parent
                super().add(child)

                self._impl.add_child(child._impl)

        # Whatever layout we're a part of needs to be refreshed
        self.refresh()

    def insert(self, index: int, child: Widget) -> None:
        """Insert a widget as a child of this widget.

        If a child widget already has a parent, it will be re-parented as a
        child of this widget. If the child widget is already a child of this
        widget, there is no change.

        :param index: The position in the list of children where the new widget
            should be added.
        :param child: The child to insert as a child of this node.
        :raises ValueError: If this widget cannot have children.
        """
        self._assert_can_have_children()
        if child.parent is not self:
            # remove from old parent
            if child.parent:
                child.parent.remove(child)

            # Set app and window. This is done *before* changing any parenting
            # relationships, so that the widget registry can verify the widget ID is
            # unique. App must be set before window to ensure the widget registry
            # can be found.
            child.app = self.app
            child.window = self.window

            # add to new parent
            super().insert(index, child)

            self._impl.insert_child(index, child._impl)

        # Whatever layout we're a part of needs to be refreshed
        self.refresh()

    def index(self, child: Widget) -> int:
        """Get the index of a widget in the list of children of this widget.

        :param child: The child widget of interest.
        :raises ValueError: If the specified child widget is not found in the
            list of children.

        :returns: Index of specified child widget in children list.
        """
        for _ind, _child in enumerate(self._children):
            if child == _child:
                return _ind
        raise ValueError(f"{type(child).__name__} not found")

    def replace(self, old_child: Widget, new_child: Widget) -> None:
        """Replace an existing child widget with a new child widget.

        :param old_child: The existing child widget to be replaced.
        :param new_child: The new child widget to be included.
        """
        old_child_index = self.index(old_child)
        self.remove(old_child)
        self.insert(old_child_index, new_child)

    def remove(self, *children: Widget) -> None:
        """Remove the provided widgets as children of this node.

        Any nominated child widget that is not a child of this widget will
        not have any change in parentage.

        Refreshes the widget after removal if any children were removed.

        :param children: The child nodes to remove.
        :raises ValueError: If this widget cannot have children.
        """
        self._assert_can_have_children()

        removed = False
        for child in children:
            if child.parent is self:
                removed = True
                super().remove(child)

                # Remove from the window before removing from the app
                # so that the widget can be removed from the app-level registry.
                child.window = None
                child.app = None

                self._impl.remove_child(child._impl)

        # If we removed something, whatever layout we're a part of needs to be refreshed
        if removed:
            self.refresh()

    def clear(self) -> None:
        """Remove all child widgets of this node.

        Refreshes the widget after removal if any children were removed.

        :raises ValueError: If this widget cannot have children.
        """
        self._assert_can_have_children()
        self.remove(*self.children)

    @property
    def app(self) -> App | None:
        """The App to which this widget belongs.

        When setting the app for a widget, all children of this widget will be
        recursively assigned to the same app.

        :raises ValueError: If this widget is already associated with another app.
        """
        return self._app

    @app.setter
    def app(self, app: App | None) -> None:
        # If the widget is already assigned to an app
        if self._app:
            if self._app == app:
                # If app is the same as the previous app, return
                return

        self._app = app
        self._impl.set_app(app)
        for child in self.children:
            child.app = app

    @property
    def window(self) -> Window | None:
        """The window to which this widget belongs.

        When setting the window for a widget, all children of this widget will be
        recursively assigned to the same window.

        If the widget has a value for :any:`window`, it *must* also have a value for
        :any:`app`.
        """
        return self._window

    @window.setter
    def window(self, window: Window | None) -> None:
        if self.window is not None and window is None:
            # If the widget is currently in the registry, but is being removed from a
            # window, remove the widget from the widget registry
            self.window.app.widgets._remove(self.id)
        elif self.window is None and window is not None:
            # If the widget is being assigned to a window for the first time, add it to the widget registry
            window.app.widgets._add(self)

        self._window = window
        self._impl.set_window(window)

        for child in self.children:
            child.window = window

    @property
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?"""
        return self._impl.get_enabled()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._impl.set_enabled(bool(value))

    def refresh(self) -> None:
        self._impl.refresh()

        # Refresh the layout
        if self._root:
            # We're not the root of the node hierarchy;
            # defer the refresh call to the root node.
            self._root.refresh()
        else:
            # We can't compute a layout until we have a container
            if self._impl.container:
                super().refresh(self._impl.container)
                self._impl.container.refreshed()

    def focus(self) -> None:
        """Give this widget the input focus.

        This method is a no-op if the widget can't accept focus. The ability of a widget
        to accept focus is platform-dependent. In general, on desktop platforms you can
        focus any widget that can accept user input, while on mobile platforms focus is
        limited to widgets that accept text input (i.e., widgets that cause the virtual
        keyboard to appear).
        """
        self._impl.focus()
