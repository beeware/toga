##########################################################################
# System/Library/Frameworks/UIKit.framework
##########################################################################
from ctypes import cdll, util

from rubicon.objc import ObjCClass

######################################################################
glkit = cdll.LoadLibrary(util.find_library("GLKit"))
######################################################################

######################################################################
# GLKView.h
GLKView = ObjCClass("GLKView")

GLKViewDrawableColorFormatRGBA8888 = 0
GLKViewDrawableDepthFormat24 = 2
GLKViewDrawableStencilFormat8 = 1
GLKViewDrawableMultisample4X = 1

EAGLContext = ObjCClass("EAGLContext")

kEAGLRenderingAPIOpenGLES1 = 1
kEAGLRenderingAPIOpenGLES2 = 2
kEAGLRenderingAPIOpenGLES3 = 3
