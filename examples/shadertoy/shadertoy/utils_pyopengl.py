"""Utility objects and methods for PyOpenGL"""

import OpenGL

# Get spurious errors with Qt backend
OpenGL.ERROR_CHECKING = False

from OpenGL import GL  # noqa: E402

#: Shader version header: this should work on most modern desktops
VERSION_HEADER = "#version 330 core"

# Adapt some functions to common API


def glGetShaderInfoLog(id):
    return GL.glGetShaderInfoLog(id).decode("utf-8")


def glGetProgramInfoLog(id):
    return GL.glGetProgramInfoLog(id).decode("utf-8")


def glGetActiveUniform(id, loc):
    name, size, uniform_type = GL.glGetActiveUniform(id, loc)
    return name.decode("utf-8"), size, uniform_type


def __getattr__(name):
    value = getattr(GL, name)
    if value is not None:
        globals()[name] = value
        return value
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
