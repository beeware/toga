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
import datetime
import time
import traceback

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
VERTEX_SHADER_SOURCE = f"""{VERSION_HEADER}

precision highp float;

in vec4 position;

void main() {{
   gl_Position = position;
}}
"""

#: Fragment shader: calls mainImage to set pixel colors.
FRAGMENT_SHADER_TEMPLATE = """{header}

precision highp float;

uniform vec3 iResolution;
uniform float iTime;
uniform float iTimeDelta;
uniform float iFrame;
uniform float iFrameRate;
uniform vec4 iMouse;
uniform vec4 iDate;

out vec4 output_color;

{source}

void main() {{
  mainImage(output_color, gl_FragCoord.xy);
}}
"""

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

#: Vertex coordinates for a square filling the viewport.
# fmt: off
VERTEX_POSITIONS = [
     1.0,  1.0,  # triangle 1: bottom right
     1.0, -1.0,
    -1.0, -1.0,
     1.0,  1.0,  # triangle 2: top left
    -1.0, -1.0,
    -1.0,  1.0,
]
# fmt: on

#: Number of vertices
N_VERTICES = len(VERTEX_POSITIONS) // 2


class ShadertoyRenderer:
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

    #: Whether or not the source has changed and needs to be updated
    # on the next render.
    source_updated: bool = False

    #: The start time of the shader run in seconds since the epoch.
    start: float

    #: The time stamp of the last frame.
    timestamp: float

    #: The frame count.
    frame: int

    #: A list of the last 100 time deltas.
    deltas: list[float]

    #: The position of the pointer, or None if not available.
    pointer: tuple[int, int]

    #: Whether the mouse button (or user touch) is down or up.
    mouse_down: bool

    #: The starting location of most recent drag operation.
    drag_start: tuple[int, int]

    #: The source for the mainImage function.
    _source: str

    def __init__(self, source):
        self.message = "Uninitialized."
        self.source = source

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, source):
        """Set a new value for the source.

        This is merged into the fragment shader template and then the
        source is marked for updating on the next render.
        """
        self._source = source
        self.fragment_shader_source = FRAGMENT_SHADER_TEMPLATE.format(
            source=source,
            header=VERSION_HEADER,
        )
        self.source_updated = True

    def on_init(self, widget, **kwargs):
        """Initialize the OpenGL state."""
        self.message = "Initializing...\n\n"
        try:
            self._initialize_vbo(VERTEX_POSITIONS)
            self._update_program()
            self.source_updated = False
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
            self.message += "Initialization successful"

    def on_render(
        self,
        widget,
        size,
        pointer=(-1, -1),
        buttons=frozenset(),
        **kwargs,
    ):
        """Render a frame using OpenGL."""
        self.message = "Rendering...\n\n"
        GL.glClearColor(0.0, 0.0, 1.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Handle a pending source update.
        if self.source_updated:
            try:
                if hasattr(self, "program"):
                    self.program.delete()
                self._update_program()
            except OpenGLError as exc:
                # Add OpenGL error to messages
                # This is most likely an error in the source, so this is important
                # user feedback.
                self.message = exc.args[0]
                raise
            except Exception:
                # Add other errors to messages
                # This is most likely caused by a bug in the renderer.
                self.message = traceback.format_exc()
                raise
            else:
                # Indicate success.
                self.source_updated = False
                self.message += "Update successful\n\n"

        try:
            # Update the state for the uniforms
            self._set_pointer(size, pointer, buttons)
            t = time.time() - self.start
            self.deltas.append(t - self.timestamp + 1e-6)
            if sum(self.deltas) == 0:
                frame_rate = 0.0
            else:
                frame_rate = len(self.deltas) / sum(self.deltas)
            self.timestamp = t
            dt = datetime.datetime.now()

            # Set the uniform values into a dictionary to be applied later
            uniforms = {
                "iResolution": (*size, 1.0),
                "iMouse": (*self.pointer, *self.drag_start),
                "iTime": (self.timestamp,),
                "iTimeDelta": (self.deltas[-1],),
                "iFrame": (self.frame,),
                "iFrameRate": (frame_rate,),
                "iDate": (
                    dt.year,
                    dt.month,
                    dt.day,
                    dt.hour * 3600
                    + dt.minute * 60
                    + dt.second
                    + (dt.microsecond / 1e6),
                ),
            }

            # draw!
            with self.program.use():
                self.program.set_uniforms(uniforms)
                with self.vao:
                    GL.glDrawArrays(GL.GL_TRIANGLES, 0, N_VERTICES)

            # Update frame and time delta information
            self.frame += 1
            if len(self.deltas) > 100:
                del self.deltas[0]
        except Exception:
            # Display error messages
            self.message += traceback.format_exc()
            raise
        else:
            # Display uniform values in message.
            self.message += UNIFORM_VALUES.format(**uniforms)

    def _initialize_vbo(self, data):
        """Set the vertex buffer data.

        This is never updated, so we call once during init.
        """
        data_bytes = bytes(array.array("f", data))
        self.vbo = Buffer(BufferType.array, BufferUsage.static_draw)
        self.vbo.create(data_bytes)

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

    def _initialize_vao(self, attribute):
        """Initialize the vertex attribute object.

        This creates a vertex attribute object for the specified attribute,
        and then binds the vertex buffer object to that attribute.

        This needs to be called every time the program changes.
        """
        self.vao = VertexArrayObject()
        self.vao.create()
        with self.vao:
            self.program.bind_attribute_buffer(attribute, self.vbo, size=2)

    def _update_program(self):
        """Update the program and related data when the source changes.

        This:
        - initializes the program
        - initializes the vertex attribute object
        - resets the state used for the uniforms
        """
        self._initialize_program(VERTEX_SHADER_SOURCE, self.fragment_shader_source)
        self._initialize_vao("position")

        # Reset the state variables for the uniforms.
        self.start = time.time()
        self.timestamp = 0
        self.frame = 0
        self.deltas = []
        self.pointer = (0, 0)
        self.mouse_down = False
        self.drag_start = (0, 0)

    def _set_pointer(self, size, pointer, buttons):
        """Set the values for the pointer data.

        Shadertoy follows the following conventions:
        - if no buttons are pressed (or a touch/drag is not underway) the position
          does not update
        - if the button/touch has *just* started, drag start coordinates are positive
        - if the drag is continuing, the drag start y coordinate is negative
        - if the drag has ended, the drag start x coordinate is also set negative

        We also have to handle the case where no pointer information is available.
        This happens most often in mobile before the user has interacted with the
        OpenGLView widget. In this case we set everything to 0.
        """
        if (
            pointer is not None
            and 0 <= pointer[0] < size[0]
            and 0 <= pointer[1] < size[1]
        ):
            if buttons:
                self.pointer = pointer
                if not self.mouse_down:
                    # new mouse down
                    self.drag_start = pointer
                    self.mouse_down = True
                elif self.drag_start[1] > 0:
                    # mouse was newly down, still down
                    self.drag_start = (self.drag_start[0], -self.drag_start[1])
            elif self.mouse_down:
                # new mouse up
                self.drag_start = (-self.drag_start[0], self.drag_start[1])
                self.mouse_down = False
        elif pointer is None:
            self.pointer = (0, 0)
            self.drag_start = (0, 0)
            self.mouse_down = False
