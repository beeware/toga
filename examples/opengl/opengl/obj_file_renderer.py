"""
Generic Shadertoy Renderer
==========================

This renderer allows the use of basic Shadertoy-style fragment
rendering. It provides a single image shader, pointer state and time
data, but doesn't provide additional shaders, textures, channels,
video or sound support.

Differences between OpenGL APIs are handled in the appropriate
utils object: which one is selected depends on the toga backend.
The utils provide abstractions for Shaders, Programs, Buffers and
Vertex Array Objects which make the code in the renderer cleaner
and hide the OpenGL code somewhat.
"""

import array
import time
import traceback
from math import pi

from .matrix import Matrix
from .obj_file import bbox
from .utils import (
    GL,
    VERSION_HEADER,
    Buffer,
    BufferType,
    BufferUsage,
    OpenGLError,
    Program,
    Shader,
    ShaderType,
    VertexArrayObject,
)

#: Vertex shader: displays triangles in 2D.
VERTEX_SHADER_SOURCE = (
    VERSION_HEADER
    + """

precision highp float;

in vec4 position;
in vec3 normal;
in vec3 color;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 world;
uniform mat4 world_normal;
uniform vec3 view_position;

out vec3 vertex_normal;
out vec3 vertex_color;
out vec3 surface_to_view;

void main() {
    vec4 world_position = world * position;
    gl_Position = projection * view * world_position;
    surface_to_view = view_position - world_position.xyz;
    vertex_normal = mat3(world) * normal;
    vertex_color = color;
}
"""
)

#: Fragment shader: calls mainImage to set pixel colors.
FRAGMENT_SHADER_SOURCE = (
    VERSION_HEADER
    + """

precision highp float;

in vec3 vertex_normal;
in vec3 vertex_color;
in vec3 surface_to_view;

uniform vec3 light_direction;
uniform vec3 ambient_light;

uniform vec3 diffuse;
uniform vec3 ambient;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;

out vec4 output_color;

void main() {
    vec3 normal = normalize(vertex_normal);
    float light = dot(normal, light_direction) * 0.5 + 0.5;

    output_color = vec4(
        emissive
        + ambient * ambient_light
        + diffuse * light,
        opacity
    );

    if (shininess > 0) {
        vec3 surface_to_view_direction = normalize(surface_to_view);
        vec3 half_vector = normalize(light_direction + surface_to_view_direction);
        float specular_light = clamp(dot(normal, half_vector), 0.0, 1.0);

        output_color.rgb += specular * pow(specular_light, shininess);
    }
    //output_color = vec4(vec3(gl_FragCoord.z), 1.0);
}
"""
)

#: Message to display in side-panel giving info about
#: values of uniforms.
UNIFORM_VALUES = """Frame: {iFrame[0]}
Frame rate: {iFrameRate[0]:.3f} fps

Resolution: {iResolution}
Mouse: ({iMouse[0]:.1f}, {iMouse[1]:.1f}) ({iMouse[2]:.1f}, {iMouse[3]:.1f})

Time: {iTime[0]:.3f} s
Time delta: {iTimeDelta[0]:.3f} s
Date: {iDate[0]}-{iDate[1]}-{iDate[2]} {iDate[3]:.3f}
"""


