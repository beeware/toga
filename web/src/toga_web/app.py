import toga
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

        formal_name = self.interface.formal_name

        self.interface.commands.add(
            # ---- Help menu ----------------------------------
            toga.Command(
                lambda _: self.interface.about(),
                "About " + formal_name,
                group=toga.Group.HELP,
            ),
            toga.Command(
                None,
                "Preferences",
                group=toga.Group.HELP,
            ),
        )

        # Create the menus.
        self.create_menus()

        # Call user code to populate the main window
        self.interface.startup()

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
            if cmd == toga.GROUP_BREAK:
                submenu = None
            elif cmd == toga.SECTION_BREAK:
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
                menu_item.onclick = cmd.action

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

        self.menubar = create_element(
            "header",
            classes=["toga"],
            children=[
                create_element(
                    "a",
                    classes=["brand"],
                    content=(
                        '<img src="static/logo-32.png" '
                        'class="d-inline-block align-top" '
                        f'alt="{self.interface.formal_name} logo" '
                        'loading="lazy">'
                    ),
                ),
                menu_container,
                help_menu_container,
            ],
        )

        # Menubar exists at the app level.
        app_placeholder = js.document.getElementById("app-placeholder")
        app_placeholder.appendChild(self.menubar)

    def main_loop(self):
        self.create()

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        about_text = f"{self.interface.formal_name}"

        if self.interface.version is not None:
            about_text += f" v{self.interface.version}"

        if self.interface.author is not None:
            about_text += "\n\nCopyright © {author}".format(
                author=self.interface.author
            )

        js.alert(about_text)

    def exit(self):
        pass

    def current_window(self):
        self.interface.factory.not_implemented("App.current_window()")

    def enter_full_screen(self, windows):
        self.interface.factory.not_implemented("App.enter_full_screen()")

    def exit_full_screen(self, windows):
        self.interface.factory.not_implemented("App.exit_full_screen()")

    def show_cursor(self):
        self.interface.factory.not_implemented("App.show_cursor()")

    def hide_cursor(self):
        self.interface.factory.not_implemented("App.hide_cursor()")
