##########################################################################
# System/Library/Frameworks/UIKit.framework
##########################################################################
from ctypes import POINTER, c_char_p, c_float, c_int, c_uint, c_ulong, cdll, util

from rubicon.objc import ObjCClass

######################################################################
opengles = cdll.LoadLibrary(util.find_library("OpenGLES"))
######################################################################

######################################################################
# EAGL.h
EAGLContext = ObjCClass("EAGLContext")

kEAGLRenderingAPIOpenGLES1 = 1
kEAGLRenderingAPIOpenGLES2 = 2
kEAGLRenderingAPIOpenGLES3 = 3

# Types
GLbitfield = c_ulong
GLint = c_int
GLuint = c_uint
GLsizei = c_ulong
GLfloat = c_float

# Functions
opengles.glGetString.argtypes = [c_int]
opengles.glGetString.restype = c_char_p

opengles.glClearColor.argtypes = [c_float, c_float, c_float, c_float]
opengles.glClear.restype = None
opengles.glClear.argtypes = [GLbitfield]
opengles.glClear.restype = None

opengles.glCreateShader.argtypes = [GLuint]
opengles.glShaderSource.argtypes = [GLuint, GLsizei, POINTER(c_char_p), POINTER(c_int)]
opengles.glCompileShader.argtypes = [GLuint]
opengles.glGetShaderInfoLog.argtypes = [GLuint]
opengles.glGetShaderInfoLog.restype = c_char_p

opengles.glUniform1f.argtypes = [GLint, GLfloat]
opengles.glUniform2f.argtypes = [GLint, GLfloat, GLfloat]
opengles.glUniform3f.argtypes = [GLint, GLfloat, GLfloat, GLfloat]
opengles.glUniform4f.argtypes = [GLint, GLfloat, GLfloat, GLfloat, GLfloat]

opengles.glUniform1fv.argtypes = [GLint, GLsizei, POINTER(GLfloat)]
opengles.glUniform2fv.argtypes = [GLint, GLsizei, POINTER(GLfloat)]
opengles.glUniform3fv.argtypes = [GLint, GLsizei, POINTER(GLfloat)]
opengles.glUniform4fv.argtypes = [GLint, GLsizei, POINTER(GLfloat)]

# Constants
opengles.GL_FALSE = False

opengles.GL_DEPTH_BUFFER_BIT = 0x200
opengles.GL_COLOR_BUFFER_BIT = 0x4000
opengles.GL_STENCIL_BUFFER_BIT = 0x400

opengles.GL_VENDOR = 0x1F00
opengles.GL_RENDERER = 0x1F01
opengles.GL_VERSION = 0x1F02
opengles.GL_SHADING_LANGUAGE_VERSION = 0x8B8C

opengles.GL_FRAGMENT_SHADER = 0x8B30
opengles.GL_VERTEX_SHADER = 0x8B31

opengles.GL_ARRAY_BUFFER = 0x8892

opengles.GL_DYNAMIC_DRAW = 0x88E8
opengles.GL_STATIC_DRAW = 0x88E4

opengles.GL_FLOAT = 0x1406
opengles.GL_FLOAT_VEC2 = 0x8B50
opengles.GL_FLOAT_VEC3 = 0x8B51
opengles.GL_FLOAT_VEC4 = 0x8B52

opengles.GL_COMPILE_STATUS = 0x8B81

opengles.GL_LINK_STATUS = 0x8B82
opengles.GL_ACTIVE_UNIFORMS = 0x8B86
opengles.GL_ACTIVE_ATTRIBUTES = 0x8B89

opengles.GL_TRIANGLES = 0x4
