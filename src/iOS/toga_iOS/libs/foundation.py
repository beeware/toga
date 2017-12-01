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
# NSArray.h
NSMutableArray = ObjCClass('NSMutableArray')

######################################################################
# NSBundle.h
NSBundle = ObjCClass('NSBundle')

######################################################################
# NSData.h
NSData = ObjCClass('NSData')

######################################################################
# NSIndexPath.h
NSIndexPath = ObjCClass('NSIndexPath')

######################################################################
# NSNSNotification.h
NSNotificationCenter = ObjCClass('NSNotificationCenter')

######################################################################
# NSURL.h
NSURL = ObjCClass('NSURL')

######################################################################
# NSURLRequest.h
NSURLRequest = ObjCClass('NSURLRequest')
