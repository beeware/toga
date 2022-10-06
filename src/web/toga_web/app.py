try:
    import js
except ImportError:
    js = None

import toga

from .window import Window


class MainWindow(Window):
    def on_close(self, *args):
        pass


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.create()

    def create(self):
        self.interface.startup()

        self.interface.icon.bind(self.interface.factory)
        # self.resource_path = os.path.dirname(os.path.dirname(NSBundle.mainBundle.bundlePath))

        formal_name = self.interface.formal_name
        self.interface.commands.add(
            toga.Command(
                None,
                'About ' + formal_name,
                group=toga.Group.APP
            ),
            toga.Command(None, 'Preferences', group=toga.Group.APP),
        )

    def main_loop(self, **kwargs):
        js.document.getElementById("placeholder").innerHTML = self.__html__()
        js.document.title = self.interface.formal_name

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        self.interface.factory.not_implemented("App.show_about_dialog()")
        js.alert("Hello", "world")

    def exit(self):
        pass

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

    def __html__(self):
        return f"""
    <header>
        <nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="#">
                    <img src="static/logo-32.png"
                        class="d-inline-block align-top"
                        alt=""
                        loading="lazy">
                    {self.interface.formal_name}
                </a>
                <button class="navbar-toggler" type="button"
                        data-toggle="collapse" data-target="#navbarsExample07"
                        aria-controls="navbarsExample07" aria-expanded="false"
                        aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarsExample07">
                    <ul class="navbar-nav mr-auto">
                        <!--li class="nav-item">
                            <a class="nav-link" href="#">Menu</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link disabled" href="#">Disabled menu</a>
                        </li-->
                    </ul>
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle"
                                href="http://example.com" id="dropdown07"
                                data-toggle="dropdown"
                                aria-haspopup="true"
                                aria-expanded="false">Help</a>
                            <div class="dropdown-menu" aria-labelledby="dropdown07">
                                <a class="dropdown-item" href="#">About</a>
                                <a class="dropdown-item" href="#">Preferences</a>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
{self.interface.main_window._impl.__html__()}
"""
