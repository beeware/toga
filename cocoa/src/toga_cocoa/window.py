from rubicon.objc import (
    SEL,
    CGSize,
    NSMakeRect,
    NSPoint,
    NSSize,
    objc_method,
    objc_property,
)

from toga.command import Command, Separator
from toga.constants import WindowState
from toga.types import Position, Size
from toga.window import _initial_position
from toga_cocoa.container import Container
from toga_cocoa.libs import (
    NSBackingStoreBuffered,
    NSImage,
    NSMutableArray,
    NSMutableDictionary,
    NSNumber,
    NSScreen,
    NSToolbar,
    NSToolbarItem,
    NSWindow,
    NSWindowStyleMask,
    core_graphics,
)

from .screens import Screen as ScreenImpl


def toolbar_identifier(cmd):
    return f"Toolbar-{type(cmd).__name__}-{id(cmd)}"


class TogaWindow(NSWindow):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def windowShouldClose_(self, notification) -> bool:
        # The on_close handler has a cleanup method that will enforce
        # the close if the on_close handler requests it; this initial
        # "should close" request always returns False.
        self.interface.on_close()
        return False

    @objc_method
    def windowWillClose_(self, notification) -> None:
        # Setting the toolbar delegate to None doesn't disconnect
        # the delegate and still triggers the delegate events.
        # Hence, simply remove the toolbar instead.
        if self.toolbar:
            self.toolbar = None
        # Disconnect the window delegate.
        self.delegate = None

        # Disconnecting the window delegate doesn't prevent custom methods
        # which are performed with a delay (i.e., having a delay != 0),
        # from being triggered when `impl` & `interface` attributes are empty.
        # Hence, check guards for empty `impl` and `interface` attributes need
        # to be used in such custom methods.

    @objc_method
    def windowDidResize_(self, notification) -> None:
        if self.interface.content:
            # Set the window to the new size
            self.interface.content.refresh()

    @objc_method
    def windowDidBecomeMain_(self, notification):
        self.interface.on_gain_focus()

    @objc_method
    def windowDidResignMain_(self, notification):
        self.interface.on_lose_focus()

    @objc_method
    def windowDidMiniaturize_(self, notification) -> None:
        self.interface.on_hide()
        if (
            self.impl._pending_state_transition
            and self.impl._pending_state_transition != WindowState.MINIMIZED
        ):
            self.impl._apply_state(WindowState.NORMAL)
        else:
            self.impl._pending_state_transition = None

    @objc_method
    def windowDidDeminiaturize_(self, notification) -> None:
        self.interface.on_show()
        self.impl._apply_state(self.impl._pending_state_transition)

    @objc_method
    def windowDidEnterFullScreen_(self, notification) -> None:
        if (
            self.impl._pending_state_transition
            and self.impl._pending_state_transition != WindowState.FULLSCREEN
        ):
            # Directly exiting fullscreen without a delay will result in error:
            # ````2024-08-09 15:46:39.050 python[2646:37395] not in fullscreen state````
            # and any subsequent window state calls to the OS will not work or will be
            # glitchy.
            self.performSelector(
                SEL("delayedFullScreenExit:"), withObject=None, afterDelay=0
            )
        else:
            self.impl._pending_state_transition = None

    @objc_method
    def delayedFullScreenExit_(self, sender) -> None:
        self.impl._apply_state(WindowState.NORMAL)

    @objc_method
    def windowDidExitFullScreen_(self, notification) -> None:
        self.impl._apply_state(self.impl._pending_state_transition)

    ######################################################################
    # Toolbar delegate methods
    ######################################################################

    @objc_method
    def toolbarAllowedItemIdentifiers_(self, toolbar):  # pragma: no cover
        """Determine the list of available toolbar items."""
        # This method is required by the Cocoa API, but it's only ever called if the
        # toolbar allows user customization. We don't turn that option on so this method
        # can't ever be invoked - but we need to provide an implementation.
        allowed = NSMutableArray.alloc().init()
        for item in self.interface.toolbar:
            allowed.addObject_(toolbar_identifier(item))
        return allowed

    @objc_method
    def toolbarDefaultItemIdentifiers_(self, toolbar):
        """Determine the list of toolbar items that will display by default."""
        default = NSMutableArray.alloc().init()
        prev_group = None
        for item in self.interface.toolbar:
            # If there's been a group change, and this item isn't a separator,
            # add a separator between groups.
            if prev_group is not None:
                if item.group != prev_group and not isinstance(item, Separator):
                    default.addObject_(toolbar_identifier(prev_group))
            default.addObject_(toolbar_identifier(item))
            prev_group = item.group

        return default

    @objc_method
    def toolbar_itemForItemIdentifier_willBeInsertedIntoToolbar_(
        self,
        toolbar,
        identifier,
        insert: bool,
    ):
        """Create the requested toolbar button."""
        native = NSToolbarItem.alloc().initWithItemIdentifier_(identifier)
        try:
            item = self.impl._toolbar_items[str(identifier)]
            native.setLabel(item.text)
            native.setPaletteLabel(item.text)
            if item.tooltip:
                native.setToolTip(item.tooltip)
            if item.icon:
                native.setImage(item.icon._impl.native)

            item._impl.native.add(native)

            native.setTarget_(self)
            native.setAction_(SEL("onToolbarButtonPress:"))
        except KeyError:  # Separator items
            pass

        return native

    @objc_method
    def validateToolbarItem_(self, item) -> bool:
        """Confirm if the toolbar item should be enabled."""
        try:
            return self.impl._toolbar_items[str(item.itemIdentifier)].enabled
        except KeyError:  # pragma: nocover
            # This branch *shouldn't* ever happen; but there's an edge
            # case where a toolbar redraw happens in the middle of deleting
            # a toolbar item that can't be reliably reproduced, so it sometimes
            # happens in testing.
            return False

    ######################################################################
    # Toolbar button press delegate methods
    ######################################################################

    @objc_method
    def onToolbarButtonPress_(self, obj) -> None:
        """Invoke the action tied to the toolbar button."""
        item = self.impl._toolbar_items[str(obj.itemIdentifier)]
        item.action()


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        mask = NSWindowStyleMask.Titled
        if self.interface.closable:
            mask |= NSWindowStyleMask.Closable

        if self.interface.resizable:
            mask |= NSWindowStyleMask.Resizable

        if self.interface.minimizable:
            mask |= NSWindowStyleMask.Miniaturizable

        # Create the window with a default frame;
        # we'll update size and position later.
        self.native = TogaWindow.alloc().initWithContentRect(
            NSMakeRect(0, 0, 0, 0),
            styleMask=mask,
            backing=NSBackingStoreBuffered,
            defer=False,
        )
        self.native.interface = self.interface
        self.native.impl = self

        # Cocoa releases windows when they are closed; this causes havoc with
        # Toga's widget cleanup because the ObjC runtime thinks there's no
        # references to the object left. Explicitly prevent this and let Rubicon
        # manage the release when no Python references are left.
        self.native.releasedWhenClosed = False

        # Pending Window state transition variable:
        self._pending_state_transition = None

        self.set_title(title)
        self.set_size(size)
        self.set_position(position if position is not None else _initial_position())

        self.native.delegate = self.native

        self.container = Container(on_refresh=self.content_refreshed)
        self.native.contentView = self.container.native

        # Ensure that the container renders it's background in the same color as the
        # window.
        self.native.wantsLayer = True
        self.container.native.backgroundColor = self.native.backgroundColor

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return str(self.native.title)

    def set_title(self, title):
        self.native.title = title

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):
        self.native.close()

    def set_app(self, app):
        pass

    def show(self):
        self.native.makeKeyAndOrderFront(None)
        # Cocoa doesn't provide a native window delegate notification that would
        # be triggered when makeKeyAndOrderFront_ is called. So, trigger the event
        # here instead.
        self.interface.on_show()

    ######################################################################
    # Window content and resources
    ######################################################################

    def content_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height

        # If the minimum layout is bigger than the current window,
        # increase the size of the window.
        frame = self.native.frame
        if frame.size.width < min_width and frame.size.height < min_height:
            self.set_size((min_width, min_height))
        elif frame.size.width < min_width:
            self.set_size((min_width, frame.size.height))
        elif frame.size.height < min_height:
            self.set_size((frame.size.width, min_height))

        self.container.min_width = min_width
        self.container.min_height = min_height

    def set_content(self, widget):
        # Set the content of the window's container
        self.container.content = widget

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        frame = self.native.frame
        return Size(frame.size.width, frame.size.height)

    def set_size(self, size):
        frame = self.native.frame
        frame.size = NSSize(size[0], size[1])
        self.native.setFrame(frame, display=True, animate=True)

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        return ScreenImpl(self.native.screen)

    def get_position(self) -> Position:
        # The "primary" screen has index 0 and origin (0, 0).
        primary_screen = NSScreen.screens[0].frame
        window_frame = self.native.frame

        # macOS origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        return Position(
            window_frame.origin.x,
            primary_screen.size.height
            - (window_frame.origin.y + window_frame.size.height),
        )

    def set_position(self, position):
        # The "primary" screen has index 0 and origin (0, 0).
        primary_screen = NSScreen.screens[0].frame

        # macOS origin is bottom left of screen, and the screen might be
        # offset relative to other screens. Adjust for this.
        x = position[0]
        y = primary_screen.size.height - position[1]

        self.native.setFrameTopLeftPoint(NSPoint(x, y))

    ######################################################################
    # Window visibility
    ######################################################################

    def hide(self):
        self.native.orderOut(self.native)
        # Cocoa doesn't provide a native window delegate notification that would
        # be triggered when orderOut_ is called. So, trigger the event here instead.
        self.interface.on_hide()

    def get_visible(self):
        # macOS reports minimized windows as non-visible, but Toga considers minimized
        # windows to be visible, so we need to override in that case. However,
        # minimization state is retained when the app as a whole is hidden; so we also
        # need to check for app-level hiding when overriding.
        return bool(self.native.isVisible) or (
            self.get_window_state(in_progress_state=True) == WindowState.MINIMIZED
            and not bool(self.interface.app._impl.native.isHidden())
        )

    ######################################################################
    # Window state
    ######################################################################

    def get_window_state(self, in_progress_state=False):
        if in_progress_state and self._pending_state_transition:
            return self._pending_state_transition
        if bool(self.container.native.isInFullScreenMode()):
            return WindowState.PRESENTATION
        elif bool(self.native.styleMask & NSWindowStyleMask.FullScreen):
            return WindowState.FULLSCREEN
        elif bool(self.native.isZoomed):
            return WindowState.MAXIMIZED
        elif bool(self.native.isMiniaturized):
            return WindowState.MINIMIZED
        else:
            return WindowState.NORMAL

    def set_window_state(self, state):
        # Since the requests to the OS for changing window states are non-blocking,
        # if we are in the middle of processing a state, we need to store the
        # user-requested state and apply the state when we have completed processing
        # a transition. There are 2 types of callbacks:
        # * EnteredState:
        #   Here, we need to check if the current state is the same as the pending
        #   state.
        #   -- If yes: Clear the pending state variable and return.
        #   -- If no: Apply NORMAL state, which will later apply the pending state
        #             when the state is NORMAL.
        # * ExitedState:
        #   Here, since we are in NORMAL state, we just apply the pending state.
        #   When we enter the user-requested pending state, then clear the pending
        #   state variable and return.

        if self._pending_state_transition:
            self._pending_state_transition = state
        else:
            # If the app is in presentation mode, but this window isn't, then
            # exit app presentation mode before setting the requested state.
            if any(
                window.state == WindowState.PRESENTATION and window != self.interface
                for window in self.interface.app.windows
            ):
                self.interface.app.exit_presentation_mode()

            self._pending_state_transition = state
            if self.get_window_state() != WindowState.NORMAL:
                self._apply_state(WindowState.NORMAL)
            else:
                self._apply_state(state)

    def _apply_state(self, target_state):
        if target_state is None:
            return

        current_state = self.get_window_state()
        # Although same state check is done at the core, yet this is required
        # Since, _apply_state() is called internally on the implementation
        # side, after the completion of non-blocking APIs(setIsMiniaturized,
        # toggleFullScreen), by the delegate. Then this same state check is
        # used to terminate further processing.
        if target_state == current_state:
            self._pending_state_transition = None
            return

        elif target_state == WindowState.MAXIMIZED:
            self.native.setIsZoomed(True)
            # No need to check for other pending states,
            # since this is fully applied at this point.
            self._pending_state_transition = None

        elif target_state == WindowState.MINIMIZED:
            self.native.setIsMiniaturized(True)

        elif target_state == WindowState.FULLSCREEN:
            self.native.toggleFullScreen(self.native)

        elif target_state == WindowState.PRESENTATION:
            self._before_presentation_mode_screen = self.interface.screen
            opts = NSMutableDictionary.alloc().init()
            opts.setObject(
                NSNumber.numberWithBool(True),
                forKey="NSFullScreenModeAllScreens",
            )
            # The widgets are actually added to
            # window._impl.container.native, instead of
            # window.content._impl.native. And
            # window._impl.native.contentView is
            # window._impl.container.native. Hence,
            # we need to go fullscreen on
            # window._impl.container.native instead.
            self.container.native.enterFullScreenMode(
                self.interface.screen._impl.native, withOptions=opts
            )

            # Going presentation mode causes the window content
            # to be re-homed in a NSFullScreenWindow; teach the
            # new parent window about its Toga representations.
            self.container.native.window._impl = self
            self.container.native.window.interface = self.interface
            self.interface.content.refresh()

            # No need to check for other pending states,
            # since this is fully applied at this point.
            self._pending_state_transition = None

        else:  # target_state == WindowState.NORMAL:
            if current_state == WindowState.MAXIMIZED:
                self.native.setIsZoomed(False)
                self._apply_state(self._pending_state_transition)

            elif current_state == WindowState.MINIMIZED:
                self.native.setIsMiniaturized(False)

            elif current_state == WindowState.FULLSCREEN:
                self.native.toggleFullScreen(self.native)

            else:  # current_state == WindowState.PRESENTATION:
                opts = NSMutableDictionary.alloc().init()
                opts.setObject(
                    NSNumber.numberWithBool(True), forKey="NSFullScreenModeAllScreens"
                )
                self.container.native.exitFullScreenModeWithOptions(opts)
                self.interface.content.refresh()

                self.interface.screen = self._before_presentation_mode_screen
                del self._before_presentation_mode_screen

                self._apply_state(self._pending_state_transition)

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        bitmap = self.container.native.bitmapImageRepForCachingDisplayInRect(
            self.container.native.bounds
        )
        self.container.native.cacheDisplayInRect(
            self.container.native.bounds, toBitmapImageRep=bitmap
        )

        # Get a reference to the CGImage from the bitmap
        cg_image = bitmap.CGImage

        target_size = CGSize(
            core_graphics.CGImageGetWidth(cg_image),
            core_graphics.CGImageGetHeight(cg_image),
        )
        ns_image = NSImage.alloc().initWithCGImage(cg_image, size=target_size)
        return ns_image


