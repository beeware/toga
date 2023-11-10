##########################################################################
# System/Library/Frameworks/CoreGraphics.framework
##########################################################################
from ctypes import (
    POINTER,
    Structure,
    c_bool,
    c_int,
    c_int32,
    c_size_t,
    c_void_p,
    c_wchar_p,
    cdll,
    util,
)

from rubicon.objc import CGFloat, CGPoint, CGRect, CGSize
from rubicon.objc.types import register_preferred_encoding

######################################################################
core_graphics = cdll.LoadLibrary(util.find_library("CoreGraphics"))
######################################################################

######################################################################
# CGAffineTransform.h


class CGAffineTransform(Structure):
    _fields_ = [
        ("a", CGFloat),
        ("b", CGFloat),
        ("c", CGFloat),
        ("d", CGFloat),
        ("tx", CGFloat),
        ("ty", CGFloat),
    ]


core_graphics.CGAffineTransformIdentity = CGAffineTransform
core_graphics.CGAffineTransformInvert.restype = CGAffineTransform
core_graphics.CGAffineTransformInvert.argtypes = [CGAffineTransform]
core_graphics.CGAffineTransformMakeScale.restype = CGAffineTransform
core_graphics.CGAffineTransformMakeScale.argtypes = [CGFloat, CGFloat]

######################################################################
# CGContext.h
CGContextRef = c_void_p
register_preferred_encoding(b"^{__CGContext=}", CGContextRef)

CGPathDrawingMode = c_int32
kCGPathFill = 0
kCGPathEOFill = 1
kCGPathStroke = 2
kCGPathFillStroke = 3
kCGPathEOFillStroke = 4

CGTextDrawingMode = c_int32
kCGTextFill = 0
kCGTextStroke = 1
kCGTextFillStroke = 2
kCGTextInvisible = 3
kCGTextFillClip = 4
kCGTextStrokeClip = 5
kCGTextFillStrokeClip = 6
kCGTextClip = 7

CGTextEncoding = c_int32
kCGEncodingFontSpecific = 0
kCGEncodingMacRoman = 1

