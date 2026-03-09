from PySide6.QtGui import QOpenGLContext
from PySide6.QtOpenGL import QOpenGLShader
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from travertino.size import at_least

from toga.widgets.gl.openglcontext import OpenGLContext

from .base import Widget


class QtOpenGLShader:
    def __init__(self, native_shader: QOpenGLShader):
        self.native = native_shader


class QtOpenGLContext(OpenGLContext):
    """The implementation layer of a Qt OpenGL context."""

    def __init__(self, native_context: QOpenGLContext):
        self.native = native_context
        self.functions = native_context.functions()

    def clear_color(self, r: float, g: float, b: float, a: float):
        self.functions.glClearColor(r, g, b, a)

    def clear(self, mask: int):
        self.functions.glClear(mask)

    def create_shader(self, type: int):
        return self.functions.glCreateShader(type)

    def shader_source(self, shader: int, source: str):
        self.functions.glShaderSource(shader, source)

    def compile_shader(self, shader: int):
        self.functions.glCompileShader(shader)

    def delete_shader(self, shader):
        self.functions.glDeleteShader(shader)

    def create_program(self) -> int:
        return self.functions.glCreateProgram()

    def attach_shader(self, program: int, shader: int):
        self.functions.glAttachShader(program, shader)

    def link_program(self, program: int):
        self.functions.glLinkProgram(program)

    def delete_program(self, program):
        self.functions.glDeleteProgram(program)


class GLWidget(QOpenGLWidget):
    def __init__(self, impl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.impl = impl
        self.interface = impl.interface

    def initializeGL(self):
        pass

    def resizeGL(self, w, h):
        self._redraw()

    def paintGL(self):
        self._redraw()

    def _redraw(self):
        context = QtOpenGLContext(QOpenGLContext.currentContext())
        self.interface.on_render(context)


class OpenGLView(Widget):
    def create(self):
        self.native = GLWidget(self)

    def redraw(self):
        self.native.update()

    # Rehint
    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(size.width(), self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = at_least(
            max(size.height(), self.interface._MIN_HEIGHT)
        )


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         central = QWidget()
#         layout = QVBoxLayout(central)

#         self.gl = GLWidget()
#         layout.addWidget(self.gl)

#         self.setCentralWidget(central)
#         self.resize(800, 600)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Explicit OpenGL format
#     fmt = QSurfaceFormat()
#     fmt.setRenderableType(QSurfaceFormat.OpenGL)
#     fmt.setProfile(QSurfaceFormat.CoreProfile)
#     fmt.setVersion(3, 3)
#     fmt.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
#     QSurfaceFormat.setDefaultFormat(fmt)

#     w = MainWindow()
#     w.show()

#     sys.exit(app.exec())
