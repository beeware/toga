from toga_cocoa.libs import NSObject, NSTabView, NSTabViewItem, objc_method
from toga_cocoa.window import CocoaViewport

from ..libs import objc_property
from .base import Widget


class TogaTabViewDelegate(NSObject):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        # If the widget is part of a visible layout, and a resize event has
        # occurred while the tab wasn't visible, the layout of *this* tab won't
        # reflect the new availalble size. Refresh the layout.
        if self.interface.window:
            self.interface.refresh()

        # Trigger any selection handler
        if self.interface.on_select:
            index = view.indexOfTabViewItem(view.selectedTabViewItem)
            self.interface.on_select(
                self.interface, option=self.interface.content[index]
            )


class OptionContainer(Widget):
    def create(self):
        self.native = NSTabView.alloc().init()
        self.delegate = TogaTabViewDelegate.alloc().init()
        self.delegate.interface = self.interface
        self.delegate.impl = self
        self.native.delegate = self.delegate

        # Cocoa doesn't provide an explicit (public) API for tracking
        # tab enabled/disabled status; it's handled by the delegate returning
        # if a specific tab should be enabled/disabled. Keep the set set of
        # currently disabled tabs for reference purposes.
        self._disabled_tabs = set()

        # Add the layout constraints
        self.add_constraints()

    def add_content(self, index, text, widget):
        """Adds a new option to the option container.

        Args:
            index: The index in the tab list where the tab should be added.
            text (str): The text for the option container
            widget: The widget or widget tree that belongs to the text.
        """
        widget.viewport = CocoaViewport(widget.native)

        for child in widget.interface.children:
            child._impl.container = widget

        item = NSTabViewItem.alloc().init()
        item.label = text

        # Turn the autoresizing mask on the widget widget
        # into constraints. This makes the widget fill the
        # available space inside the OptionContainer.
        widget.native.translatesAutoresizingMaskIntoConstraints = True

        item.view = widget.native
        self.native.insertTabViewItem(item, atIndex=index)

    def remove_content(self, index):
        tabview = self.native.tabViewItemAtIndex(index)
        if tabview == self.native.selectedTabViewItem:
            # Don't allow removal of a selected tab
            raise self.interface.OptionException(
                "Currently selected option cannot be removed"
            )

        self.native.removeTabViewItem(tabview)

    def set_on_select(self, handler):
        pass

    def set_option_enabled(self, index, enabled):
        tabview = self.native.tabViewItemAtIndex(index)
        if enabled:
            try:
                self._disabled_tabs.remove(index)
            except KeyError:
                pass
        else:
            if tabview == self.native.selectedTabViewItem:
                # Don't allow disable a selected tab
                raise self.interface.OptionException(
                    "Currently selected option cannot be disabled"
                )

            self._disabled_tabs.add(index)
        tabview._setTabEnabled(enabled)

    def is_option_enabled(self, index):
        return index not in self._disabled_tabs

    def set_option_text(self, index, value):
        tabview = self.native.tabViewItemAtIndex(index)
        tabview.label = value

    def get_option_text(self, index):
        tabview = self.native.tabViewItemAtIndex(index)
        return tabview.label

    def get_current_tab_index(self):
        return self.native.indexOfTabViewItem(self.native.selectedTabViewItem)

    def set_current_tab_index(self, current_tab_index):
        self.native.selectTabViewItemAtIndex(current_tab_index)
