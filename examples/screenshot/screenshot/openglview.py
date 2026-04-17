import array

import toga

if toga.backend in {"toga_cocoa", "toga_gtk", "toga_qt"}:
    import OpenGL

    OpenGL.ERROR_CHECKING = False

    from OpenGL.GL import (
        GL_ARRAY_BUFFER,
        GL_COLOR_BUFFER_BIT,
        GL_COMPILE_STATUS,
        GL_DEPTH_BUFFER_BIT,
        GL_DEPTH_TEST,
        GL_FALSE,
        GL_FLOAT,
        GL_FRAGMENT_SHADER,
        GL_LINK_STATUS,
        GL_STATIC_DRAW,
        GL_TRIANGLES,
        GL_VERTEX_SHADER,
        glAttachShader,
        glBindBuffer,
        glBindVertexArray,
        glBufferData,
        glClear,
        glClearColor,
        glCompileShader,
        glCreateProgram,
        glCreateShader,
        glDeleteShader,
        glDetachShader,
        glDrawArrays,
        glEnable,
        glEnableVertexAttribArray,
        glGenBuffers,
        glGenVertexArrays,
        glGetAttribLocation,
        glGetProgramInfoLog,
        glGetProgramiv,
        glGetShaderInfoLog,
        glGetShaderiv,
        glGetUniformLocation,
        glLinkProgram,
        glShaderSource,
        glUniformMatrix4fv,
        glUseProgram,
        glVertexAttribPointer,
        glViewport,
    )  # noqa: E402

    SHADER_HEADER = "#version 330 core"

elif toga.backend in {"toga_android"}:
    from android.opengl import GLES32 as GL
    from java import jarray, jfloat, jint
    from java.nio import ByteBuffer, ByteOrder

    GL_ARRAY_BUFFER = GL.GL_ARRAY_BUFFER
    GL_COLOR_BUFFER_BIT = GL.GL_COLOR_BUFFER_BIT
    GL_COMPILE_STATUS = GL.GL_COMPILE_STATUS
    GL_DEPTH_BUFFER_BIT = GL.GL_DEPTH_BUFFER_BIT
    GL_DEPTH_TEST = GL.GL_DEPTH_TEST
    GL_FALSE = GL.GL_FALSE
    GL_FLOAT = GL.GL_FLOAT
    GL_FRAGMENT_SHADER = GL.GL_FRAGMENT_SHADER
    GL_LINK_STATUS = GL.GL_LINK_STATUS
    GL_STATIC_DRAW = GL.GL_STATIC_DRAW
    GL_TRIANGLES = GL.GL_TRIANGLES
    GL_VERTEX_SHADER = GL.GL_VERTEX_SHADER
    glAttachShader = GL.glAttachShader
    glBindBuffer = GL.glBindBuffer
    glBindVertexArray = GL.glBindVertexArray
    glClear = GL.glClear
    glClearColor = GL.glClearColor
    glCompileShader = GL.glCompileShader
    glCreateProgram = GL.glCreateProgram
    glCreateShader = GL.glCreateShader
    glDeleteShader = GL.glDeleteShader
    glDetachShader = GL.glDetachShader
    glDrawArrays = GL.glDrawArrays
    glEnable = GL.glEnable
    glEnableVertexAttribArray = GL.glEnableVertexAttribArray
    glGetAttribLocation = GL.glGetAttribLocation
    glGetProgramInfoLog = GL.glGetProgramInfoLog
    glGetShaderInfoLog = GL.glGetShaderInfoLog
    glGetUniformLocation = GL.glGetUniformLocation
    glLinkProgram = GL.glLinkProgram
    glShaderSource = GL.glShaderSource
    glUseProgram = GL.glUseProgram
    glViewport = GL.glViewport

    def glGetShaderiv(id, param):
        data = jarray(jint)([0])
        GL.glGetShaderiv(id, param, data, 0)
        return data[0]

    def glGetProgramiv(id, param):
        data = jarray(jint)([0])
        GL.glGetProgramiv(id, param, data, 0)
        return data[0]

    def glGenBuffers(count):
        data = jarray(jint)([0] * count)
        GL.glGenBuffers(count, data, 0)
        if count == 1:
            return data[0]
        else:
            return tuple(data)

    def glGenVertexArrays(count):
        data = jarray(jint)([0] * count)
        GL.glGenVertexArrays(count, data, 0)
        if count == 1:
            return data[0]
        else:
            return tuple(data)

    def glUniformMatrix4fv(loc, size, transpose, value):
        buffer = jarray(jfloat)(list(value))
        GL.glUniformMatrix4fv(loc, size, bool(transpose), buffer, 0)

    def glVertexAttribPointer(loc, size, type, normalize, stride, offset):
        offset = 0 if offset is None else offset
        GL.glVertexAttribPointer(loc, size, type, bool(normalize), stride, offset)

    def glBufferData(buffer_type, data, usage):
        nbytes = len(data)
        buffer = ByteBuffer.allocateDirect(nbytes)
        buffer.order(ByteOrder.nativeOrder())
        buffer.put(data)
        buffer.position(0)
        GL.glBufferData(buffer_type, nbytes, buffer, usage)

    SHADER_HEADER = "#version 300 es"

