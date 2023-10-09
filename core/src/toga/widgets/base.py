from __future__ import annotations

from builtins import id as identifier
from typing import TYPE_CHECKING, Iterator, NoReturn
from weakref import WeakValueDictionary

from travertino.node import Node

from toga.platform import get_platform_factory
from toga.style import Pack, TogaApplicator

if TYPE_CHECKING:
    from toga.app import App
    from toga.window import Window


class WidgetRegistry(WeakValueDictionary):
    # WidgetRegistry is implemented as a subclass of WeakValueDictionary, because it
    # provides a mapping from ID to widget. However, it exposes a set-like API; add()
    # and update() take instances to be added, and iteration is over values. The
    # mapping is weak so the registry doesn't retain a strong reference to the widget,
    # preventing memory cleanup.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: str, value: Widget) -> NoReturn:
        # We do not want to allow setting items directly but to use the "add"
        # method instead.
        raise RuntimeError("Widgets cannot be directly added to a registry")

    def update(self, widgets: list[Widget]) -> None:
        for widget in widgets:
            self.add(widget)

    def add(self, widget: Widget) -> None:
        if widget.id in self:
            # Prevent from adding the same widget twice
            # or adding 2 widgets with the same id
            raise KeyError(f"There is already a widget with the id {widget.id!r}")
        super().__setitem__(widget.id, widget)

    def remove(self, id: str) -> None:
        del self[id]

    def __iter__(self) -> Iterator[Widget]:
        return iter(self.values())

    def __repr__(self) -> str:
        return "{" + ", ".join(f"{k!r}: {v!r}" for k, v in self.items()) + "}"


class Widget(Node):
    _MIN_WIDTH = 100
    _MIN_HEIGHT = 100

    def __init__(
        self,
        id: str | None = None,
        style=None,
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
        self._window = None
        self._app = None
        self._impl = None

        self.factory = get_platform_factory()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:0x{identifier(self):x}>"

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

            This is a beta feature. The ``tab_index`` API may change in
            future.
        """
        return self._impl.get_tab_index()

    @tab_index.setter
    def tab_index(self, tab_index: int) -> None:
        self._impl.set_tab_index(tab_index)

    def _assert_can_have_children(self):
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

                # add to new parent
                super().add(child)

                # set app and window
                child.app = self.app
                child.window = self.window

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

            # add to new parent
            super().insert(index, child)

            # set app and window
            child.app = self.app
            child.window = self.window

            self._impl.insert_child(index, child._impl)

        # Whatever layout we're a part of needs to be refreshed
        self.refresh()

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

                child.app = None
                child.window = None

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

            # Deregister the widget from the old app
            self._app.widgets.remove(self.id)

        self._app = app
        self._impl.set_app(app)
        for child in self.children:
            child.app = app

        if app is not None:
            # Add this widget to the application widget registry
            app.widgets.add(self)

    @property
    def window(self) -> Window | None:
        """The window to which this widget belongs.

        When setting the window for a widget, all children of this widget will be
        recursively assigned to the same window.
        """
        return self._window

    @window.setter
    def window(self, window: Window | None) -> None:
        # Remove the widget from the widget registry it is currently a part of
        if self.window is not None:
            self.window.widgets.remove(self.id)

        self._window = window
        self._impl.set_window(window)

        for child in self.children:
            child.window = window

        if window is not None:
            # Add this widget to the window's widget registry
            window.widgets.add(self)

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
