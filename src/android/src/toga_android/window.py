from .libs.android import R__id
from .libs.android.view import ViewTreeObserver__OnGlobalLayoutListener


class AndroidViewport(ViewTreeObserver__OnGlobalLayoutListener):
    def __init__(self, native, container):
        """
        :param native: A native widget whose size will be tracked.
        :param container: An object with a ``content`` attribute, which will have
            ``refresh()`` called on it whenever the native widget's size changes.
        """
        super().__init__()
        self.native = native
        self.container = container
        self.last_size = (None, None)
        native.getViewTreeObserver().addOnGlobalLayoutListener(self)

        self.dpi = native.getContext().getResources().getDisplayMetrics().densityDpi
        # Toga needs to know how the current DPI compares to the platform default,
        # which is 160: https://developer.android.com/training/multiscreen/screendensities
        self.baseline_dpi = 160
        self.scale = float(self.dpi) / self.baseline_dpi

    def onGlobalLayout(self):
        """This listener is run after each native layout pass. If any view's size or
        position has changed, the new values will be visible here.
        """
        new_size = (self.width, self.height)
        if self.last_size != new_size:
            self.last_size = new_size
            if self.container.content:
                self.container.content.refresh()

    @property
    def width(self):
        return self.native.getWidth()

    @property
    def height(self):
        return self.native.getHeight()


class Window:
    def __init__(self, interface, title, position, size):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        # self.set_title(title)

    def set_app(self, app):
        self.app = app
        self.viewport = AndroidViewport(
            self.app.native.findViewById(R__id.content).__global__(),
            self.interface
        )

    def clear_content(self):
        if self.interface.content:
            for child in self.interface.content.children:
                child._impl.container = None

    def set_content(self, widget):
        # Set the widget's viewport to be based on the window's content.
        widget.viewport = self.viewport
        # Set the app's entire contentView to the desired widget. This means that
        # calling Window.set_content() on any Window object automatically updates
        # the app, meaning that every Window object acts as the MainWindow.
        self.app.native.setContentView(widget.native)

        # Attach child widgets to widget as their container.
        for child in widget.interface.children:
            child._impl.container = widget

    def get_title(self):
        return str(self.app.native.getTitle())

    def set_title(self, title):
        self.app.native.setTitle(title)

    def get_position(self):
        return (0, 0)

    def set_position(self, position):
        # Does nothing on mobile
        pass

    def get_size(self):
        return self.viewport.last_size

    def set_size(self, size):
        # Does nothing on mobile
        pass

    def create_toolbar(self):
        pass

    def show(self):
        pass

    def hide(self):
        # A no-op, as the window cannot be hidden.
        pass

    def get_visible(self):
        # The window is alays visible
        return True

    def close(self):
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')
