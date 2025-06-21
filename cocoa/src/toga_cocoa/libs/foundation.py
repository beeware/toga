##########################################################################
# System/Library/Frameworks/Foundation.framework
##########################################################################
from ctypes import c_bool
from enum import IntFlag

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
