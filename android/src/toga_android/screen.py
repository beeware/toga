from android.view import WindowInsets, WindowManager

from toga.screen import Screen as ScreenInterface


class Screen:
    _instances = {}

    def __new__(cls, native):
        if native in cls._instances:
            return cls._instances[native]
        else:
            instance = super().__new__(cls)
            instance.interface = ScreenInterface(_impl=instance)
            instance.native = native
            cls._instances[native] = instance
            return instance

    def get_name(self):
        return self.native.getName()

    def get_origin(self):
        return (0, 0)

    def get_size(self):
        metrics = WindowManager.getCurrentWindowMetrics()
        window_insets = metrics.getWindowInsets()
        insets = window_insets.getInsetsIgnoringVisibility(
            WindowInsets.Type.navigationBars() | WindowInsets.Type.displayCutout()
        )
        insets_width = insets.right + insets.left
        insets_height = insets.top + insets.bottom
        bounds = metrics.getBounds()
        return (bounds.width() - insets_width, bounds.height() - insets_height)

    def get_image_data(self):
        self.interface.factory.not_implemented("Screen.get_image_data()")
