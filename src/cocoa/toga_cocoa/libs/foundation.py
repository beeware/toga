##########################################################################
# System/Library/Frameworks/Foundation.framework
##########################################################################
from ctypes import cdll, c_bool, util

from rubicon.objc import NSPoint, NSRect, ObjCClass

######################################################################
foundation = cdll.LoadLibrary(util.find_library('Foundation'))
######################################################################

foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]

######################################################################
# NSBundle.h
NSBundle = ObjCClass('NSBundle')
NSBundle.declare_class_property('mainBundle')
NSBundle.declare_property('bundlePath')

######################################################################
# NSFileWrapper.h
NSFileWrapper = ObjCClass('NSFileWrapper')

######################################################################
# NSNotification.h
NSNotificationCenter = ObjCClass('NSNotificationCenter')

######################################################################
NSNotification = ObjCClass('NSNotification')
NSNotification.declare_property('object')

######################################################################
# NSURL.h
NSURL = ObjCClass('NSURL')

######################################################################
# NSURLRequest.h
NSURLRequest = ObjCClass('NSURLRequest')

######################################################################
# NSValue.h
NSNumber = ObjCClass('NSNumber')
