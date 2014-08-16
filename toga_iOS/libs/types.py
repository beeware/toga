from __future__ import print_function, absolute_import, division

from ctypes import *

import platform, struct

__LP64__ = (8*struct.calcsize("P") == 64)
__i386__ = (platform.machine() == 'i386')

PyObjectEncoding = b'{PyObject=@}'

def encoding_for_ctype(vartype):
    typecodes = {c_char:b'c', c_int:b'i', c_short:b's', c_long:b'l', c_longlong:b'q',
                 c_ubyte:b'C', c_uint:b'I', c_ushort:b'S', c_ulong:b'L', c_ulonglong:b'Q',
                 c_float:b'f', c_double:b'd', c_bool:b'B', c_char_p:b'*', c_void_p:b'@',
                 py_object:PyObjectEncoding}
    return typecodes.get(vartype, b'?')

try:
    text = unicode
except NameError:
    text = str


# Note CGBase.h located at
# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreGraphics.framework/Headers/CGBase.h
# defines CGFloat as double if __LP64__, otherwise it's a float.
NSInteger = c_int
NSUInteger = c_uint
CGFloat = c_float
NSPointEncoding = b'{CGPoint=ff}'
NSSizeEncoding = b'{CGSize=ff}'
NSRectEncoding = b'{CGRect={CGPoint=ff}{CGSize=ff}}'

NSRangeEncoding = b'{_NSRange=II}'

NSIntegerEncoding = encoding_for_ctype(NSInteger)
NSUIntegerEncoding = encoding_for_ctype(NSUInteger)
CGFloatEncoding = encoding_for_ctype(CGFloat)

# Special case so that NSImage.initWithCGImage_size_() will work.
CGImageEncoding = b'{CGImage=}'

NSZoneEncoding = b'{_NSZone=}'

# from /System/Library/Frameworks/Foundation.framework/Headers/NSGeometry.h
class NSPoint(Structure):
    _fields_ = [
        ("x", CGFloat),
        ("y", CGFloat)
    ]

class NSSize(Structure):
    _fields_ = [
        ("width", CGFloat),
        ("height", CGFloat)
    ]

class NSRect(Structure):
    _fields_ = [
        ("origin", NSPoint),
        ("size", NSSize)
    ]

def NSMakeSize(w, h):
    return NSSize(w, h)

def NSMakeRect(x, y, w, h):
    return NSRect(NSPoint(x, y), NSSize(w, h))

def NSMakePoint(x, y):
    return NSPoint(x, y)


# NSDate.h
NSTimeInterval = c_double

CFIndex = c_long
UniChar = c_ushort
unichar = c_wchar  # (actually defined as c_ushort in NSString.h, but need ctypes to convert properly)
CGGlyph = c_ushort

# CFRange struct defined in CFBase.h
# This replaces the CFRangeMake(LOC, LEN) macro.
class CFRange(Structure):
    _fields_ = [
        ("location", CFIndex),
        ("length", CFIndex)
    ]

# NSRange.h  (Note, not defined the same as CFRange)
class NSRange(Structure):
    _fields_ = [
        ("location", NSUInteger),
        ("length", NSUInteger)
    ]

NSZeroPoint = NSPoint(0,0)

CFTypeID = c_ulong
CFNumberType = c_uint32
