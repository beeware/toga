from rubicon.objc import objc_method, objc_property
from travertino.size import at_least

from toga.widgets.openglview import TOUCH
from toga_iOS.libs import (
    CGRect,
    CGSize,
    EAGLContext,
    GLKView,
    GLKViewDrawableColorFormatRGBA8888,
    GLKViewDrawableDepthFormat24,
    GLKViewDrawableMultisample4X,
    GLKViewDrawableStencilFormat8,
    kEAGLRenderingAPIOpenGLES3,
)

from .base import Widget


class TogaGLKView(GLKView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)
    initialized = objc_property(object)
    pointer = objc_property(object)
    buttons = objc_property(object)

    @objc_method
    def drawRect_(self, rect: CGRect) -> None:
        if not self.initialized:
            self.interface.renderer.on_init(self.interface)
            self.initialized = True

        width = rect.size.width
        height = rect.size.height
        self.interface.renderer.on_render(
            self.interface,
            size=(width, height),
            pointer=self.pointer,
            buttons=frozenset(self.buttons),
        )

    @objc_method
    def touchesBegan_withEvent_(self, touches, event) -> None:
        position = touches.allObjects()[0].locationInView(self)
        self.buttons.add(TOUCH)
        self.pointer = (position.x, position.y)

    @objc_method
    def touchesMoved_withEvent_(self, touches, event) -> None:
        position = touches.allObjects()[0].locationInView(self)
        self.buttons.add(TOUCH)
        self.pointer = (position.x, position.y)

    @objc_method
    def touchesEnded_withEvent_(self, touches, event) -> None:
        position = touches.allObjects()[0].locationInView(self)
        self.buttons.discard(TOUCH)
        self.pointer = (position.x, position.y)


class OpenGLView(Widget):
    def create(self):
        self.native = TogaGLKView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.pointer = None
        self.native.buttons = set()
        self.native.initialized = False
        self.native.context = EAGLContext.alloc().initWithAPI_(
            kEAGLRenderingAPIOpenGLES3
        )

        # Configure renderbuffers created by the view
        self.native.drawableColorFormat = GLKViewDrawableColorFormatRGBA8888
        self.native.drawableDepthFormat = GLKViewDrawableDepthFormat24
        self.native.drawableStencilFormat = GLKViewDrawableStencilFormat8

        # Enable multisampling
        self.native.drawableMultisample = GLKViewDrawableMultisample4X

        # Add the layout constraints
        self.add_constraints()

    def redraw(self):
        self.native.setNeedsDisplay()

    # Rehint
    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = at_least(fitting_size.height)
