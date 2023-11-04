import asyncio
import platform

from rubicon.objc.api import Block

from toga_iOS.libs import (
    NSIndexPath,
    NSPoint,
    UIContextualActionStyle,
    UITableView,
    UITableViewController,
)

from .base import SimpleProbe, UIControlEventValueChanged


class DetailedListProbe(SimpleProbe):
    native_class = UITableView
    supports_actions = True
    supports_refresh = True

    def __init__(self, widget):
        super().__init__(widget)
        self.native_controller = widget._impl.native_controller
        assert isinstance(self.native_controller, UITableViewController)

    @property
    def row_count(self):
        # Need to use the long form of this method because the first argument when used
        # as a selector is ambiguous with a property of the same name on the object.
        return int(
            self.native.delegate.tableView_numberOfRowsInSection_(self.native, 0)
        )

    def assert_cell_content(self, row, title, subtitle, icon=None):
        # Need to use the long form of this method because the first argument when used
        # as a selector is ambiguous with a property of the same name on the object.
        cell = self.native.delegate.tableView_cellForRowAtIndexPath_(
            self.native,
            NSIndexPath.indexPathForRow(row, inSection=0),
        )
        assert str(cell.textLabel.text) == title
        assert str(cell.detailTextLabel.text) == subtitle

        if icon:
            assert cell.imageView.image == icon._impl.native
        else:
            assert cell.imageView.image is None

    @property
    def max_scroll_position(self):
        max_value = int(self.native.contentSize.height - self.native.frame.size.height)
        # The max value is a little higher on iOS 17.
        # Not sure where the 34 extra pixels are coming from. It appears to be
        # a constant, independent of the number of rows of data.
        if int(platform.release().split(".")[0]) >= 17:
            max_value += 34
        return max(0, max_value)

    @property
    def scroll_position(self):
        return int(self.native.contentOffset.y)

    async def wait_for_scroll_completion(self):
        position = self.scroll_position
        current = None
        # Iterate until 2 successive reads of the scroll position,
        # 0.05s apart, return the same value
        while position != current:
            position = current
            await asyncio.sleep(0.05)
            current = self.scroll_position

    async def select_row(self, row, add=False):
        path = NSIndexPath.indexPathForRow(row, inSection=0)
        self.native.selectRowAtIndexPath(path, animated=False, scrollPosition=0)
        # Need to use the long form of this method because the first argument when used
        # as a selector is ambiguous with a property of the same name on the object.
        self.native.delegate.tableView_didSelectRowAtIndexPath_(self.native, path)

    def refresh_available(self):
        return self.scroll_position <= 0

    async def non_refresh_action(self):
        # iOS completely handles refresh actions, so there's no testing path
        pass

    async def refresh_action(self, active=True):
        if active:
            assert self.native_controller.refreshControl is not None
            self.native_controller.refreshControl.beginRefreshing()
            self.native_controller.refreshControl.sendActionsForControlEvents(
                UIControlEventValueChanged
            )
            self.native.setContentOffset(
                NSPoint(0, -self.native_controller.refreshControl.frame.size.height)
            )

            # Wait for the scroll to relax after reload completion
            while self.scroll_position < 0:
                await asyncio.sleep(0.01)
        else:
            assert self.native_controller.refreshControl is None

    def _perform_action(self, action, row, label, handler_factory):
        # This is a little convoluted, and not an ideal test, but :shrug:. The
        # Primary/Secondary actions are swipe actions with confirmation buttons, but iOS
        # doesn't expose any way to programmatically generate a swipe, or to
        # programmatically reveal and press the confirmation button. However, we *can*
        # generate the action object that a swipe would create, and invoke the handler
        # associated with that action.
        assert str(action.title) == label
        assert action.style == UIContextualActionStyle.Normal.value

        action_done = False

        @Block
        def on_action_performed(done: bool) -> None:
            nonlocal action_done
            action_done = True

        # Ideally, we'd use `action.handler` to get the handler associated with the
        # action, but https://github.com/beeware/rubicon-objc/issues/225 prevents the
        # retrieval of blocks by property on ARM64 hardware. So - we use the same
        # factory method to generate a fresh copy of the handler, and invoke the copy.
        handler_factory(row)(action, self.native, on_action_performed)

        # Confirm the completion handler was invoked.
        assert action_done

    async def perform_primary_action(self, row, active=True):
        path = NSIndexPath.indexPathForRow(row, inSection=0)
        # Need to use the long form of this method because the first argument when used
        # as a selector is ambiguous with a property of the same name on the object.
        config = self.native.delegate.tableView_trailingSwipeActionsConfigurationForRowAtIndexPath_(
            self.native, path
        )

        if active:
            assert len(config.actions) == 1
            self._perform_action(
                config.actions[0],
                row=row,
                label=self.widget._primary_action,
                handler_factory=self.impl.primary_action_handler,
            )
        else:
            assert len(config.actions) == 0

    async def perform_secondary_action(self, row, active=True):
        path = NSIndexPath.indexPathForRow(row, inSection=0)
        # Need to use the long form of this method because the first argument when used
        # as a selector is ambiguous with a property of the same name on the object.
        config = self.native.delegate.tableView_leadingSwipeActionsConfigurationForRowAtIndexPath_(
            self.native, path
        )

        if active:
            assert len(config.actions) == 1
            self._perform_action(
                config.actions[0],
                row=row,
                label=self.widget._secondary_action,
                handler_factory=self.impl.secondary_action_handler,
            )
        else:
            assert len(config.actions) == 0
