##########################################################################
# System/Library/Frameworks/UIKit.framework
##########################################################################
from ctypes import c_char_p, c_float, c_int, c_ulong, cdll, util

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

# Functions
opengles.glGetString.argtypes = [c_int]
opengles.glGetString.restype = c_char_p

opengles.glClearColor.argtypes = [c_float, c_float, c_float, c_float]
opengles.glClear.restype = None
opengles.glClear.argtypes = [GLbitfield]
opengles.glClear.restype = None

opengles.glCreateShader.argtypes = [c_int]
opengles.glGetShaderInfoLog.argtypes = [c_int]
opengles.glGetShaderInfoLog.restype = c_char_p
