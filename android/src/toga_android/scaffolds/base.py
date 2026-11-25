from decimal import ROUND_UP

from android.view import ViewGroup
from org.beeware.android import MainActivity

from ..container import Container


class Scaffold:
    def __init__(self, interface):
        self.interface = interface
        self._title = ""
        self._navigation_bar_hidden = False
        # The activity this scaffold is displayed in; None while not attached.
        self._activity = None

        self.container = Container()
        self.container.create_container(
            MainActivity.singletonThis,
            pre_refresh=self.container_pre_refresh,
        )
        # The container is created unparented, but it can be refreshed (e.g., when
        # content is assigned) before it is attached to a window, so it needs layout
        # params of its own. These match the defaults the root content view would
        # have generated; they're converted to the parent's type on attachment.
        self.container.native_content.setLayoutParams(
            ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT,
            )
        )

    @property
    def current_container(self):
        return self.container

    def set_content(self, widget):
        self.container.set_content(widget)

    def refresh(self):
        if self.container.content:
            self.container.content.interface.refresh()

    ######################################################################
    # Title and navigation bar
    ######################################################################

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        if self._activity is not None:
            self._activity.setTitle(value)

    @property
    def navigation_bar_hidden(self):
        return self._navigation_bar_hidden

    @navigation_bar_hidden.setter
    def navigation_bar_hidden(self, hidden):
        self._navigation_bar_hidden = hidden
        if self._activity is not None:
            self.apply_navigation_bar()

    def apply_navigation_bar(self, force_hidden=False):
        # Android has a single, Activity-level ActionBar; the scaffold that is
        # currently displayed controls whether it is visible.
        actionbar = self._activity.getSupportActionBar()
        if force_hidden or self._navigation_bar_hidden:
            actionbar.hide()
        else:
            actionbar.show()

    ######################################################################
    # Attachment to a window
    ######################################################################

    def attach(self, activity, native_parent):
        self._activity = activity
        self.container.attach_container(native_parent)
        activity.setTitle(self._title)
        self.apply_navigation_bar()

    def detach(self):
        self.container.detach_container()
        self._activity = None

    ######################################################################
    # Layout
    ######################################################################

    def container_pre_refresh(self, container):
        if container.native_width and container.native_height:
            layout = self.interface.content.layout
            available_width = container.scale_out(container.native_width, ROUND_UP)
            available_height = container.scale_out(container.native_height, ROUND_UP)
            if (layout.width > available_width) or (layout.height > available_height):
                # Show the sizes in terms of CSS pixels.
                print(
                    f"Warning: Window content {(layout.width, layout.height)} "
                    f"exceeds available space {(available_width, available_height)}"
                )
