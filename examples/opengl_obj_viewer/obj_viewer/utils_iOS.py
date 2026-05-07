"""Utility objects and methods for iOS"""

from ctypes import byref, c_char_p, c_float, c_int, c_uint, create_string_buffer

from toga_iOS.libs.opengles import opengles as GL

#: Shader version header: we want OpenGL ES GLSL 3
VERSION_HEADER = """#version 300 es"""


# Adapt some functions to common API


def v_func(v_size=1, ctype=c_int):
    """Decorator for functions expecting a pointer to an output vector.

    A number of OpenGL functions have a suffix of the form {l}{t}v,
    which expect an argument of an array of length l of type t (and
    an offset into it) which is used to return values by setting them
    into the array.

    This wrapper wraps these functions to create a ctypes array of the
    correct type, call the function, and then unpack the values from
    the array.
    """

    def wrapper(func):
        def call_v_function(*args):
            data = (ctype * v_size)(*([0] * v_size))
            func(*args, byref(data))
            if v_size == 1:
                return data[0]
            else:
                return tuple(data)

        return call_v_function

    return wrapper


glGetShaderiv = v_func()(GL.glGetShaderiv)
glGetProgramiv = v_func()(GL.glGetProgramiv)
glGenBuffers = v_func()(GL.glGenBuffers)
glGenVertexArrays = v_func()(GL.glGenVertexArrays)


def glShaderSource(id, source):
    source_bytes = c_char_p(source.encode("utf-8"))
    GL.glShaderSource(
        id,
        1,
        source_bytes,
        None,
    )


def glGetActiveUniform(id, loc):
    size = c_int()
    type = c_uint()
    name = create_string_buffer(255)
    GL.glGetActiveUniform(
        id,
        loc,
        255,
        None,
        byref(size),
        byref(type),
        name,
    )
    return name.value.decode("utf-8"), size.value, type.value


def glGetAttribLocation(id, item):
    buffer = create_string_buffer(item.encode("utf-8"))
    return GL.glGetAttribLocation(id, buffer)


def glGetuniformLocation(id, item):
    buffer = create_string_buffer(item.encode("utf-8"))
    return GL.glGetUniformLocation(id, buffer)


def glUniformMatrix4fv(loc, size, transpose, value):
    buffer = (c_float * (16 * size))(*value)
    GL.glUniformMatrix4fv(loc, size, transpose, buffer)


def glBufferData(buffer_type, data: bytes, usage):
    GL.glBufferData(buffer_type, len(data), data, usage)


def __getattr__(name):
    value = getattr(GL, name, None)
    if value is not None:
        globals()[name] = value
        return value
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
