from rubicon.objc import (
    Block,
    NSPoint,
    NSRect,
    NSSize,
    objc_id,
)

from toga.constants import WindowState
from toga.types import Position, Size
from toga_iOS.images import nsdata_to_bytes
from toga_iOS.libs import (
    NSData,
    UIColor,
    UIGraphicsImageRenderer,
    UIImage,
    UIScreen,
    UIWindow,
    core_graphics,
    uikit,
)

from .screens import Screen as ScreenImpl


class Window:
    def __init__(self, interface, position, size):
        self.interface = interface
        self.interface._impl = self

        self.native = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)
        self._title = ""

        # Set the background color of the root content.
        try:
            # systemBackgroundColor() was introduced in iOS 13
            # We don't test on iOS 12, so mark the other branch as nocover
            self.native.backgroundColor = UIColor.systemBackgroundColor()
        except AttributeError:  # pragma: no cover
            self.native.backgroundColor = UIColor.whiteColor

        self._navigation_bar_hidden = True

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title
        self.scaffold.title = title

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):  # pragma: no cover
        # An iOS app only ever contains a main window, and that window *can't* be
        # closed, so the platform-specific close handling is never triggered.
        pass

    def set_app(self, app):
        if len(app.interface.windows) > 1:
            raise RuntimeError("Secondary windows cannot be created on iOS")

    def show(self):
        self.native.makeKeyAndVisible()

    ######################################################################
    # Window content and resources
    ######################################################################

    def set_scaffold(self, scaffold):
        self.scaffold = scaffold
        self.native.rootViewController = self.scaffold.nav_controller
        self.scaffold.title = self._title
        self.scaffold.navigation_bar_hidden = self._navigation_bar_hidden

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        return Size(
            int(UIScreen.mainScreen.bounds.size.width),
            int(UIScreen.mainScreen.bounds.size.height),
        )

    def set_size(self, size):
        # Does nothing on mobile
        pass

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        return ScreenImpl(UIScreen.mainScreen)

    def get_position(self) -> Position:
        return Position(0, 0)

    def set_position(self, position):
        # Does nothing on mobile
        pass

    ######################################################################
    # Window visibility
    ######################################################################

    def get_visible(self):
        # The window is hidden as default by the system, unless makeKeyAndVisible
        # has been called on the UIWindow. Requesting the same visibility as the
        # current visibility state is a no-op and is ignored at the core level.
        # So, always check if the window is currently hidden or not, to ensure that
        # the other APIs that are dependent on get_visible() work correctly.
        return not bool(self.native.isHidden())

    def hide(self):
        # A no-op, as the window cannot be hidden.
        pass

    ######################################################################
    # Window state
    ######################################################################

    def get_window_state(self, in_progress_state=False):
        # Windows are always in NORMAL state.
        return WindowState.NORMAL

    def set_window_state(self, state):
        # Window state setting is not implemented on iOS.
        pass

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        # This is... baroque.
        #
        # The iOS root container has an offset at the top, because the root view
        # flows *under* the title bar. We don't want this in the screenshot.
        #
        # You can render a view using UIView.drawViewHierarchyInRect(), which
        # takes a rect defining the region to be captured. It needs to be
        # invoked in a graphics rendering context, which is initialized with a
        # size. You'd *think* that you could specify the size of the final
        # output image, and then render a rectangle that has that size at any
        # position offset you choose... but no. If you do this, you end up with
        # the *full* view, scaled to fit the provided size of the graphics
        # context, with the offset being used in reverse to offset the origin of
        # the scaling function. I'm sure this is useful to someone, but it's not
        # useful to us.
        #
        # So - we capture the *entire* view, then crop to remove the section at
        # the top of the image.
        #
        # Of course, the screenshot functionality uses UIImage, and UIImage has
        # tooling to convert into PNG format... but doesn't contain *crop*
        # functionality.
        #
        # So, we need to convert from UIImage to CGImage, and use Core Graphics
        # to crop the image.
        #
        # Except that UIImage works in scaled coordinate, and Core Graphics
        # works in native coordinates, so we need to do a size transformation
        # along the way.
        #
        # I need a drink.
        container = self.scaffold.current_container

        renderer = UIGraphicsImageRenderer.alloc().initWithSize(
            container.native.bounds.size
        )

        def render(context):
            container.native.drawViewHierarchyInRect(
                container.native.bounds, afterScreenUpdates=True
            )

        # Render the full image
        full_image = UIImage.imageWithData(
            renderer.PNGDataWithActions(Block(render, None, objc_id))
        )

        # Get the size of the actual content (offsetting for the header)
        # in raw coordinates.
        container_bounds = container.content.native.bounds
        image_bounds = NSRect(
            NSPoint(
                container.left_inset * UIScreen.mainScreen.scale,
                container.top_inset * UIScreen.mainScreen.scale,
            ),
            NSSize(
                container_bounds.size.width * UIScreen.mainScreen.scale,
                container_bounds.size.height * UIScreen.mainScreen.scale,
            ),
        )

        # Crop the image,
        cropped_image = core_graphics.CGImageCreateWithImageInRect(
            full_image.CGImage, image_bounds
        )
        # Convert back into a UIGraphics
        final_image = UIImage.imageWithCGImage(cropped_image)
        # Convert into PNG data.
        return nsdata_to_bytes(NSData(uikit.UIImagePNGRepresentation(final_image)))


class MainWindow(Window):
    def create_toolbar(self):
        # No toolbar handling at present
        pass

    def __init__(self, interface, position, size):
        super().__init__(interface, position, size)
        self._navigation_bar_hidden = False
