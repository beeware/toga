##########################################################################
# System/Library/Frameworks/Foundation.framework
##########################################################################
from ctypes import c_bool, cdll, util

from rubicon.objc import NSPoint, NSRect, ObjCClass

######################################################################
foundation = cdll.LoadLibrary(util.find_library('Foundation'))
######################################################################

foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]


######################################################################
# NSArray.h
NSMutableArray = ObjCClass('NSMutableArray')


######################################################################
# NSBundle.h
NSBundle = ObjCClass('NSBundle')


######################################################################
# NSData.h
NSData = ObjCClass('NSData')


######################################################################
# NSDate.h
NSDate = ObjCClass('NSDate')


######################################################################
# NSIndexPath.h
NSIndexPath = ObjCClass('NSIndexPath')


######################################################################
# NSNotification.h
NSNotificationCenter = ObjCClass('NSNotificationCenter')


######################################################################
# NSRunLoop.h
NSRunLoop = ObjCClass('NSRunLoop')

NSRunLoop.declare_class_property('currentRunLoop')


######################################################################
# NSURL.h
NSURL = ObjCClass('NSURL')


######################################################################
# NSURLRequest.h
NSURLRequest = ObjCClass('NSURLRequest')
