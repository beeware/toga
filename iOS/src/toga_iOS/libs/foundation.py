##########################################################################
# System/Library/Frameworks/Foundation.framework
##########################################################################
from ctypes import c_bool, cdll, util
from enum import Enum, IntFlag

from rubicon.objc import NSPoint, NSRect, ObjCClass

######################################################################
foundation = cdll.LoadLibrary(util.find_library("Foundation"))
######################################################################

foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]


######################################################################
# NSArray.h
NSMutableArray = ObjCClass("NSMutableArray")


######################################################################
# NSBundle.h
NSBundle = ObjCClass("NSBundle")


######################################################################
# NSData.h
NSData = ObjCClass("NSData")


######################################################################
# NSDate.h
NSDate = ObjCClass("NSDate")


######################################################################
# NSIndexPath.h
NSIndexPath = ObjCClass("NSIndexPath")


######################################################################
# NSNotification.h
NSNotificationCenter = ObjCClass("NSNotificationCenter")


######################################################################
# NSFileManager.h
NSFileManager = ObjCClass("NSFileManager")

######################################################################
# NSPathUtilities.h


class NSSearchPathDirectory(Enum):
    Documents = 9
    Cache = 13
    ApplicationSupport = 14
    Downloads = 15
    Movies = 17
    Music = 18
    Pictures = 19
    Public = 21


class NSSearchPathDomainMask(Enum):
    User = 1
    Local = 2
    Network = 4
    System = 8
    All = 0x0FFFF


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
# NSCalendar.h
NSCalendar = ObjCClass("NSCalendar")


class NSCalendarUnit(IntFlag):
    Era = 1 << 1
    Year = 1 << 2
    Month = 1 << 3
    Day = 1 << 4
    Hour = 1 << 5
    Minute = 1 << 6
    Second = 1 << 7
    Weekday = 1 << 9
    WeekdayOrdinal = 1 << 10
    Quarter = 1 << 11
    WeekOfMonth = 1 << 12
    WeekOfYear = 1 << 13
    YearForWeekOfYear = 1 << 14
    Nanosecond = 1 << 15
    Calendar = 1 << 20
    TimeZone = 1 << 21


NSDateComponents = ObjCClass("NSDateComponents")
