from toga_iOS.libs import opengles as GL

# This is a very basic renderer using ctypes, because there are currently no
# Python Open GL ES wrappers for iOS

# Constants
GL_COLOR_BUFFER_BIT = 16384


class Renderer:
    def on_init(self, widget, **kwargs):
        # set the clear color to blue
        GL.glClearColor(0.0, 0.0, 1.0, 1.0)

    def on_render(self, widget, size, **kwargs):
        # clear the OpenGL view
        GL.glClear(GL_COLOR_BUFFER_BIT)
