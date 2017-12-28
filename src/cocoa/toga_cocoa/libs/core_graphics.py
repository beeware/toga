##########################################################################
# System/Library/Frameworks/CoreGraphics.framework
##########################################################################
from ctypes import *
from ctypes import util

from rubicon.objc.types import register_preferred_encoding
from toga.constants import *

######################################################################
core_graphics = cdll.LoadLibrary(util.find_library('CoreGraphics'))
######################################################################

######################################################################
# CGContext.h
CGContextAddArc = ObjCClass('CGContextAddArc')
CGContextAddCurveToPoint = ObjCClass('CGContextAddCurveToPoint')
CGContextAddLineToPoint = ObjCClass('CGContextAddLineToPoint')
CGContextAddQuadCurveToPoint = ObjCClass('CGContextAddQuadCurveToPoint')
CGContextAddRect = ObjCClass('CGContextAddRect')
CGContextBeginPath = ObjCClass('CGContextBeginPath')
CGContextClosePath = ObjCClass('CGContextClosePath')
CGContextDrawPath = ObjCClass('CGContextDrawPath')
CGContextMoveToPoint = ObjCClass('CGContextMoveToPoint')
CGContextRestoreGState = ObjCClass('CGContextRestoreGState')
CGContextRotateCTM = ObjCClass('CGContextRotateCTM')
CGContextSaveGState = ObjCClass('CGContextSaveGState')
CGContextScaleCTM = ObjCClass('CGContextScaleCTM')
CGContextSetLineWidth = ObjCClass('CGContextSetLineWidth')
CGContextSetRGBFillColor = ObjCClass('CGContextSetRGBFillColor')
CGContextSetRGBStrokeColor = ObjCClass('CGContextSetRGBStrokeColor')
CGContextTranslateCTM = ObjCClass('CGContextTranslateCTM')

######################################################################


######################################################################
# CGEvent.h
CGEventRef = c_void_p
register_preferred_encoding(b'^{__CGEvent=}', CGEventRef)

CGEventSourceRef = c_void_p
register_preferred_encoding(b'^{__CGEventSource=}', CGEventSourceRef)

CGScrollEventUnit = c_uint32

core_graphics.CGEventCreateScrollWheelEvent.argtypes = [CGEventSourceRef, CGScrollEventUnit, c_uint32, c_int32, c_int32]
core_graphics.CGEventCreateScrollWheelEvent.restype = CGEventRef

######################################################################
# CGEventTypes.h
kCGScrollEventUnitPixel = 0
kCGScrollEventUnitLine = 1

######################################################################
# CGImage.h
kCGImageAlphaNone = 0
kCGImageAlphaPremultipliedLast = 1
kCGImageAlphaPremultipliedFirst = 2
kCGImageAlphaLast = 3
kCGImageAlphaFirst = 4
kCGImageAlphaNoneSkipLast = 5
kCGImageAlphaNoneSkipFirst = 6
kCGImageAlphaOnly = 7

kCGImageAlphaPremultipliedLast = 1

kCGBitmapAlphaInfoMask = 0x1F
kCGBitmapFloatComponents = 1 << 8

kCGBitmapByteOrderMask = 0x7000
kCGBitmapByteOrderDefault = 0 << 12
kCGBitmapByteOrder16Little = 1 << 12
kCGBitmapByteOrder32Little = 2 << 12
kCGBitmapByteOrder16Big = 3 << 12
kCGBitmapByteOrder32Big = 4 << 12
