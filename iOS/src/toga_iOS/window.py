from rubicon.objc import (
    Block,
    NSPoint,
    NSRect,
    NSSize,
    objc_id,
)

from toga.types import Position, Size
from toga_iOS.container import NavigationContainer, RootContainer
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
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self.native = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)

        # Set up a container for the window's content
        self.create_container()

        # Set the size of the content to the size of the window
        self.container.native.frame = self.native.bounds

        # Set the window's root controller to be the container's controller
        self.native.rootViewController = self.container.controller

        # Set the background color of the root content.
        try:
            # systemBackgroundColor() was introduced in iOS 13
            # We don't test on iOS 12, so mark the other branch as nocover
            self.native.backgroundColor = UIColor.systemBackgroundColor()
        except AttributeError:  # pragma: no cover
            self.native.backgroundColor = UIColor.whiteColor

        self.set_title(title)

    def create_container(self):
        # RootContainer provides a titlebar for the window.
        self.container = RootContainer(on_refresh=self.content_refreshed)

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return str(self.container.title)

    def set_title(self, title):
        self.container.title = title

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

    def content_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height

        # If the minimum layout is bigger than the current window, log a warning
        if self.container.width < min_width or self.container.height < min_height:
            print(
                f"Warning: Window content {(min_width, min_height)} "
                f"exceeds available space {(self.container.width, self.container.height)}"
            )

    def set_content(self, widget):
        self.container.content = widget

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        return Size(
            UIScreen.mainScreen.bounds.size.width,
            UIScreen.mainScreen.bounds.size.height,
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
        # The window is always visible
        return True

    def hide(self):
        # A no-op, as the window cannot be hidden.
        pass

    ######################################################################
    # Window state
    ######################################################################

    def set_full_screen(self, is_full_screen):
        # Windows are always full screen
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

        renderer = UIGraphicsImageRenderer.alloc().initWithSize(
            self.container.native.bounds.size
        )

        def render(context):
            self.container.native.drawViewHierarchyInRect(
                self.container.native.bounds, afterScreenUpdates=True
            )

        # Render the full image
        full_image = UIImage.imageWithData(
            renderer.PNGDataWithActions(Block(render, None, objc_id))
        )

        # Get the size of the actual content (offsetting for the header) in raw coordinates.
        container_bounds = self.container.content.native.bounds
        image_bounds = NSRect(
            NSPoint(
                container_bounds.origin.x * UIScreen.mainScreen.scale,
                (container_bounds.origin.y + self.container.top_offset)
                * UIScreen.mainScreen.scale,
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
    def create_container(self):
        # NavigationContainer provides a titlebar for the window.
        self.container = NavigationContainer(on_refresh=self.content_refreshed)

    def create_toolbar(self):
        # No toolbar handling at present
        pass
