##########################################################################
# System/Library/Frameworks/UIKit.framework
##########################################################################
from ctypes import cdll, util

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