core_graphics.CGContextAddArc.restype = c_void_p
core_graphics.CGContextAddArc.argtypes = [
    CGContextRef,
    CGFloat,
    CGFloat,
    CGFloat,
    CGFloat,
    CGFloat,
    c_int,
]
core_graphics.CGContextAddCurveToPoint.restype = c_void_p
core_graphics.CGContextAddCurveToPoint.argtypes = [
    CGContextRef,
    CGFloat,
    CGFloat,
    CGFloat,
    CGFloat,
    CGFloat,
    CGFloat,
]
core_graphics.CGContextAddLineToPoint.restype = c_void_p
core_graphics.CGContextAddLineToPoint.argtypes = [CGContextRef, CGFloat, CGFloat]
core_graphics.CGContextAddQuadCurveToPoint.restype = c_void_p
core_graphics.CGContextAddQuadCurveToPoint.argtypes = [
    CGContextRef,
    CGFloat,
    CGFloat,
    CGFloat,
    CGFloat,
]
core_graphics.CGContextAddRect.restype = c_void_p
core_graphics.CGContextAddRect.argtypes = [CGContextRef, CGRect]
core_graphics.CGContextBeginPath.restype = c_void_p
core_graphics.CGContextBeginPath.argtypes = [c_void_p]
core_graphics.CGContextConcatCTM.restype = c_void_p
core_graphics.CGContextConcatCTM.argtypes = [CGContextRef, CGAffineTransform]
core_graphics.CGContextClosePath.restype = c_void_p
core_graphics.CGContextClosePath.argtypes = [c_void_p]
core_graphics.CGContextDrawPath.restype = c_void_p
core_graphics.CGContextDrawPath.argtypes = [CGContextRef, CGPathDrawingMode]
core_graphics.CGContextGetCTM.restype = CGAffineTransform
core_graphics.CGContextGetCTM.argtypes = [CGContextRef]
core_graphics.CGContextIsPathEmpty.restype = c_bool
core_graphics.CGContextIsPathEmpty.argtypes = [CGContextRef]
core_graphics.CGContextMoveToPoint.restype = c_void_p
core_graphics.CGContextMoveToPoint.argtypes = [CGContextRef, CGFloat, CGFloat]
core_graphics.CGContextRestoreGState.restype = c_void_p
core_graphics.CGContextRestoreGState.argtypes = [c_void_p]
core_graphics.CGContextRotateCTM.restype = c_void_p
core_graphics.CGContextRotateCTM.argtypes = [CGContextRef, CGFloat]
core_graphics.CGContextSaveGState.restype = c_void_p
core_graphics.CGContextSaveGState.argtypes = [c_void_p]
core_graphics.CGContextScaleCTM.restype = c_void_p
core_graphics.CGContextScaleCTM.argtypes = [CGContextRef, CGFloat, CGFloat]
core_graphics.CGContextSelectFont.restype = c_void_p
core_graphics.CGContextSelectFont.argtypes = [
    CGContextRef,
    c_wchar_p,
    CGFloat,
    CGTextEncoding,
]
core_graphics.CGContextSetLineWidth.restype = c_void_p
core_graphics.CGContextSetLineWidth.argtypes = [CGContextRef, CGFloat]
core_graphics.CGContextSetLineDash.restype = c_void_p
core_graphics.CGContextSetLineDash.argtypes = [
    CGContextRef,
    CGFloat,
    POINTER(CGFloat),
    c_size_t,
]
core_graphics.CGContextSetRGBFillColor.restype = c_void_p
core_graphics.CGContextSetRGBFillColor.argtypes = [
    CGContextRef,
    CGFloat,
    CGFloat,
    CGFloat,
    CGFloat,
]
core_graphics.CGContextSetRGBStrokeColor.restype = c_void_p
core_graphics.CGContextSetRGBStrokeColor.argtypes = [
    CGContextRef,
    CGFloat,
    CGFloat,
    CGFloat,
    CGFloat,
]
core_graphics.CGContextSetTextDrawingMode.restype = c_void_p
core_graphics.CGContextSetTextDrawingMode.argtypes = [CGContextRef, CGTextDrawingMode]
core_graphics.CGContextSetTextMatrix.restype = c_void_p
core_graphics.CGContextSetTextMatrix.argtypes = [CGContextRef, CGAffineTransform]
core_graphics.CGContextSetTextPosition.restype = c_void_p
core_graphics.CGContextSetTextPosition.argtypes = [CGContextRef, CGFloat, CGFloat]
core_graphics.CGContextShowTextAtPoint.restype = c_void_p
core_graphics.CGContextShowTextAtPoint.argtypes = [
    CGContextRef,
    CGFloat,
    CGFloat,
    c_wchar_p,
    c_size_t,
]
core_graphics.CGContextTranslateCTM.restype = c_void_p
core_graphics.CGContextTranslateCTM.argtypes = [CGContextRef, CGFloat, CGFloat]

######################################################################
# CGEventTypes.h
kCGImageAlphaNone = 0
kCGImageAlphaPremultipliedLast = 1
kCGImageAlphaPremultipliedFirst = 2
kCGImageAlphaLast = 3
kCGImageAlphaFirst = 4
kCGImageAlphaNoneSkipLast = 5
kCGImageAlphaNoneSkipFirst = 6
kCGImageAlphaOnly = 7

kCGBitmapAlphaInfoMask = 0x1F
kCGBitmapFloatComponents = 1 << 8

kCGBitmapByteOrderMask = 0x7000
kCGBitmapByteOrderDefault = 0 << 12
kCGBitmapByteOrder16Little = 1 << 12
kCGBitmapByteOrder32Little = 2 << 12
kCGBitmapByteOrder16Big = 3 << 12
kCGBitmapByteOrder32Big = 4 << 12

######################################################################
# CGGeometry.h


def CGRectMake(x, y, w, h):
    return CGRect(CGPoint(x, y), CGSize(w, h))


######################################################################
# CGImage.h

CGImageRef = c_void_p
register_preferred_encoding(b"^{CGImage=}", CGImageRef)

core_graphics.CGImageCreateWithImageInRect.argtypes = [CGImageRef, CGRect]
core_graphics.CGImageCreateWithImageInRect.restype = CGImageRef