elif toga.backend in {"toga_iOS"}:
    from ctypes import (
        byref,
        c_char_p,
        c_float,
        c_float_p,
        c_int,
        cast,
        create_string_buffer,
    )

    from toga_iOS.libs.opengles import opengles as GL

    GL_ARRAY_BUFFER = GL.GL_ARRAY_BUFFER
    GL_COLOR_BUFFER_BIT = GL.GL_COLOR_BUFFER_BIT
    GL_COMPILE_STATUS = GL.GL_COMPILE_STATUS
    GL_DEPTH_BUFFER_BIT = GL.GL_DEPTH_BUFFER_BIT
    GL_DEPTH_TEST = GL.GL_DEPTH_TEST
    GL_FALSE = GL.GL_FALSE
    GL_FLOAT = GL.GL_FLOAT
    GL_FRAGMENT_SHADER = GL.GL_FRAGMENT_SHADER
    GL_LINK_STATUS = GL.GL_LINK_STATUS
    GL_STATIC_DRAW = GL.GL_STATIC_DRAW
    GL_TRIANGLES = GL.GL_TRIANGLES
    GL_VERTEX_SHADER = GL.GL_VERTEX_SHADER
    glAttachShader = GL.glAttachShader
    glBindBuffer = GL.glBindBuffer
    glBindVertexArray = GL.glBindVertexArray
    glClear = GL.glClear
    glClearColor = GL.glClearColor
    glCompileShader = GL.glCompileShader
    glCreateProgram = GL.glCreateProgram
    glCreateShader = GL.glCreateShader
    glDeleteShader = GL.glDeleteShader
    glDetachShader = GL.glDetachShader
    glDrawArrays = GL.glDrawArrays
    glEnable = GL.glEnable
    glEnableVertexAttribArray = GL.glEnableVertexAttribArray
    glGetProgramInfoLog = GL.glGetProgramInfoLog
    glGetShaderInfoLog = GL.glGetShaderInfoLog
    glLinkProgram = GL.glLinkProgram
    glUseProgram = GL.glUseProgram
    glViewport = GL.glViewport

    def glGetShaderiv(id, param):
        data = c_int(0)
        GL.glGetShaderiv(id, param, byref(data))
        return data.value

    def glGetProgramiv(id, param):
        data = c_int(0)
        GL.glGetProgramiv(id, param, byref(data), 0)
        return data.value

    def glGenBuffers(count):
        data = (c_int * count)(*([0] * count))
        GL.glGenBuffers(count, byref(data))
        if count == 1:
            return data[0]
        else:
            return tuple(data)

    def glGenVertexArrays(count):
        data = (c_int * count)(*([0] * count))
        GL.glGenVertexArrays(count, byref(data))
        if count == 1:
            return data[0]
        else:
            return tuple(data)

    def glShaderSource(id, source):
        source_bytes = c_char_p(source.encode("utf-8"))
        GL.glShaderSource(
            id,
            1,
            source_bytes,
            None,
        )

    def glGetAttribLocation(id, item):
        buffer = create_string_buffer(item.encode("utf-8"))
        return GL.glGetAttribLocation(id, buffer)

    def glGetUniformLocation(id, item):
        buffer = create_string_buffer(item.encode("utf-8"))
        return GL.glGetUniformLocation(id, buffer)

    def glUniformMatrix4fv(loc, size, transpose, value):
        buffer = (c_float * (16 * size))(*value)
        GL.glUniformMatrix4fv(loc, size, transpose, cast(buffer, c_float_p))

    def glBufferData(buffer_type, data: bytes, usage):
        GL.glBufferData(buffer_type, len(data), data, usage)

    def glVertexAttribPointer(loc, size, type, normalize, stride, offset):
        offset = 0 if offset is None else offset
        GL.glVertexAttribPointer(loc, size, type, bool(normalize), stride, offset)

    SHADER_HEADER = "#version 300 es"

else:
    raise NotImplementedError()


VERTEX_SHADER = (
    SHADER_HEADER
    + """

precision highp float;

in vec4 position;
in vec3 normal;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 world;

out vec3 vertex_normal;

void main() {
    gl_Position = projection * view * world * position;
    vertex_normal = mat3(world) * normal;
}
"""
)
FRAGMENT_SHADER = (
    SHADER_HEADER
    + """

precision highp float;

in vec3 vertex_normal;

vec3 light_direction = vec3(-1.0, 3.0, 5.0);
vec3 diffuse = vec3(1.0, 1.0, 1.0);

out vec4 output_color;

void main() {
    float light = dot(
        normalize(vertex_normal),
        normalize(light_direction)
    ) * 0.5 + 0.5;

    output_color = vec4(light * diffuse, 1.0);
}
"""
)


