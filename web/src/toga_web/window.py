from toga.command import Group, Separator
from toga.types import Position, Size
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

        app_placeholder = js.document.getElementById("app-placeholder")
        app_placeholder.appendChild(self.native)

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

    def set_app(self, app):
        pass

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

    def get_size(self) -> Size:
        return Size(self.native.offsetWidth, self.native.offsetHeight)

    def set_size(self, size):
        # Does nothing on web
        pass

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        return ScreenImpl(js.document.documentElement)

    def get_position(self) -> Position:
        return Position(0, 0)

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
        if Group.APP not in self._menu_groups:
            menu_container.appendChild(
                create_element(
                    "span",
                    classes=["app"],
                    content=self.interface.app.formal_name,
                )
            )

        for group, items in self._menu_groups.items():
            submenu = self._create_submenu(group, items)
            if group != Group.HELP:
                menu_container.appendChild(submenu)
            else:
                help_menu_container.appendChild(submenu)

        menubar_id = f"{self.interface.id}-header"
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
                            alt=f"{self.interface.app.formal_name} logo",
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
            self.native.prepend(self.menubar)

    def create_toolbar(self):
        self.interface.factory.not_implemented("Window.create_toolbar()")
