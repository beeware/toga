"""Utility objects and methods for android.opengl"""

from android.opengl import GLES32 as GL
from java import jarray, jbyte, jint
from java.nio import ByteBuffer, ByteOrder

#: Shader version header: we want OpenGL ES GLSL 3
VERSION_HEADER = """#version 300 es"""

# Adapt some functions to common API


def v_func(v_size=1, jtype=jint):
    """Decorator for functions expecting a pointer to an output vector.

    A number of OpenGL functions have a suffix of the form {l}{t}v,
    which expect an argument of an array of length l of type t (and
    an offset into it) which is used to return values by setting them
    into the array.

    This wrapper wraps these functions to create a java array of the
    correct type, call the function, and then unpack the values from
    the array.
    """

    def wrapper(func):
        def call_v_function(*args):
            data = jarray(jtype)([0] * v_size)
            func(*args, data, 0)
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


def glVertexAttribPointer(loc, size, type, normalize, stride, offset):
    offset = 0 if offset is None else offset
    GL.glVertexAttribPointer(loc, size, type, bool(normalize), stride, offset)


def glGetActiveUniform(id, loc):
    length = jarray(jint)([0])
    size = jarray(jint)([0])
    type = jarray(jint)([0])
    name = jarray(jbyte)(b"\0x00" * 255)
    GL.glGetActiveUniform(
        id,
        loc,
        255,
        length,
        0,
        size,
        0,
        type,
        0,
        name,
        0,
    )
    return bytes(name[: length[0]]).decode("utf-8"), size[0], type[0]


def glBufferData(buffer_type, data, usage):
    nbytes = len(data)
    buffer = ByteBuffer.allocateDirect(nbytes)
    buffer.order(ByteOrder.nativeOrder())
    buffer.put(data)
    buffer.position(0)
    GL.glBufferData(buffer_type, nbytes, buffer, usage)


def __getattr__(name):
    value = getattr(GL, name, None)
    if value is not None:
        globals()[name] = value
        return value
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
