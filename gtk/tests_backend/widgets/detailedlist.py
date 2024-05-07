import asyncio
import html

from toga_gtk.libs import GLib, Gtk

from .base import SimpleProbe


class DetailedListProbe(SimpleProbe):
    native_class = Gtk.Overlay
    supports_actions = True
    supports_refresh = True

    def __init__(self, widget):
        super().__init__(widget)
        self.native_detailedlist = widget._impl.native_detailedlist
        self.native_vadj = widget._impl.native_vadj
        assert isinstance(self.native_detailedlist, Gtk.ListBox)

    @property
    def row_count(self):
        return len(self.impl.store)

    def assert_cell_content(self, row, title, subtitle, icon=None):
        row = self.impl.store[row]

        assert (
            str(row.text.get_label())
            == f"{html.escape(title)}\n<small>{html.escape(subtitle)}</small>"
        )

        if icon:
            assert row.icon.get_pixbuf() == icon._impl.native(32)
        else:
            assert row.icon is None

    @property
    def max_scroll_position(self):
        return int(self.native_vadj.get_upper() - self.native_vadj.get_page_size())

    @property
    def scroll_position(self):
        return int(self.native_vadj.get_value())

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    async def select_row(self, row, add=False):
        self.native_detailedlist.select_row(self.impl.store[row])

    def refresh_available(self):
        return self.impl.native_revealer.get_child_revealed()

    async def non_refresh_action(self):
        # Non-refresh is ... don't press the button, so it's a no op.
        pass

    async def refresh_action(self, active=True):
        if active:
            assert self.refresh_available()

            # This is a Red code/Blue code thing. We're in an async context, but the
            # method performing the click handler is non-async, and the event handler is
            # async. We lose the async context on the way, so we can't invoke the event
            # handler. To avoid this, defer the click event to the run loop, so the
            # event handler isn't inside an async context.
            def click_refresh(data):
                self.impl.native_refresh_button.clicked()

            GLib.idle_add(click_refresh, None)

            # A short pause to allow the click handler to be processed.
            await asyncio.sleep(0.1)
        else:
            assert not self.refresh_available()

    async def perform_primary_action(self, row, active=True):
        item = self.impl.store[row]
        row_height = self.native_vadj.get_upper() / len(self.impl.store)

        # item's widget stack is showing content
        assert item.stack.get_visible_child_name() == "content"
        self.impl.gesture.emit("pressed", 1, 100, row * row_height + row_height / 2)

        if active:
            await self.redraw("Action bar is visible")

            # Confirm primary action is visible, and click it.
            assert item.stack.get_visible_child_name() == "actions"
            assert self.impl.native_primary_action_button.get_visible()
            self.impl.native_primary_action_button.clicked()

            await self.redraw("Primary action button clicked")
        else:
            # Visibility of the action bar is dependent on the state
            # of the other action.
            if self.widget.on_secondary_action._raw is not None:
                # Actions are visible, but the primary button isn't.
                assert item.stack.get_visible_child_name() == "actions"
                assert not self.impl.native_primary_action_button.get_visible()
                await self.redraw(
                    "Action bar is visible, but primary action isn't available"
                )

                # Select the previous row to hide the action bar.
                await self.select_row(row - 1)

            # Item's content stack has been fully restored
            await self.redraw("Action bar is not visible")

        # Item's content stack has been fully restored
        assert item.stack.get_visible_child_name() == "content"

    async def perform_secondary_action(self, row, active=True):
        item = self.impl.store[row]
        row_height = self.native_vadj.get_upper() / len(self.impl.store)

        # item's widget stack is showing content
        assert item.stack.get_visible_child_name() == "content"

        # Right click on the row
        self.impl.gesture.emit("pressed", 1, 100, row * row_height + row_height / 2)

        if active:
            await self.redraw("Action bar is visible")

            # Confirm Secondary action is visible, and click it.
            assert item.stack.get_visible_child_name() == "actions"
            assert self.impl.native_secondary_action_button.get_visible()
            self.impl.native_secondary_action_button.clicked()

            await self.redraw("Secondary action button clicked")
        else:
            # Visibility of the action bar is dependent on the state
            # of the other action.
            if self.widget.on_primary_action._raw is not None:
                # Actions are visible, but the secondary button isn't.
                assert item.stack.get_visible_child_name() == "actions"
                assert not self.impl.native_secondary_action_button.get_visible()
                await self.redraw(
                    "Action bar is visible, but secondary action isn't available"
                )

                # Select the previous row to hide the action bar.
                await self.select_row(row - 1)

            # Item's content stack has been fully restored
            await self.redraw("Action bar is not visible")

        # Item's content stack has been fully restored
        assert item.stack.get_visible_child_name() == "content"
