import array

from android.opengl import GLES32 as GL
from java import jarray, jint
from java.nio import ByteBuffer, ByteOrder

vertext_shader_source = """

layout(location = 0) in vec4 position;

void main()
{
   gl_Position = position;
}
"""
fragment_shader_source = """

out vec4 outputColor;
void main()
{
   outputColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""


def create_program(shader_list):
    program = GL.glCreateProgram()

    for shader in shader_list:
        GL.glAttachShader(program, shader)

    GL.glLinkProgram(program)

    # status = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
    # if status == GL.GL_FALSE:
    #     strInfoLog = GL.glGetProgramInfoLog(program)
    #     raise RuntimeError("Linker failure: \n" + strInfoLog)

    for shader in shader_list:
        GL.glDetachShader(program, shader)

    return program


def create_shader(shader_type, shader_code):
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, shader_code)

    GL.glCompileShader(shader)

    # status = None
    # GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS, status)
    # if status == GL.GL_FALSE:
    #     info_log = GL.glGetShaderInfoLog(shader)
    #     shader_types = {
    #         GL.GL_VERTEX_SHADER: "vertex",
    #         GL.GL_GEOMETRY_SHADER: "geometry",
    #         GL.GL_FRAGMENT_SHADER: "fragment",
    #     }
    #     raise RuntimeError(
    #         f"Compilation failure for {shader_types.get(shader_type, 'unknown')} "
    #         f"shader:\n{info_log}"
    #     )

    return shader


def initialize_program(vertex_shader_code, fragment_shader_code):
    shaderList = []

    shaderList.append(create_shader(GL.GL_VERTEX_SHADER, vertex_shader_code))
    shaderList.append(create_shader(GL.GL_FRAGMENT_SHADER, fragment_shader_code))

    program = create_program(shaderList)

    for shader in shaderList:
        GL.glDeleteShader(shader)

    return program


def initialize_vbo(vertex_positions):
    buffers = jarray(jint)([0])
    GL.glGenBuffers(1, buffers, 0)
    vbo = buffers[0]

    vertex_bytes = bytes(array.array("f", vertex_positions))
    nbytes = len(vertex_bytes)
    vertex_buffer = ByteBuffer.allocateDirect(nbytes)
    vertex_buffer.order(ByteOrder.nativeOrder())
    vertex_buffer.put(vertex_bytes)
    vertex_buffer.position(0)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, nbytes, vertex_buffer, GL.GL_STATIC_DRAW)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    return vbo


class Renderer:
    def on_init(self, widget, **kwargs):
        GL.glClearColor(1.0, 1.0, 0.0, 1.0)

        vertex_positions = [
            0.75,
            0.75,
            0.0,
            1.0,
            0.75,
            -0.75,
            0.0,
            1.0,
            -0.75,
            -0.75,
            0.0,
            1.0,
        ]

        self.program = initialize_program(vertext_shader_source, fragment_shader_source)
        self.vbo = initialize_vbo(vertex_positions)

        buffers = jarray(jint)([0])
        GL.glGenVertexArrays(1, buffers, 0)
        vao = buffers[0]

        GL.glBindVertexArray(vao)

    def on_render(self, widget, size, **kwargs):
        vertex_dim = 4
        n_vertices = 3

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(self.program)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, vertex_dim, GL.GL_FLOAT, False, 0, 0)

        GL.glDrawArrays(GL.GL_TRIANGLES, 0, n_vertices)

        GL.glDisableVertexAttribArray(0)
        GL.glUseProgram(0)
