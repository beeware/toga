# OpenGL

Test app for the [OpenGLView widget](https://toga.beeware.org/en/stable/reference/api/widgets/openglview.html).

The following OpenGLView features are present in this example:

- rendering simple Shadertoy OpenGL views using PyOpenGL

## Quickstart

You need PyOpenGL and numpy to run the example on desktop OS.

```text
$ python -m pip install toga PyOpenGL pyopengl-accelerate numpy
$ python -m shadertoy
```

Alternatively, you can use Pyglet

```text
$ python -m pip install toga pyglet
$ TOGA_OPENGL=pyglet python -m shadertoy
```
