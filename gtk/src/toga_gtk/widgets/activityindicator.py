from ..libs import ADW_VERSION, GTK_VERSION, Adw, Gtk
from .base import Widget


class ActivityIndicator(Widget):
    # libadwaita 1.6.0 is not in Ubuntu 24.04 yet; no-cover it.
    if Adw is not None and ADW_VERSION >= (1, 6, 0):  # pragma: no cover

        def create(self):
            self.native = Adw.Spinner()
            self._hidden = False
            self._running = False

        def set_hidden(self, hidden):
            super().set_hidden(not self._running or hidden)
            self._hidden = hidden

        def start(self):
            self._running = True
            super().set_hidden(self._hidden)

        def stop(self):
            self._running = False
            super().set_hidden(True)

        def is_running(self):
            return self._running

        def rehint(self):
            # libadwaita spinners could take on any size;
            # getting preferred size would not work.  Hardcode
            # a reasonable size based on documented limits.
            self.interface.intrinsic.width = 32
            self.interface.intrinsic.height = 32

    else:  # pragma: no-cover-unless-plain-gtk

        def create(self):
            self.native = Gtk.Spinner()

        def start(self):
            self.native.start()

        def stop(self):
            self.native.stop()

        def is_running(self):
            if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
                return self.native.get_property("active")
            else:  # pragma: no-cover-if-gtk3
                return self.native.get_property("spinning")

        def rehint(self):
            if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
                # print(
                #     "REHINT",
                #     self,
                #     self.native.get_preferred_width(),
                #     self.native.get_preferred_height(),
                # )
                width = self.native.get_preferred_width()[0]
                height = self.native.get_preferred_height()[0]
            else:  # pragma: no-cover-if-gtk3
                size = self.native.get_preferred_size()[0]
                width, height = size.width, size.height
            self.interface.intrinsic.width = width
            self.interface.intrinsic.height = height
