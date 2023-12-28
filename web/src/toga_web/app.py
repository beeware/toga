import toga
from toga.command import Separator
from toga_web.libs import create_element, js
from toga_web.window import Window


class MainWindow(Window):
    def on_close(self, *args):
        pass


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def create(self):
        # self.resource_path = os.path.dirname(os.path.dirname(NSBundle.mainBundle.bundlePath))
        self.native = js.document.getElementById("app-placeholder")

        formal_name = self.interface.formal_name

        self.interface.commands.add(
            # ---- Help menu ----------------------------------
            toga.Command(
                self._menu_about,
                "About " + formal_name,
                group=toga.Group.HELP,
            ),
            toga.Command(
                None,
                "Preferences",
                group=toga.Group.HELP,
            ),
        )

        # Create the menus. This is done before main window content to ensure
        # the <header> for the menubar is inserted before the <main> for the
        # main window.
        self.create_menus()

        # Call user code to populate the main window
        self.interface._startup()

    def _create_submenu(self, group, items):
        submenu = create_element(
            "sl-dropdown",
            children=[
                create_element(
                    "span",
                    id=f"menu-{id(group)}",
                    classes=["menu"],
                    slot="trigger",
                    content=group.text,
                ),
                create_element(
                    "sl-menu",
                    children=items,
                ),
            ],
        )
        return submenu

    def create_menus(self):
        self._menu_groups = {}
        submenu = None

        for cmd in self.interface.commands:
            if isinstance(cmd, Separator):
                # TODO - add a section break
                pass
            else:
                # TODO - this doesn't handle submenus properly;
                # all menu items will appear in their root group.
                submenu = self._menu_groups.setdefault(cmd.group, [])

                menu_item = create_element(
                    "sl-menu-item",
                    content=cmd.text,
                    disabled=not cmd.enabled,
                )
                menu_item.onclick = cmd._impl.dom_click

                submenu.append(menu_item)

        menu_container = create_element("nav", classes=["menubar"])
        help_menu_container = create_element("nav", classes=["menubar"])

        # If there isn't an explicit app menu group, add an inert placeholder
        if toga.Group.APP not in self._menu_groups:
            menu_container.appendChild(
                create_element(
                    "span",
                    classes=["app"],
                    content=self.interface.formal_name,
                )
            )

        for group, items in self._menu_groups.items():
            submenu = self._create_submenu(group, items)
            if group != toga.Group.HELP:
                menu_container.appendChild(submenu)
            else:
                help_menu_container.appendChild(submenu)

        menubar_id = f"{self.interface.app_id}-header"
        self.menubar = create_element(
            "header",
            id=menubar_id,
            classes=["toga"],
            children=[
                create_element(
                    "a",
                    classes=["brand"],
                    children=[
                        create_element(
                            "img",
                            src="static/logo-32.png",
                            alt=f"{self.interface.formal_name} logo",
                            loading="lazy",
                        )
                    ],
                ),
                menu_container,
                help_menu_container,
            ],
        )

        # If there's an existing menubar, replace it.
        old_menubar = js.document.getElementById(menubar_id)
        if old_menubar:
            old_menubar.replaceWith(self.menubar)
        else:
            self.native.append(self.menubar)

    def _menu_about(self, command, **kwargs):
        self.interface.about()

    def main_loop(self):
        self.create()

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        name_and_version = f"{self.interface.formal_name}"

        if self.interface.version is not None:
            name_and_version += f" v{self.interface.version}"

        if self.interface.author is not None:
            copyright = f"\n\nCopyright © {self.interface.author}"

        close_button = create_element(
            "sl-button", slot="footer", variant="primary", content="Ok"
        )
        about_dialog = create_element(
            "sl-dialog",
            id="toga-about-dialog",
            label="About",
            children=[
                create_element("p", content=name_and_version),
                create_element("p", content=copyright),
                close_button,
            ],
        )

        # Create a button handler to capture the close,
        # and destroy the dialog
        def dialog_close(event):
            about_dialog.hide()
            self.native.removeChild(about_dialog)

        close_button.onclick = dialog_close

        # Add the dialog to the DOM.
        self.native.appendChild(about_dialog)

        # If this is the first time a dialog is being shown, the Shoelace
        # autoloader needs to construct the Dialog custom element. We can't
        # display the dialog until that element has been fully loaded and
        # constructed. Only show the dialog when the promise of <sl-dialog>
        # element construction has been fulfilled.
        def show_dialog(promise):
            about_dialog.show()

        js.customElements.whenDefined("sl-dialog").then(show_dialog)

    def beep(self):
        self.interface.factory.not_implemented("App.beep()")

    def exit(self):
        pass

    def get_current_window(self):
        self.interface.factory.not_implemented("App.get_current_window()")

    def set_current_window(self):
        self.interface.factory.not_implemented("App.set_current_window()")

    def enter_full_screen(self, windows):
        self.interface.factory.not_implemented("App.enter_full_screen()")

    def exit_full_screen(self, windows):
        self.interface.factory.not_implemented("App.exit_full_screen()")

    def show_cursor(self):
        self.interface.factory.not_implemented("App.show_cursor()")

    def hide_cursor(self):
        self.interface.factory.not_implemented("App.hide_cursor()")
