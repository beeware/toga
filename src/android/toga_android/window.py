from . import dialogs
from .libs.android_widgets import R__attr, TypedValue


class AndroidViewport:
    def __init__(self, native):
        self.native = native
        self.dpi = self.native.getContext().getResources().getDisplayMetrics().densityDpi
        # Toga needs to know how the current DPI compares to the platform default,
        # which is 160: https://developer.android.com/training/multiscreen/screendensities
        self.baseline_dpi = 160

    @property
    def width(self):
        return self.native.getContext().getResources().getDisplayMetrics().widthPixels

    @property
    def height(self):
        screen_height = self.native.getContext().getResources().getDisplayMetrics().heightPixels
        return screen_height - self._status_bar_height() - self._action_bar_height()

    def _action_bar_height(self):
        """
        Get the size of the action bar. The action bar shows the app name and can provide some app actions.
        """
        tv = TypedValue()
        has_action_bar_size = self.native.getContext().getTheme().resolveAttribute(R__attr.actionBarSize, tv, True)
        if not has_action_bar_size:
            return 0

        return TypedValue.complexToDimensionPixelSize(
            tv.data, self.native.getContext().getResources().getDisplayMetrics())

    def _status_bar_height(self):
        """
        Get the size of the status bar. The status bar is typically rendered above the app,
        showing the current time, battery level, etc.
        """
        resource_id = self.native.getContext().getResources().getIdentifier("status_bar_height", "dimen", "android")
        if resource_id <= 0:
            return 0

        return self.native.getContext().getResources().getDimensionPixelSize(resource_id)


class Window:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        pass

    def set_app(self, app):
        self.app = app

    def set_content(self, widget):
        # Set the widget's viewport to be based on the window's content.
        widget.viewport = AndroidViewport(widget.native)
        # Set the app's entire contentView to the desired widget. This means that
        # calling Window.set_content() on any Window object automatically updates
        # the app, meaning that every Window object acts as the MainWindow.
        self.app.native.setContentView(widget.native)

        # Attach child widgets to widget as their container.
        for child in widget.interface.children:
            child._impl.container = widget
            child._impl.viewport = widget.viewport

    def set_title(self, title):
        pass

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def create_toolbar(self):
        pass

    def show(self):
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')

    def info_dialog(self, title, message):
        dialogs.info(self, title, message)

    def question_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.question_dialog()')

    def confirm_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.confirm_dialog()')

    def error_dialog(self, title, message):
        self.interface.factory.not_implemented('Window.error_dialog()')

    def stack_trace_dialog(self, title, message, content, retry=False):
        self.interface.factory.not_implemented('Window.stack_trace_dialog()')

    def save_file_dialog(self, title, suggested_filename, file_types):
        self.interface.factory.not_implemented('Window.save_file_dialog()')
