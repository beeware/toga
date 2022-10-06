import toga

from toga_web.libs import js, create_element
from toga_web.window import Window


class MainWindow(Window):
    def on_close(self, *args):
        pass


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def create(self):

        self.interface.icon.bind(self.interface.factory)
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

        # self.menubar.innerHTML = f"""
        #     <nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
        #         <div class="container">
        #             <a class="navbar-brand" href="#">
        #                 <img src="static/logo-32.png"
        #                     class="d-inline-block align-top"
        #                     alt=""
        #                     loading="lazy">
        #                 {self.interface.formal_name}
        #             </a>
        #             <button class="navbar-toggler" type="button"
        #                     data-toggle="collapse" data-target="#navbarsExample07"
        #                     aria-controls="navbarsExample07" aria-expanded="false"
        #                     aria-label="Toggle navigation">
        #                 <span class="navbar-toggler-icon"></span>
        #             </button>

        #             <div class="collapse navbar-collapse" id="navbarsExample07">
        #                 <ul class="navbar-nav mr-auto">
        #                     <!--li class="nav-item">
        #                         <a class="nav-link" href="#">Menu</a>
        #                     </li>
        #                     <li class="nav-item">
        #                         <a class="nav-link disabled" href="#">Disabled menu</a>
        #                     </li-->
        #                 </ul>
        #                 <ul class="navbar-nav ml-auto">
        #                     <li class="nav-item dropdown">
        #                         <a class="nav-link dropdown-toggle"
        #                             href="http://example.com" id="dropdown07"
        #                             data-toggle="dropdown"
        #                             aria-haspopup="true"
        #                             aria-expanded="false">Help</a>
        #                         <div class="dropdown-menu" aria-labelledby="dropdown07">
        #                             <a class="dropdown-item" href="#">About</a>
        #                             <a class="dropdown-item" href="#">Preferences</a>
        #                         </div>
        #                     </li>
        #                 </ul>
        #             </div>
        #         </div>
        #     </nav>
        # """

        # Create the menus.
        self.create_menus()

        # Call user code to populate the main window
        self.interface.startup()

    def create_menus(self):

        # self._menu_items = {}
        self._menu_groups = {}
        submenu = None

        help_menu_items = []

        for cmd in self.interface.commands:
            if cmd == toga.GROUP_BREAK:
                submenu = None
            elif cmd == toga.SECTION_BREAK:
                # TODO - add a section break
                pass
            else:
                submenu = self._menu_groups.setdefault(cmd.group, [])

                menu_item = create_element(
                   "a",
                    classes=["dropdown-item"] + ([] if cmd.enabled else ['disabled']),
                    content=cmd.text,
                )
                menu_item.onclick = cmd.action

                submenu.append(menu_item)

        menu_container = create_element(
            "ul",
            classes=["navbar-nav", "mr-auto"],
        )

        for group, items in self._menu_groups.items():
            if group != toga.Group.HELP:
                submenu = create_element(
                    "li",
                    classes=["nav-item", "dropdown"],
                    children=[
                        create_element(
                            "a",
                            id=f"menu-{id(group)}",
                            classes=[
                                "nav-link",
                                "dropdown-toggle",
                            ],
                            data_toggle="dropdown",
                            aria_haspopup="true",
                            aria_expanded="false",
                            content=group,
                        ),
                        create_element(
                            "div",
                            classes=["dropdown-menu"],
                            aria_labelledby=f"menu-{id(group)}",
                            children=items,
                        ),
                    ],
                )
                menu_container.appendChild(submenu)

        help_menu_container = create_element(
            "ul",
            classes=["navbar-nav", "ml-auto"],
            children=[
                create_element(
                    "li",
                    classes=["nav-item", "dropdown"],
                    children=[
                        create_element(
                            "a",
                            id="help-menu",
                            classes=[
                                "nav-link",
                                "dropdown-toggle",
                            ],
                            data_toggle="dropdown",
                            aria_haspopup="true",
                            aria_expanded="false",
                            content="Help",
                        ),
                        create_element(
                            "div",
                            classes=["dropdown-menu"],
                            aria_labelledby="help-menu",
                            children=self._menu_groups[toga.Group.HELP],
                        ),
                    ],
                )
            ],
        )

        self.menubar = create_element(
            "header",
            children=[
                create_element(
                    "nav",
                    classes=[
                        "navbar",
                        "fixed-top",
                        "navbar-expand-lg",
                        "navbar-dark",
                        "bg-dark",
                    ],
                    children=[
                        create_element(
                            "div",
                            classes=["container"],
                            children=[
                                create_element(
                                    "a",
                                    classes=["navbar-brand"],
                                    content=f"""
                                        <img src="static/logo-32.png" class="d-inline-block align-top" alt="{self.interface.formal_name} logo" loading="lazy">
                                        {self.interface.formal_name}
                                    """,
                                ),
                                create_element(
                                    "button",
                                    classes=["navbar-toggler"],
                                    type="button",
                                    data_toggle="collapse",
                                    data_target="#navbarsExample07",
                                    aria_controls="navbarsExample07",
                                    aria_expanded="false",
                                    aria_label="Toggle navigation",
                                    children=[
                                        create_element(
                                            "span", classes=["navbar-toggler-icon"]
                                        )
                                    ],
                                ),
                                create_element(
                                    "div",
                                    id="navbarsExample07",
                                    classes=["collapse", "navbar-collapse"],
                                    children=[
                                        menu_container,
                                        help_menu_container,
                                    ],
                                ),
                            ],
                        )
                    ],
                )
            ],
        )

        # Menubar exists at the app level.
        app_placeholder = js.document.getElementById("app-placeholder")
        app_placeholder.appendChild(self.menubar)

    def main_loop(self, **kwargs):
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

    def set_on_exit(self, value):
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

    def add_background_task(self, handler):
        self.interface.factory.not_implemented("App.add_background_task()")
