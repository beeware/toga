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
                self.interface.about_command,
                'About ' + formal_name,
                group=toga.Group.APP
            ),
            toga.Command(None, 'Preferences', group=toga.Group.APP),
        )

    def main_loop(self):
        # Main loop is a no-op
        pass

    def set_main_window(self, window):
        pass

    def show_about_dialog(self):
        self.interface.factory.not_implemented("App.show_about_dialog()")

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

    def render(self, state, headers):
        return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="shortcut icon" type="image/png" href="/static/favicon.ico"/>

    <!-- Bootstrap CSS -->
    <link rel="stylesheet"
          href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
          integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
          crossorigin="anonymous">
    <link rel="stylesheet" href="/static/toga.css">

    <title>{self.interface.formal_name}</title>
  </head>
  <body>
    <header>
        <nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="#">
                    <img src="/static/logo-32.png"
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
{main_window}
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
        crossorigin="anonymous">
        </script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
        integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
        crossorigin="anonymous">
        </script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"
        integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"
        crossorigin="anonymous">
        </script>
  </body>
</html>""".format(
            self=self,
            main_window=self.interface.main_window._impl.__html__(),
        )
