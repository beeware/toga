import ctypes

from rubicon.objc import objc_method, objc_property
from travertino.size import at_least

from toga_cocoa.libs import (
    NSOpenGLPFADoubleBuffer,
    NSOpenGLPFAOpenGLProfile,
    NSOpenGLPixelFormat,
    NSOpenGLProfileVersion4_1Core,
    NSOpenGLView,
    NSRect,
)

from .base import Widget


class TogaOpenGLView(NSOpenGLView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)
    mouse_state = objc_property(object)

    @objc_method
    def prepareOpenGL(self) -> None:
        self.openGLContext.makeCurrentContext()
        try:
            self.interface.renderer.on_init(self.interface)
        except Exception as exc:
            print(exc)
            raise

    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        # Get size in GL pixels
        backingBounds = self.convertRectToBacking(self.bounds)
        size = (backingBounds.size.width, backingBounds.size.height)

        # Get current mouse position in GL pixels
        position = self.convertPoint(
            self.window.mouseLocationOutsideOfEventStream(),
            fromView=None,
        )
        scale = self.backingScaleFactor
        pointer = (position.x * scale, position.y * scale)

        self.openGLContext.makeCurrentContext()
        try:
            self.interface.renderer.on_render(
                self.interface,
                size=size,
                pointer=pointer,
                buttons=tuple(self.mouse_state),
            )
        except Exception as exc:
            print(exc)
            raise
        self.openGLContext.flushBuffer()

    @objc_method
    def initWithFrame_(self, frame: NSRect):
        a = (
            NSOpenGLPFADoubleBuffer,
            NSOpenGLPFAOpenGLProfile,
            NSOpenGLProfileVersion4_1Core,
        )
        attributes = (ctypes.c_uint32 * len(a))(*a)
        pixel_format = NSOpenGLPixelFormat.alloc().initWithAttributes_(attributes)
        # try help pinpoint the failure if we can't set things up correctly
        # can't test, as this would only occur on an older machine/macOS version
        if pixel_format is None:  # pragma: no cover
            # warnings cause segfault here, so just print
            print("Can't create NSOpenGLPixelFormat with required properties.")
            return None

        return self.initWithFrame_pixelFormat_(frame, pixel_format)

    @objc_method
    def mouseDown_(self, event) -> None:
        self.mouse_state[0] = True

    @objc_method
    def mouseUp_(self, event) -> None:
        self.mouse_state[0] = False

    @objc_method
    def otherMouseDown_(self, event) -> None:
        self.mouse_state[1] = True

    @objc_method
    def otherMouseUp_(self, event) -> None:
        self.mouse_state[1] = False

    @objc_method
    def rightMouseDown_(self, event) -> None:
        self.mouse_state[2] = True

    @objc_method
    def rightMouseUp_(self, event) -> None:
        self.mouse_state[2] = False


class OpenGLView(Widget):
    def create(self):
        self.native = TogaOpenGLView.alloc().init()
        # try to fail gracefully if we can't set things up correctly
        # can't test, as this would only occur on an older machine/macOS version
        if self.native is None:  # pragma: no cover
            raise RuntimeError("Can't create native OpenGLView widget.")
        self.native.interface = self.interface
        self.native.impl = self
        self.native.mouse_state = [False, False, False]

        # Add the layout constraints
        self.add_constraints()

    def redraw(self):
        self.native.needsDisplay = True

    # Rehint
    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = at_least(fitting_size.height)
        self.interface.intrinsic.width = at_least(fitting_size.width)