# fmt: off
VERTICES = [
    -0.5, -0.5,  -0.5,
    -0.5,  0.5,  -0.5,
     0.5, -0.5,  -0.5,
    -0.5,  0.5,  -0.5,
     0.5,  0.5,  -0.5,
     0.5, -0.5,  -0.5,

    -0.5, -0.5,   0.5,
     0.5, -0.5,   0.5,
    -0.5,  0.5,   0.5,
    -0.5,  0.5,   0.5,
     0.5, -0.5,   0.5,
     0.5,  0.5,   0.5,

    -0.5,   0.5, -0.5,
    -0.5,   0.5,  0.5,
     0.5,   0.5, -0.5,
    -0.5,   0.5,  0.5,
     0.5,   0.5,  0.5,
     0.5,   0.5, -0.5,

    -0.5,  -0.5, -0.5,
     0.5,  -0.5, -0.5,
    -0.5,  -0.5,  0.5,
    -0.5,  -0.5,  0.5,
     0.5,  -0.5, -0.5,
     0.5,  -0.5,  0.5,

    -0.5,  -0.5, -0.5,
    -0.5,  -0.5,  0.5,
    -0.5,   0.5, -0.5,
    -0.5,  -0.5,  0.5,
    -0.5,   0.5,  0.5,
    -0.5,   0.5, -0.5,

     0.5,  -0.5, -0.5,
     0.5,   0.5, -0.5,
     0.5,  -0.5,  0.5,
     0.5,  -0.5,  0.5,
     0.5,   0.5, -0.5,
     0.5,   0.5,  0.5,
]

NORMALS = (
    [0.0, 0.0, -1.0] * 6
    + [0.0, 0.0, 1.0] * 6
    + [0.0, 1.0, 0.0] * 6
    + [0.0, -1.0, 0.0] * 6
    + [-1.0, 0.0, 0.0] * 6
    + [1.0,  0.0,  0.0] * 6
)
# fmt: on


class CubeRenderer:
    def on_init(self, widget, **kwargs):
        glEnable(GL_DEPTH_TEST)
        self.init_buffers()
        self.init_program()
        self.init_vertex_array()

    def on_render(self, widget, size, **kwargs):
        aspect = size[0] / size[1]
        glViewport(0, 0, int(size[0]), int(size[1]))
        glClearColor(0.5, 0.5, 1.0, 1.0)
        glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))

        if not hasattr(self, "program"):
            # Didn't initialize correctly.
            print("Failed!")
            return

        glUseProgram(self.program)
        glBindVertexArray(self.vao)
        # set uniforms
        loc = glGetUniformLocation(self.program, "projection")
        # fmt: off
        glUniformMatrix4fv(
            loc,
            1,
            GL_FALSE,
            [
                1.73 / aspect, 0.00,  0.00,  0.00,
                0.00,          1.73,  0.00,  0.00,
                0.00,          0.00, -1.00, -1.00,
                0.00,          0.00, -0.01,  0.00,
            ],
        )
        # fmt: on
        loc = glGetUniformLocation(self.program, "view")
        # fmt: off
        glUniformMatrix4fv(
            loc,
            1,
            GL_FALSE,
            [
                 1.00,  0.00,  0.00,  0.00,
                 0.00,  1.00,  0.00,  0.00,
                 0.00,  0.00,  1.00,  0.00,
                 0.00,  0.00, -2.00,  1.00,
            ],
        )
        # fmt: on
        loc = glGetUniformLocation(self.program, "world")
        # fmt: off
        glUniformMatrix4fv(
            loc,
            1,
            GL_FALSE,
            [
                 0.50,  0.61,  0.61,  0.00,
                 0.00,  0.71, -0.71,  0.00,
                -0.87,  0.35,  0.35,  0.00,
                 0.00,  0.00,  0.00,  1.00,
            ],
        )
        # fmt: on

        # draw!
        glDrawArrays(GL_TRIANGLES, 0, self.n_vertices)
        print("Drawing done!")

    def init_buffers(self):
        # Initialize buffers
        self.n_vertices = len(VERTICES) // 3
        vertex_data = bytes(array.array("f", VERTICES))
        self.vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertex_data, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        normal_data = bytes(array.array("f", NORMALS))
        self.normal_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glBufferData(GL_ARRAY_BUFFER, normal_data, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def init_program(self):
        # Initialize shaders
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, VERTEX_SHADER)
        glCompileShader(vertex_shader)
        status = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if status == GL_FALSE:
            info_log = glGetShaderInfoLog(vertex_shader)
            raise RuntimeError(f"Compilation failure shader:\n{info_log}")

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, FRAGMENT_SHADER)
        glCompileShader(fragment_shader)
        status = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
        if status == GL_FALSE:
            info_log = glGetShaderInfoLog(fragment_shader)
            raise RuntimeError(f"Compilation failure for shader:\n{info_log}")

        # Initialize program
        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        status = glGetProgramiv(self.program, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(self.program)
            raise RuntimeError(f"Linker failure: \n{strInfoLog}")

        # Clean up shaders
        glDetachShader(self.program, vertex_shader)
        glDetachShader(self.program, fragment_shader)
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def init_vertex_array(self):
        self.vao = glGenVertexArrays(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        loc = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        loc = glGetAttribLocation(self.program, "normal")
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
