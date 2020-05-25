# import os
# import os.path
# import signal
# import sys
# from urllib.parse import unquote, urlparse

# import toga
# from toga import App as toga_App
# from toga.command import GROUP_BREAK, SECTION_BREAK, Command

from .window import Window


class MainWindow(Window):
    # def create(self):
    #     super().create()
    #     self.native.set_role("MainWindow")
    #     toga_App.app.icon.bind(self.interface.factory)
    #     self.native.set_icon(toga_App.app.icon._impl.native_72.get_pixbuf())

    # def set_app(self, app):
    #     super().set_app(app)

    #     # The GTK docs list set_wmclass() as deprecated (and "pointless")
    #     # but it's the only way I've found that actually sets the
    #     # Application name to something other than '__main__.py'.
    #     self.native.set_wmclass(app.interface.name, app.interface.name)

    def on_close(self, *args):
        pass


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.create()

    def create(self):
        self.interface.startup()

        # self.interface.icon.bind(self.interface.factory)
        # self.resource_path = os.path.dirname(os.path.dirname(NSBundle.mainBundle.bundlePath))

        # formal_name = self.interface.formal_name

        # self.interface.commands.add(
        #     toga.Command(None, 'About ' + formal_name, group=toga.Group.APP),
        #     toga.Command(None, 'Preferences', group=toga.Group.APP),
        #     toga.Command(None, 'Visit homepage', group=toga.Group.HELP)
        # )
        # self._create_app_commands()

        # self._menu_items = {}
        # self.create_menus()

    def create_menus(self):
        self.interface.factory.not_implemented('App.create_menus()')

    def main_loop(self):
        # Main loop is a no-op
        pass

    def set_main_window(self, window):
        self.interface.factory.not_implemented('App.set_main_window()')

    def exit(self):
        self.interface.factory.not_implemented('App.exit()')

    def set_on_exit(self, value):
        pass

    def current_window(self):
        self.interface.factory.not_implemented('App.current_window()')

    def enter_full_screen(self, windows):
        self.interface.factory.not_implemented('App.enter_full_screen()')

    def exit_full_screen(self, windows):
        self.interface.factory.not_implemented('App.exit_full_screen()')

    def show_cursor(self):
        self.interface.factory.not_implemented('App.show_cursor()')

    def hide_cursor(self):
        self.interface.factory.not_implemented('App.hide_cursor()')

    def add_background_task(self, handler):
        self.interface.factory.not_implemented('App.add_background_task()')

    def render(self, state, headers):
        # content = ''.join(
        #     child.__html__()
        #     for child in self.main_window.children
        # )
        content = "App content goes here..."

        return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="shortcut icon" type="image/png" href="/static/favicon.ico"/>

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    <link rel="stylesheet" href="/static/toga.css">

    <title>{self.interface.formal_name}</title>
  </head>
  <body>
    <header>
        <nav class="navbar fixed-top navbar-dark bg-dark">
            <a class="navbar-brand" href="#">
                <img src="/static/logo-32.png" class="d-inline-block align-top" alt="" loading="lazy">
                {self.interface.formal_name}
            </a>
        </nav>
    </header>
    <main class="container" role="main">
    {content}
    </main>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <!--script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script-->
    <!--script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script-->
    <!--script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script-->
  </body>
</html>""".format(
            self=self,
            content=content,
        )
