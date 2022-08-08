from .libs.android.view import ViewTreeObserver__OnGlobalLayoutListener


class AndroidViewport:
    # `content_parent` should be the view that will become the parent of the widget passed to
    # `Window.set_content`. This ensures that the viewport `width` and `height` attributes
    # return the usable area of the app, not including the action bar or status bar.
    def __init__(self, app):
        self.app = app
        self.dpi = app.native.getResources().getDisplayMetrics().densityDpi
        # Toga needs to know how the current DPI compares to the platform default,
        # which is 160: https://developer.android.com/training/multiscreen/screendensities
        self.baseline_dpi = 160
        self.scale = float(self.dpi) / self.baseline_dpi

    @property
    def width(self):
        return self.app.content_parent.getWidth()

    @property
    def height(self):
        return self.app.content_parent.getHeight()


class Window(ViewTreeObserver__OnGlobalLayoutListener):
    def __init__(self, interface, title, position, size):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self.last_size = (None, None)

        # self.set_title(title)

    def set_app(self, app):
        self.app = app
        self.viewport = AndroidViewport(app)
        app.content_parent.getViewTreeObserver().addOnGlobalLayoutListener(self)

    def onGlobalLayout(self):
        """This listener is run after each native layout pass. If any view's size or position has
        changed, the new values will be visible here.
        """
        new_size = (self.viewport.width, self.viewport.height)
        if self.last_size != new_size:
            self.last_size = new_size
            if self.interface.content:
                self.interface.content.refresh()

    def set_content(self, widget):
        # Set the widget's viewport to be based on the window's content.
        widget.viewport = self.viewport

        # Set the activity's entire content to the desired widget. This means that
        # every Window object currently acts as the MainWindow.
        self.app.content_parent.removeAllViews()
        self.app.content_parent.addView(widget.native)

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
        return self.last_size

    def set_size(self, size):
        # Does nothing on mobile
        pass

    def create_toolbar(self):
        pass

    def show(self):
        pass

    def close(self):
        pass

    def set_full_screen(self, is_full_screen):
        self.interface.factory.not_implemented('Window.set_full_screen()')