class MainWindow(Window):
    def __init__(self, interface, title, position, size):
        super().__init__(interface, title, position, size)

        # By default, no toolbar
        self._toolbar_items = {}
        self.native_toolbar = None

    def __del__(self):
        self.purge_toolbar()

    def create_menus(self):
        # macOS doesn't have window-level menus
        pass

    def create_toolbar(self):
        # Purge any existing toolbar items
        self.purge_toolbar()

        # Create the new toolbar items.
        if self.interface.toolbar:
            for cmd in self.interface.toolbar:
                if isinstance(cmd, Command):
                    self._toolbar_items[toolbar_identifier(cmd)] = cmd

            self.native_toolbar = NSToolbar.alloc().initWithIdentifier(
                "Toolbar-%s" % id(self)
            )
            self.native_toolbar.setDelegate(self.native)
        else:
            self.native_toolbar = None

        self.native.setToolbar(self.native_toolbar)

        # Adding/removing a toolbar changes the size of the content window.
        if self.interface.content:
            self.interface.content.refresh()

    def purge_toolbar(self):
        while self._toolbar_items:
            dead_items = []
            _, cmd = self._toolbar_items.popitem()
            # The command might have toolbar representations on multiple window
            # toolbars, and may have other representations (at the very least, a menu
            # item). Only clean up the representation pointing at *this* window. Do this
            # in 2 passes so that we're not modifying the set of native objects while
            # iterating over it.
            for item_native in cmd._impl.native:
                if (
                    isinstance(item_native, NSToolbarItem)
                    and item_native.target == self.native
                ):
                    dead_items.append(item_native)

            for item_native in dead_items:
                cmd._impl.native.remove(item_native)
