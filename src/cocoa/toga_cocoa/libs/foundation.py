##########################################################################
# System/Library/Frameworks/Foundation.framework
##########################################################################
from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################
foundation = cdll.LoadLibrary(util.find_library('Foundation'))
######################################################################

foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]

######################################################################
# NSBundle.h
NSBundle = ObjCClass('NSBundle')
NSBundle.declare_class_property('mainBundle')

######################################################################
# NSFileWrapper.h
NSFileWrapper = ObjCClass('NSFileWrapper')

######################################################################
# NSNotification.h
NSNotificationCenter = ObjCClass('NSNotificationCenter')

######################################################################
# NSURL.h
NSURL = ObjCClass('NSURL')

######################################################################
# NSURLRequest.h
NSURLRequest = ObjCClass('NSURLRequest')

######################################################################
# NSValue.h
NSNumber = ObjCClass('NSNumber')
