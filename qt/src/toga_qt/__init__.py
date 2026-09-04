from importlib.metadata import version

__version__ = version("toga-qt")


def _init_opengl():
    """OpenGL initialization needed before QApplication started.

    This sets the default OpenGL profile and version.
    """
    from PySide6.QtGui import QSurfaceFormat

    surface_format = QSurfaceFormat.defaultFormat()
    surface_format.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    surface_format.setVersion(4, 1)
    QSurfaceFormat.setDefaultFormat(surface_format)


_init_opengl()
del _init_opengl
