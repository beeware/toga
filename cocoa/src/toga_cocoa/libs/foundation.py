##########################################################################
# System/Library/Frameworks/Foundation.framework
##########################################################################
from ctypes import c_bool

from rubicon.objc import NSPoint, NSRect, ObjCClass
from rubicon.objc.runtime import load_library

######################################################################
foundation = load_library("Foundation")
######################################################################

foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]

######################################################################
# NSBundle.h
NSBundle = ObjCClass("NSBundle")
NSBundle.declare_class_property("mainBundle")
NSBundle.declare_property("bundlePath")

######################################################################
# NSData.h
NSData = ObjCClass("NSData")

######################################################################
# NSFileWrapper.h
NSFileWrapper = ObjCClass("NSFileWrapper")

######################################################################
# NSNotification.h
NSNotificationCenter = ObjCClass("NSNotificationCenter")

######################################################################
NSNotification = ObjCClass("NSNotification")
NSNotification.declare_property("object")

######################################################################
# NSRunLoop.h
NSRunLoop = ObjCClass("NSRunLoop")
NSRunLoop.declare_class_property("currentRunLoop")

######################################################################
# NSURL.h
NSURL = ObjCClass("NSURL")

######################################################################
# NSURLRequest.h
NSURLRequest = ObjCClass("NSURLRequest")

######################################################################
# NSValue.h
NSNumber = ObjCClass("NSNumber")
