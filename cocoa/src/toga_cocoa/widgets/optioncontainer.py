import asyncio
import warnings

from rubicon.objc import objc_method
from travertino.size import at_least

from toga_cocoa.container import Container
from toga_cocoa.libs import NSTabView, NSTabViewItem

from ..libs import objc_property
from .base import Widget


class TogaTabView(NSTabView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def tabView_shouldSelectTabViewItem_(self, view, item) -> bool:
        return view.indexOfTabViewItem(item) not in self.impl._disabled_tabs

    @objc_method
    def tabView_didSelectTabViewItem_(self, view, item) -> None:
        # Refresh the layout of the newly selected tab.
        index = view.indexOfTabViewItem(view.selectedTabViewItem)
        container = self.impl.sub_containers[index]
        container.content.interface.refresh()

        # Notify of the change in selection.
        self.interface.on_select()

    @objc_method
    def refreshContent(self) -> None:
        # Refresh all the subcontainer layouts
        for container in self.impl.sub_containers:
            container.content.interface.refresh()


class OptionContainer(Widget):
    uses_icons = False

    def create(self):
        self.native = TogaTabView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native

        # Cocoa doesn't provide an explicit (public) API for tracking
        # tab enabled/disabled status; it's handled by the delegate returning
        # if a specific tab should be enabled/disabled. Keep the set of
        # currently disabled tabs for reference purposes.
        self._disabled_tabs = set()
        self.sub_containers = []

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        # Setting the bounds changes the constraints, but that doesn't mean
        # the constraints have been fully applied. Force realization of the
        # new layout, and then refresh the content.
        self.native.layoutSubtreeIfNeeded()
        self.native.refreshContent()

    def content_refreshed(self, container):
        container.min_width = container.content.interface.layout.min_width
        container.min_height = container.content.interface.layout.min_height

        # Re-layout and schedule a second refresh if intrinsic size has changed,
        # since if the subcontainers' minimum size changes, the widget itself's
        # minimum size may change as well.
        prev_intrinsic_size = (
            self.interface.intrinsic.width,
            self.interface.intrinsic.height,
        )
        self.rehint()
        intrinsic_size = (
            self.interface.intrinsic.width,
            self.interface.intrinsic.height,
        )
        if prev_intrinsic_size != intrinsic_size:
            asyncio.get_running_loop().call_soon_threadsafe(self.interface.refresh)

    def add_option(self, index, text, widget, icon):
        # Create the container for the widget
        container = Container(on_refresh=self.content_refreshed)
        container.content = widget
        self.sub_containers.insert(index, container)

        # Create a NSTabViewItem for the content
        item = NSTabViewItem.alloc().init()
        item.label = text

        item.view = container.native
        self.native.insertTabViewItem(item, atIndex=index)

    def remove_option(self, index):
        tabview = self.native.tabViewItemAtIndex(index)
        self.native.removeTabViewItem(tabview)

        sub_container = self.sub_containers[index]
        sub_container.content = None
        del self.sub_containers[index]

    def set_option_enabled(self, index, enabled):
        tabview = self.native.tabViewItemAtIndex(index)
        if enabled:
            try:
                self._disabled_tabs.remove(index)
            except KeyError:
                # Enabling a tab that wasn't previously disabled
                pass
        else:
            self._disabled_tabs.add(index)

        # This is an undocumented method, but it disables the button for the item. As an
        # extra safety mechanism, the delegate will prevent the item from being selected
        # by returning False for tabView:shouldSelectTabViewItem: if the item is in the
        # disabled tab set. We catch the AttributeError and raise a warning in case the
        # private method is ever fully deprecated; if this happens, the tab still won't
        # be selectable (because of the delegate), but it won't be *visually* disabled,
        # the code won't crash.
        try:
            tabview._setTabEnabled(enabled)
        except AttributeError:  # pragma: no cover
            warnings.warn(
                "Private Cocoa method _setTabEnabled: has been removed!",
                stacklevel=2,
            )

    def is_option_enabled(self, index):
        return index not in self._disabled_tabs

    def set_option_text(self, index, value):
        tabview = self.native.tabViewItemAtIndex(index)
        tabview.label = value

    def set_option_icon(self, index, value):  # pragma: nocover
        # This shouldn't ever be invoked, but it's included for completeness.
        pass

    def get_option_icon(self, index):
        # Icons aren't supported
        return None

    def get_option_text(self, index):
        tabview = self.native.tabViewItemAtIndex(index)
        return str(tabview.label)

    def get_current_tab_index(self):
        return self.native.indexOfTabViewItem(self.native.selectedTabViewItem)

    def set_current_tab_index(self, current_tab_index):
        self.native.selectTabViewItemAtIndex(current_tab_index)

    def rehint(self):
        # The optionContainer must be at least the size of it's largest content
        # plus the decors around the OptionContainer.
        min_width = 0
        min_height = 0
        for sub_container in self.sub_containers:
            min_width = max(min_width, sub_container.min_width)
            min_height = max(min_height, sub_container.min_height)

        # The below logic to get the width and height of the tab bar and decorations
        # uses the sizes of the widget itself, which might seem conunterintuitive as
        # rehinting is done before the widget is laid out.  However, the calculations
        # here will not change regardless of layout if the widget has a non-zero
        # frame, and rehint is always called at a certain point when the widget has
        # a non-zero frame in Toga's sequence.
        self.native.layoutSubtreeIfNeeded()
        decor_width = (
            self.native.alignmentRectForFrame(self.native.frame).size.width
            - self.native.contentRect.size.width
        )
        decor_height = (
            self.native.alignmentRectForFrame(self.native.frame).size.height
            - self.native.contentRect.size.height
        )

        # Be on the defensive side and prevent absurdly small OptionContainers by maxing
        # in an artificially imposed minimum size.
        self.interface.intrinsic.width = at_least(
            max(min_width + decor_width, self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            max(min_height + decor_height, self.interface._MIN_HEIGHT)
        )
