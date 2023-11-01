import asyncio
import sys

from android.graphics.drawable import BitmapDrawable
from android.media import RingtoneManager
from android.view import Menu, MenuItem
from java import dynamic_proxy
from org.beeware.android import IPythonApp, MainActivity

from toga.command import GROUP_BREAK, SECTION_BREAK, Command, Group

from .libs import events
from .window import Window


class MainWindow(Window):
    _is_main_window = True


class TogaApp(dynamic_proxy(IPythonApp)):
    last_intent_requestcode = (
        -1
    )  # always increment before using it for invoking new Intents
    running_intents = {}  # dictionary for currently running Intents
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

    # TODO #1798: document and test this somehow
    def onActivityResult(self, requestCode, resultCode, resultData):  # pragma: no cover
        """Callback method, called from MainActivity when an Intent ends.

        :param int requestCode: The integer request code originally supplied to startActivityForResult(),
                                allowing you to identify who this result came from.
        :param int resultCode: The integer result code returned by the child activity through its setResult().
        :param Intent resultData: An Intent, which can return result data to the caller (various data can be attached
                                  to Intent "extras").
        """
        print(
            f"Toga app: onActivityResult, requestCode={requestCode}, resultData={resultData}"
        )
        try:
            # remove Intent from the list of running Intents,
            # and set the result of the intent.
            result_future = self.running_intents.pop(requestCode)
            result_future.set_result(
                {"resultCode": resultCode, "resultData": resultData}
            )
        except KeyError:
            print("No intent matching request code {requestCode}")

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
        menu.clear()
        itemid = 1  # 0 is the same as Menu.NONE.
        groupid = 1
        menulist = {}  # dictionary with all menus
        self.menuitem_mapping.clear()

        # create option menu
        for cmd in self._impl.interface.commands:
            if cmd == SECTION_BREAK or cmd == GROUP_BREAK:
                groupid += 1
                continue

            # Toolbar commands are added below.
            if cmd in self._impl.interface.main_window.toolbar:
                continue

            if cmd.group.key in menulist:
                menugroup = menulist[cmd.group.key]
            else:
                # create all missing submenus
                parentmenu = menu
                groupkey = ()
                for section, order, text in cmd.group.key:
                    groupkey += ((section, order, text),)
                    if groupkey in menulist:
                        menugroup = menulist[groupkey]
                    else:
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

            # create menu item
            menuitem = menugroup.add(groupid, itemid, Menu.NONE, cmd.text)
            menuitem.setShowAsActionFlags(MenuItem.SHOW_AS_ACTION_NEVER)
            menuitem.setEnabled(cmd.enabled)
            self.menuitem_mapping[itemid] = cmd
            itemid += 1

        # create toolbar actions
        if self._impl.interface.main_window:  # pragma: no branch
            for cmd in self._impl.interface.main_window.toolbar:
                if cmd == SECTION_BREAK or cmd == GROUP_BREAK:
                    groupid += 1
                    continue

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

        self.interface.commands.add(
            # About should be the last item in the menu, in a section on its own.
            Command(
                lambda _: self.interface.about(),
                f"About {self.interface.formal_name}",
                section=sys.maxsize,
            ),
        )

    def create_menus(self):
        self.native.invalidateOptionsMenu()  # Triggers onPrepareOptionsMenu

    def main_loop(self):
        # In order to support user asyncio code, start the Python/Android cooperative event loop.
        self.loop.run_forever_cooperatively()

        # On Android, Toga UI integrates automatically into the main Android event loop by virtue
        # of the Android Activity system.
        self.create()

    def set_main_window(self, window):
        pass

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
        self.interface.main_window.info_dialog(
            f"About {self.interface.formal_name}", "\n".join(message_parts)
        )

    def beep(self):
        uri = RingtoneManager.getActualDefaultRingtoneUri(
            self.native.getApplicationContext(), RingtoneManager.TYPE_NOTIFICATION
        )
        ringtone = RingtoneManager.getRingtone(self.native.getApplicationContext(), uri)
        ringtone.play()

    def exit(self):
        pass  # pragma: no cover

    def get_current_window(self):
        return self.interface.main_window._impl

    def set_current_window(self, window):
        pass

    # TODO #1798: document and test this somehow
    async def intent_result(self, intent):  # pragma: no cover
        """Calls an Intent and waits for its result.

        A RuntimeError will be raised when the Intent cannot be invoked.

        :param Intent intent: The Intent to call
        :returns: A Dictionary containing "resultCode" (int) and "resultData" (Intent or None)
        :rtype: dict
        """
        try:
            self._listener.last_intent_requestcode += 1
            code = self._listener.last_intent_requestcode

            result_future = asyncio.Future()
            self._listener.running_intents[code] = result_future

            self.native.startActivityForResult(intent, code)
            await result_future
            return result_future.result()
        except AttributeError:
            raise RuntimeError("No appropriate Activity found to handle this intent.")

    def enter_full_screen(self, windows):
        pass

    def exit_full_screen(self, windows):
        pass

    def hide_cursor(self):
        pass

    def show_cursor(self):
        pass
