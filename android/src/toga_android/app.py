import asyncio
import warnings

from android.content import Context
from android.graphics.drawable import BitmapDrawable
from android.media import RingtoneManager
from android.view import Menu, MenuItem
from androidx.core.content import ContextCompat
from java import dynamic_proxy
from org.beeware.android import IPythonApp, MainActivity

import toga
from toga.command import Group, Separator
from toga.dialogs import InfoDialog

from .libs import events
from .screens import Screen as ScreenImpl


class TogaApp(dynamic_proxy(IPythonApp)):
    last_requestcode = -1  # A unique ID for native background requests
    running_intents = {}  # dictionary for currently running Intents
    permission_requests = {}  # dictionary for outstanding permission requests
    menuitem_mapping = {}  # dictionary for mapping menuitems to commands

    def __init__(self, app):
        super().__init__()
        self._impl = app
        MainActivity.setPythonApp(self)
        self.native = MainActivity.singletonThis
        print("Python app launched & stored in Android Activity class")

    def onCreate(self):
        print("Toga app: onCreate")

    def onStart(self):
        print("Toga app: onStart")

    def onResume(self):
        print("Toga app: onResume")

    def onPause(self):
        print("Toga app: onPause")  # pragma: no cover

    def onStop(self):
        print("Toga app: onStop")  # pragma: no cover

    def onDestroy(self):
        print("Toga app: onDestroy")  # pragma: no cover

    def onRestart(self):
        print("Toga app: onRestart")  # pragma: no cover

    def onActivityResult(self, requestCode, resultCode, resultData):
        print(f"Toga app: onActivityResult {requestCode=} {resultCode=} {resultData=}")
        try:
            # Retrieve the completion callback; if non-none, invoke it.
            callback = self.running_intents.pop(requestCode)
            # In theory, the callback can be empty; however, we don't
            # have any practical use for this at present, so the branch
            # is marked no-cover
            if callback:  # pragma: no branch
                callback(resultCode, resultData)
        except KeyError:  # pragma: no cover
            # This shouldn't happen; we shouldn't get notified of an
            # intent that we didn't start
            print(f"No intent matching request code {requestCode}")

    def onRequestPermissionsResult(self, requestCode, permissions, grantResults):
        print(
            f"Toga app: onRequestPermissionsResult {requestCode=} {permissions=} {grantResults=}"
        )
        try:
            # Retrieve the completion callback and invoke it.
            callback = self.permission_requests.pop(requestCode)
            callback(permissions, grantResults)
        except KeyError:  # pragma: no cover
            # This shouldn't happen; we shouldn't get notified of an
            # permission that we didn't request.
            print(f"No permission request matching request code {requestCode}")

    def onConfigurationChanged(self, new_config):
        pass  # pragma: no cover

    def onOptionsItemSelected(self, menuitem):
        itemid = menuitem.getItemId()
        if itemid == Menu.NONE:
            # This method also fires when opening submenus
            return False
        else:
            self.menuitem_mapping[itemid].action()
            return True

    def onPrepareOptionsMenu(self, menu):
        # If the main window doesn't have a toolbar, there's no preparation required;
        # this is a simple main window, which can't have commands. This can't be
        # validated in the testbed, so it's marked no-cover.
        if not hasattr(self._impl.interface.main_window, "toolbar"):
            return False  # pragma: no cover

        menu.clear()
        itemid = 1  # 0 is the same as Menu.NONE.
        groupid = 1
        menulist = {}  # dictionary with all menus
        self.menuitem_mapping.clear()

        # create option menu
        for cmd in self._impl.interface.commands:
            if isinstance(cmd, Separator):
                groupid += 1
                continue

            # Toolbar commands are added below.
            if cmd in self._impl.interface.main_window.toolbar:
                continue

            try:
                # Find the menu representing the group for this command
                menugroup = menulist[cmd.group.key]
            except KeyError:
                # Menu doesn't exist yet; create it.
                parentmenu = menu
                groupkey = ()
                # Iterate over the full key, creating submenus as needed
                for section, order, text in cmd.group.key:
                    groupkey += ((section, order, text),)
                    try:
                        menugroup = menulist[groupkey]
                    except KeyError:
                        if len(groupkey) == 1 and text == Group.COMMANDS.text:
                            # Add this group directly to the top-level menu
                            menulist[groupkey] = menu
                            menugroup = menu
                        else:
                            # Add all other groups as submenus
                            menugroup = parentmenu.addSubMenu(
                                groupid, Menu.NONE, Menu.NONE, text
                            )
                            menulist[groupkey] = menugroup
                    parentmenu = menugroup

            # Create menu item
            menuitem = menugroup.add(groupid, itemid, Menu.NONE, cmd.text)
            menuitem.setShowAsActionFlags(MenuItem.SHOW_AS_ACTION_NEVER)
            menuitem.setEnabled(cmd.enabled)
            self.menuitem_mapping[itemid] = cmd
            itemid += 1

        # Create toolbar actions
        if self._impl.interface.main_window:  # pragma: no branch
            prev_group = None
            for cmd in self._impl.interface.main_window.toolbar:
                if isinstance(cmd, Separator):
                    groupid += 1
                    prev_group = None
                    continue

                # A change in group requires adding a toolbar separator
                if prev_group is not None and cmd.group != prev_group:
                    groupid += 1
                    prev_group = None
                else:
                    prev_group = cmd.group

                # Add a menu item for the toolbar command
                menuitem = menu.add(groupid, itemid, Menu.NONE, cmd.text)
                # SHOW_AS_ACTION_IF_ROOM is too conservative, showing only 2 items on
                # a medium-size screen in portrait.
                menuitem.setShowAsActionFlags(MenuItem.SHOW_AS_ACTION_ALWAYS)
                menuitem.setEnabled(cmd.enabled)
                if cmd.icon:
                    menuitem.setIcon(
                        BitmapDrawable(
                            self.native.getResources(), cmd.icon._impl.native
                        )
                    )
                self.menuitem_mapping[itemid] = cmd
                itemid += 1

        # Display the menu.
        return True