class ObjFileRenderer:
    """Renderer for Shadertoy fragment renderers.

    This renderer expects to be provided with GLSL code that implements the
    mainImage function in the fragment shader. This code is provided via the
    `source` property.  The message attribute is set to information about the
    state of the renderer, either:
    - the data provided to the uniforms; or
    - status/error messages
    """

    #: A message containing information about the renderer's state.
    message: str

    #: The source for the mainImage function.
    _data: list

    data_updated = False

    def __init__(self, data=()):
        self.message = "Uninitialized."
        self.data = data
        self.radius = 1.0
        self.center = (0.0, 0.0, 0.0)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        """Set a new value for the data."""
        self._data = data
        self.data_updated = True

    def on_init(self, widget, **kwargs):
        """Initialize the OpenGL state."""
        self.message = "Initializing...\n\n"
        try:
            if not self.data:
                return
            GL.glEnable(GL.GL_CULL_FACE)
            GL.glEnable(GL.GL_DEPTH_TEST)
            self._initialize_program(VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE)

            self.buffers = []
            bboxes = []
            for geometry in self.data:
                bboxes.extend(bbox(geometry.vertices))
                buffers = {}
                buffers["position"] = self._initialize_buffer(geometry.vertices)
                buffers["normal"] = self._initialize_buffer(geometry.normals)
                buffers["color"] = self._initialize_buffer(geometry.colors)
                self.buffers.append(buffers)
            self.bbox = bbox(bboxes)
            self.center = tuple((self.bbox[i] + self.bbox[i + 3]) / 2 for i in range(3))
            self.radius = sum(
                abs(v - c) for v, c in zip(self.bbox[3:], self.center, strict=True)
            )

            self.vaos = []
            for buffers in self.buffers:
                self.vaos.append(self._initialize_attributes(buffers))
        except OpenGLError as exc:
            # Add OpenGL error to messages
            # This is most likely an error in the source, so this is important
            # user feedback.
            self.message += exc.args[0]
            raise
        except Exception:
            # Add other errors to messages
            # This is most likely caused by a bug in the renderer.
            self.message += traceback.format_exc()
            raise
        else:
            # Indicate success.
            self.data_updated = False
            self.message += "Initialization successful"
        print(self.message)

    def on_render(
        self,
        widget,
        size,
        pointer=(-1, -1),
        buttons=frozenset(),
        **kwargs,
    ):
        """Render a frame using OpenGL."""
        if self.data_updated or not hasattr(self, "program"):
            self.on_init(widget)

        self.message = "Rendering...\n\n"
        GL.glClearColor(0.0, 0.0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        if not hasattr(self, "program"):
            # something seriously wrong, don't try to render
            return

        t = time.time()
        aspect = size[0] / size[1]

        try:
            # Set the uniform values into a dictionary to be applied later
            uniforms = {
                "projection": Matrix.perspective(
                    pi / 6, aspect, self.radius / 100, self.radius * 50
                ),
                "view": Matrix.translation(0, 0, -3 * self.radius),
                "view_position": (0, 0, -3 * self.radius),
                "world": Matrix.rotation_y(t)
                @ Matrix.translation(-self.center[0], -self.center[1], -self.center[2]),
                "world_normals": Matrix.rotation_y(-t).transpose(),
                "light_direction": (3 / 5, 0, 3 / 5),
                "ambient_light": (0.0, 0.0, 0.0),
            }

            # draw!
            with self.program.use():
                self.program.set_uniforms(uniforms)
                for obj, vao in zip(self.data, self.vaos, strict=True):
                    n_vertices = len(obj.vertices) // 3
                    if hasattr(obj, "material"):
                        material = {
                            "diffuse": obj.material.diffuse,
                            "ambient": obj.material.ambient,
                            "emissive": obj.material.emissive,
                            "specular": obj.material.specular,
                            "opacity": obj.material.opacity,
                            "shininess": obj.material.shininess,
                        }
                    else:
                        material = {
                            "diffuse": (1.0, 1.0, 1.0),
                            "ambient": (0.0, 0.0, 0.0),
                            "emissive": (0.0, 0.0, 0.0),
                            "specular": (0.0, 0.0, 0.0),
                            "opacity": (1.0,),
                        }
                    self.program.set_uniforms(material)
                    with vao:
                        GL.glDrawArrays(GL.GL_TRIANGLES, 0, n_vertices)

            # Update frame and time delta information
            # self.frame += 1
            # if len(self.deltas) > 100:
            #     del self.deltas[0]
        except Exception:
            # Display error messages
            self.message += traceback.format_exc()
            raise

    def _initialize_buffer(self, data):
        """Set some buffer data.

        This is never updated, so we call once during init.
        """
        data_bytes = bytes(array.array("f", data))
        buffer_object = Buffer(BufferType.array, BufferUsage.static_draw)
        buffer_object.create(data_bytes)
        return buffer_object

    def _initialize_program(self, vertex_shader_code, fragment_shader_code):
        """Initialize the shader program.

        This:
        - creates the shaders and the program
        - compiles the shaders
        - links the program
        - checks for errors
        - deletes the compiled shaders

        This needs to be called every time the source changes.
        """
        self.program = Program(
            [
                Shader(ShaderType.vertex, vertex_shader_code),
                Shader(ShaderType.fragment, fragment_shader_code),
            ]
        )
        self.program.create()

    def _initialize_attributes(self, attributes):
        """Initialize the vertex attribute object.

        This creates a vertex attribute object for the specified attribute,
        and then binds the vertex buffer object to that attribute.

        This needs to be called every time the program changes.
        """
        attribute_object = VertexArrayObject()
        attribute_object.create()
        with attribute_object:
            for attribute, buffer in attributes.items():
                self.program.bind_attribute_buffer(attribute, buffer, size=3)
        return attribute_object
