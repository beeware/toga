{{ component_header("OpenGLView", width=300) }}

## Usage

OpenGLView provides a surface for rendering 2D and 3D graphics using OpenGL.  It is agnostic to the library used to actually perform the OpenGL rendering: some platforms, such as Qt and Android, provide native OpenGL interfaces while for others, notably Cocoa and Gtk, can use existing Python OpenGL wrappers such as PyOpenGL or ModernGL.  Currently Toga doesn't provide a cross-platform OpenGL API layer, although it may in the future.

The OpenGLView expects to be given a renderer object which conforms to the [`RendererT`][toga.widgets.openglview.RendererT] protocol: it needs an `on_init` method which gets called by the implementation layer to perform any OpenGL initialization that is needed (eg. creating shader programs, setting up buffers); and an `on_render` method which gets called to do the actual OpenGL drawing. Both methods get called with the OpenGL context for the view set up and ready to be accessed by OpenGL library calls.

For example, a renderer that just clears the view using PyOpenGL could be written like this:
``` python
from OpenGL import GL

class ClearRenderer:
    def on_init(self, widget, **kwargs):
        # set the clear color to blue
        GL.glClearColor(0.0, 0.0, 1.0, 1.0)

    def on_render(self, widget, size, **kwargs):
        # clear the OpenGL view
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
```
The OpenGLView can then be initialized by calling it with the renderer:
``` python
renderer = ClearRenderer()
openglview = OpenGLView(renderer)
```

If the renderer changes state and a re-rendering is required, the `redraw` method will schedule the backend to refresh the OpenGLView and trigger `on_render` via the application's event loop.

## Notes

- The OpenGLView API should be considered a beta API and may change in the future.
- The renderer object used by the OpenGLView can't be changed after the view is created, but it can hold state and change the way that it renders based on that.
- The OpenGLView is currently only available on the Android, Cocoa, Gtk, iOS and Qt backends.
- OpenGL is deprecated on macOS and iOS, but it is likely to be available for the foreseeable future.
- There are currently no Python OpenGL wrappers for iOS, but `ctypes` can be used to wrap the iOS `opengles` DLL and call out to OpenGL.
- Linux relies on the appropriate OpenGL driver libraries being installed on the system with the system's package manager.

The version of OpenGL that is available on each platform depends heavily on the platform: mobile and web platforms provide OpenGL ES, while desktop platforms generally provide full OpenGL support.  The OpenGLView tries to provide an OpenGL context with the highest OpenGL version available. This is currently:

- Android: OpenGL ES 3.0
- MacOS: OpenGL 4.1
- Qt: OpenGL 4.1

## Reference

::: toga.OpenGLView

::: toga.widgets.openglview.RendererT
