import os

from toga import App as toga_App, Icon as toga_Icon

from .libs import Bitmap, WinIcon


class Icon:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        basename, file_extension = os.path.splitext(self.interface.filename)

        # The final icon path is relative to the app.
        app_path = toga_App.app.paths.app

        if not file_extension:
            # If no extension is provided, look for one of the allowed
            # icon types, in preferred format order.
            for extension in ['.ico', '.png', '.bmp']:
                file_path = app_path / (basename + extension)
                if file_path.exists():
                    break
        elif file_extension.lower() in {'.png', '.bmp', '.ico'}:
            # If an icon *is* provided, it must be one of the acceptable types
            file_path = app_path / self.interface.filename
        else:
            # An icon has been specified, but it's not a valid format.
            raise FileNotFoundError(
                "[Winforms] {filename} is not a valid icon".format(
                    filename=self.interface.filename
                )
            )

        # If a file exists, use it.
        if file_path.exists():
            if file_path.suffix == '.ico':
                self.native = WinIcon(str(file_path))
            else:
                icon_bitmap = Bitmap(str(file_path))
                icon_handle = icon_bitmap.GetHicon()
                self.native = WinIcon.FromHandle(icon_handle)
        else:
            raise FileNotFoundError(
                "[Winforms] Can't find icon {filename}".format(
                    filename=self.interface.filename
                )
            )
