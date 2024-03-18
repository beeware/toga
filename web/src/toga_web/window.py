import toga
from toga.command import Separator
from toga_web.libs import create_element, js

from .screens import Screen as ScreenImpl


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self.native = create_element(
            "main",
            id=f"toga_{self.interface.id}",
            classes=["toga", "window", "container"],
            role="main",
        )

        self.set_title(title)

    ######################################################################
    # Native event handlers
    ######################################################################

    def on_close(self, *args):
        pass

    def on_size_allocate(self, widget, allocation):
        pass

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return js.document.title

    def set_title(self, title):
        js.document.title = title

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):
        self.interface.factory.not_implemented("Window.close()")

    def create_menus(self):
        # Simple windows don't have menus
        pass

    def set_app(self, app):
        if len(app.interface.windows) > 1:
            raise RuntimeError("Secondary windows cannot be created on Web")

        app.native.appendChild(self.native)

    def show(self):
        self.native.style = "visibility: visible;"

    ######################################################################
    # Window content and resources
    ######################################################################

    def clear_content(self):
        if self.interface.content:
            for child in self.interface.content.children:
                child._impl.container = None

    def set_content(self, widget):
        # Remove existing content of the window.
        for child in self.native.childNodes:
            self.native.removeChild(child)

        # Add all children to the content widget.
        self.native.appendChild(widget.native)

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self):
        return self.native.offsetWidth, self.native.offsetHeight

    def set_size(self, size):
        # Does nothing on web
        pass

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        return ScreenImpl(js.document.documentElement)

    def get_position(self):
        return 0, 0

    def set_position(self, position):
        # Does nothing on web
        pass

    ######################################################################
    # Window visibility
    ######################################################################

    def get_visible(self):
        self.interface.not_implemented("Window.get_visible()")

    def hide(self):
        self.native.style = "visibility: hidden;"

    ######################################################################
    # Window state
    ######################################################################

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented("Window.set_full_screen()")

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        self.interface.factory.not_implemented("Window.get_image_data()")


class MainWindow(Window):
    def __init__(self, interface, title, position, size):
        super().__init__(interface, title, position, size)

        # Create the window titlebar, with placeholders for the menu items.
        self.native_menu_container = create_element("nav", classes=["menubar"])
        self.native_help_menu_container = create_element("nav", classes=["menubar"])
        self.native_titlebar = create_element(
            "header",
            classes=["toga"],
            children=[
                create_element(
                    "a",
                    classes=["brand"],
                    children=[
                        create_element(
                            "img",
                            src="static/logo-32.png",
                            alt="Logo",
                            loading="lazy",
                        )
                    ],
                ),
                self.native_menu_container,
                self.native_help_menu_container,
            ],
        )

    def set_app(self, app):
        super().set_app(app)
        app.native.insertBefore(self.native_titlebar, self.native)

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

        for cmd in self.interface.app.commands:
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
                    content=self.interface.app.formal_name,
                )
            )

        for group, items in self._menu_groups.items():
            submenu = self._create_submenu(group, items)
            if group != toga.Group.HELP:
                menu_container.appendChild(submenu)
            else:
                help_menu_container.appendChild(submenu)

        self.native_menu_container.replaceWith(menu_container)
        self.native_menu_container = menu_container

        self.native_help_menu_container.replaceWith(help_menu_container)
        self.native_help_menu_container = help_menu_container

    def create_toolbar(self):
        self.interface.factory.not_implemented("Window.create_toolbar()")
