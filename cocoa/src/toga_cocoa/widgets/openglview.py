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

    @objc_method
    def prepareOpenGL(self) -> None:
        # super().prepareOpenGL()
        self.openGLContext.makeCurrentContext()
        self.interface.renderer.on_init(self.interface)

    @objc_method
    def drawRect_(self, rect: NSRect) -> None:
        size = (int(rect.size.width), int(rect.size.height))
        self.openGLContext.makeCurrentContext()
        self.interface.renderer.on_render(self.interface, size=size)
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


class OpenGLView(Widget):
    def create(self):
        self.native = TogaOpenGLView.alloc().init()
        # try to fail gracefully if we can't set things up correctly
        # can't test, as this would only occur on an older machine/macOS version
        if self.native is None:  # pragma: no cover
            raise RuntimeError("Can't create native OpenGLView widget.")
        self.native.interface = self.interface
        self.native.impl = self

        # Add the layout constraints
        self.add_constraints()

    def redraw(self):
        self.native.needsDisplay = True

    # Rehint
    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.intrinsic.height = at_least(fitting_size.height)
        self.interface.intrinsic.width = at_least(fitting_size.width)