class App:
    # Android apps exit when the last window is closed
    CLOSE_ON_LAST_WINDOW = True
    # Android doesn't have command line handling;
    # but saying it does shortcuts the default handling
    HANDLES_COMMAND_LINE = True

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._listener = None

        self.loop = events.AndroidEventLoop()

    @property
    def native(self):
        return self._listener.native if self._listener else None

    def create(self):
        # The `_listener` listens for activity event callbacks. For simplicity,
        # the app's `.native` is the listener's native Java class.
        self._listener = TogaApp(self)

        # Call user code to populate the main window
        self.interface._startup()

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_standard_commands(self):
        pass

    def create_menus(self):
        # Menu items are configured as part of onPrepareOptionsMenu; trigger that
        # handler.
        self.native.invalidateOptionsMenu()

    ######################################################################
    # App lifecycle
    ######################################################################

    def exit(self):
        pass  # pragma: no cover

    def main_loop(self):
        # In order to support user asyncio code, start the Python/Android cooperative event loop.
        self.loop.run_forever_cooperatively()

        # On Android, Toga UI integrates automatically into the main Android event loop by virtue
        # of the Android Activity system.
        self.create()

    def set_icon(self, icon):
        # Android apps don't have runtime icons, so this can't be invoked
        pass  # pragma: no cover

    def set_main_window(self, window):
        if window is None or window == toga.App.BACKGROUND:
            raise ValueError("Apps without main windows are not supported on Android")
        else:
            # The default layout of an Android app includes a titlebar; a simple App
            # then hides that titlebar. We know what type of app we have when the main
            # window is set.
            self.interface.main_window._impl.configure_titlebar()

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        context = self.native.getApplicationContext()
        display_manager = context.getSystemService(Context.DISPLAY_SERVICE)
        screen_list = display_manager.getDisplays()
        return [ScreenImpl(self, screen) for screen in screen_list]

    ######################################################################
    # App capabilities
    ######################################################################

    def beep(self):
        uri = RingtoneManager.getActualDefaultRingtoneUri(
            self.native.getApplicationContext(), RingtoneManager.TYPE_NOTIFICATION
        )
        ringtone = RingtoneManager.getRingtone(self.native.getApplicationContext(), uri)
        ringtone.play()

    def show_about_dialog(self):
        message_parts = []
        if self.interface.version is not None:
            message_parts.append(
                f"{self.interface.formal_name} v{self.interface.version}"
            )
        else:
            message_parts.append(self.interface.formal_name)

        if self.interface.author is not None:
            message_parts.append(f"Author: {self.interface.author}")
        if self.interface.description is not None:
            message_parts.append(f"\n{self.interface.description}")

        # Create and show an info dialog as the about dialog.
        # We don't care about the response.
        asyncio.create_task(
            self.interface.dialog(
                InfoDialog(
                    f"About {self.interface.formal_name}",
                    "\n".join(message_parts),
                )
            )
        )

    ######################################################################
    # Cursor control
    ######################################################################

    def hide_cursor(self):
        pass

    def show_cursor(self):
        pass

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        return self.interface.main_window._impl

    def set_current_window(self, window):
        pass

    ######################################################################
    # Full screen control
    ######################################################################

    def enter_full_screen(self, windows):
        pass

    def exit_full_screen(self, windows):
        pass

    ######################################################################
    # Platform-specific APIs
    ######################################################################

    async def intent_result(self, intent):  # pragma: no cover
        warnings.warn(
            "intent_result has been deprecated; use start_activity",
            DeprecationWarning,
        )
        try:
            result_future = asyncio.Future()

            def complete_handler(code, data):
                result_future.set_result({"resultCode": code, "resultData": data})

            self.start_activity(intent, on_complete=complete_handler)

            await result_future
            return result_future.result()
        except AttributeError:
            raise RuntimeError("No appropriate Activity found to handle this intent.")

    def _native_startActivityForResult(
        self, activity, code, *options
    ):  # pragma: no cover
        # A wrapper around the native method so that it can be mocked during testing.
        self.native.startActivityForResult(activity, code, *options)

    def start_activity(self, activity, *options, on_complete=None):
        """Start a native Android activity.

        :param activity: The Intent/Activity to start
        :param options: Any additional arguments to pass to the native
            ``startActivityForResult`` call.
        :param on_complete: The callback to invoke when the activity
            completes. The callback will be invoked with 2 arguments:
            the result code, and the result data.
        """
        self._listener.last_requestcode += 1
        code = self._listener.last_requestcode

        self._listener.running_intents[code] = on_complete

        self._native_startActivityForResult(activity, code, *options)

    def _native_checkSelfPermission(self, permission):  # pragma: no cover
        # A wrapper around the native method so that it can be mocked during testing.
        return ContextCompat.checkSelfPermission(
            self.native.getApplicationContext(), permission
        )

    def _native_requestPermissions(self, permissions, code):  # pragma: no cover
        # A wrapper around the native method so that it can be mocked during testing.
        self.native.requestPermissions(permissions, code)

    def request_permissions(self, permissions, on_complete):
        """Request a set of permissions from the user.

        :param permissions: The list of permissions to request.
        :param on_complete: The callback to invoke when the permission request
            completes. The callback will be invoked with 2 arguments: the list of
            permissions that were processed, and a second list of the same size,
            containing the grant status of each of those permissions.
        """
        self._listener.last_requestcode += 1
        code = self._listener.last_requestcode

        self._listener.permission_requests[code] = on_complete
        self._native_requestPermissions(permissions, code)
