from __future__ import print_function, absolute_import, division

from ctypes import *
from ctypes import util

from .objc import ObjCInstance, ObjCClass
from .types import *

######################################################################

# CORE FOUNDATION

cf = cdll.LoadLibrary(util.find_library('CoreFoundation'))

kCFStringEncodingUTF8 = 0x08000100

CFAllocatorRef = c_void_p
CFStringEncoding = c_uint32

cf.CFStringCreateWithCString.restype = c_void_p
cf.CFStringCreateWithCString.argtypes = [CFAllocatorRef, c_char_p, CFStringEncoding]

cf.CFRelease.restype = c_void_p
cf.CFRelease.argtypes = [c_void_p]

cf.CFStringGetLength.restype = CFIndex
cf.CFStringGetLength.argtypes = [c_void_p]

cf.CFStringGetMaximumSizeForEncoding.restype = CFIndex
cf.CFStringGetMaximumSizeForEncoding.argtypes = [CFIndex, CFStringEncoding]

cf.CFStringGetCString.restype = c_bool
cf.CFStringGetCString.argtypes = [c_void_p, c_char_p, CFIndex, CFStringEncoding]

cf.CFStringGetTypeID.restype = CFTypeID
cf.CFStringGetTypeID.argtypes = []

cf.CFAttributedStringCreate.restype = c_void_p
cf.CFAttributedStringCreate.argtypes = [CFAllocatorRef, c_void_p, c_void_p]

# Core Foundation type to Python type conversion functions

def CFSTR(string):
    return ObjCInstance(c_void_p(cf.CFStringCreateWithCString(
            None, string.encode('utf8'), kCFStringEncodingUTF8)))

# Other possible names for this method:
# at, ampersat, arobe, apenstaartje (little monkey tail), strudel,
# klammeraffe (spider monkey), little_mouse, arroba, sobachka (doggie)
# malpa (monkey), snabel (trunk), papaki (small duck), afna (monkey),
# kukac (caterpillar).
def get_NSString(string):
    """Autoreleased version of CFSTR"""
    return CFSTR(string).autorelease()

def cfstring_to_string(cfstring):
    length = cf.CFStringGetLength(cfstring)
    size = cf.CFStringGetMaximumSizeForEncoding(length, kCFStringEncodingUTF8)
    buffer = c_buffer(size + 1)
    result = cf.CFStringGetCString(cfstring, buffer, len(buffer), kCFStringEncodingUTF8)
    if result:
        return text(buffer.value, 'utf-8')

cf.CFDataCreate.restype = c_void_p
cf.CFDataCreate.argtypes = [c_void_p, c_void_p, CFIndex]

cf.CFDataGetBytes.restype = None
cf.CFDataGetBytes.argtypes = [c_void_p, CFRange, c_void_p]

cf.CFDataGetLength.restype = CFIndex
cf.CFDataGetLength.argtypes = [c_void_p]

cf.CFDictionaryGetValue.restype = c_void_p
cf.CFDictionaryGetValue.argtypes = [c_void_p, c_void_p]

cf.CFDictionaryAddValue.restype = None
cf.CFDictionaryAddValue.argtypes = [c_void_p, c_void_p, c_void_p]

cf.CFDictionaryCreateMutable.restype = c_void_p
cf.CFDictionaryCreateMutable.argtypes = [CFAllocatorRef, CFIndex, c_void_p, c_void_p]

cf.CFNumberCreate.restype = c_void_p
cf.CFNumberCreate.argtypes = [CFAllocatorRef, CFNumberType, c_void_p]

cf.CFNumberGetType.restype = CFNumberType
cf.CFNumberGetType.argtypes = [c_void_p]

cf.CFNumberGetValue.restype = c_ubyte
cf.CFNumberGetValue.argtypes = [c_void_p, CFNumberType, c_void_p]

cf.CFNumberGetTypeID.restype = CFTypeID
cf.CFNumberGetTypeID.argtypes = []

cf.CFGetTypeID.restype = CFTypeID
cf.CFGetTypeID.argtypes = [c_void_p]

# CFNumber.h
kCFNumberSInt8Type = 1
kCFNumberSInt16Type = 2
kCFNumberSInt32Type = 3
kCFNumberSInt64Type = 4
kCFNumberFloat32Type = 5
kCFNumberFloat64Type = 6
kCFNumberCharType = 7
kCFNumberShortType = 8
kCFNumberIntType = 9
kCFNumberLongType = 10
kCFNumberLongLongType = 11
kCFNumberFloatType = 12
kCFNumberDoubleType = 13
kCFNumberCFIndexType = 14
kCFNumberNSIntegerType = 15
kCFNumberCGFloatType = 16
kCFNumberMaxType = 16

def cfnumber_to_number(cfnumber):
    """Convert CFNumber to python int or float."""
    numeric_type = cf.CFNumberGetType(cfnumber)
    cfnum_to_ctype = {kCFNumberSInt8Type:c_int8, kCFNumberSInt16Type:c_int16,
                      kCFNumberSInt32Type:c_int32, kCFNumberSInt64Type:c_int64,
                      kCFNumberFloat32Type:c_float, kCFNumberFloat64Type:c_double,
                      kCFNumberCharType:c_byte, kCFNumberShortType:c_short,
                      kCFNumberIntType:c_int, kCFNumberLongType:c_long,
                      kCFNumberLongLongType:c_longlong, kCFNumberFloatType:c_float,
                      kCFNumberDoubleType:c_double, kCFNumberCFIndexType:CFIndex,
                      kCFNumberCGFloatType:CGFloat}

    if numeric_type in cfnum_to_ctype:
        t = cfnum_to_ctype[numeric_type]
        result = t()
        if cf.CFNumberGetValue(cfnumber, numeric_type, byref(result)):
            return result.value
    else:
        raise Exception('cfnumber_to_number: unhandled CFNumber type %d' % numeric_type)

# Dictionary of cftypes matched to the method converting them to python values.
known_cftypes = { cf.CFStringGetTypeID() : cfstring_to_string,
                  cf.CFNumberGetTypeID() : cfnumber_to_number
                  }

def cftype_to_value(cftype):
    """Convert a CFType into an equivalent python type.
    The convertible CFTypes are taken from the known_cftypes
    dictionary, which may be added to if another library implements
    its own conversion methods."""
    if not cftype:
        return None
    typeID = cf.CFGetTypeID(cftype)
    if typeID in known_cftypes:
        convert_function = known_cftypes[typeID]
        return convert_function(cftype)
    else:
        return cftype

cf.CFSetGetCount.restype = CFIndex
cf.CFSetGetCount.argtypes = [c_void_p]

cf.CFSetGetValues.restype = None
# PyPy 1.7 is fine with 2nd arg as POINTER(c_void_p),
# but CPython ctypes 1.1.0 complains, so just use c_void_p.
cf.CFSetGetValues.argtypes = [c_void_p, c_void_p]

def cfset_to_set(cfset):
    """Convert CFSet to python set."""
    count = cf.CFSetGetCount(cfset)
    buffer = (c_void_p * count)()
    cf.CFSetGetValues(cfset, byref(buffer))
    return set([ cftype_to_value(c_void_p(buffer[i])) for i in range(count) ])

cf.CFArrayGetCount.restype = CFIndex
cf.CFArrayGetCount.argtypes = [c_void_p]

cf.CFArrayGetValueAtIndex.restype = c_void_p
cf.CFArrayGetValueAtIndex.argtypes = [c_void_p, CFIndex]

def cfarray_to_list(cfarray):
    """Convert CFArray to python list."""
    count = cf.CFArrayGetCount(cfarray)
    return [ cftype_to_value(c_void_p(cf.CFArrayGetValueAtIndex(cfarray, i)))
             for i in range(count) ]


kCFRunLoopDefaultMode = c_void_p.in_dll(cf, 'kCFRunLoopDefaultMode')

cf.CFRunLoopGetCurrent.restype = c_void_p
cf.CFRunLoopGetCurrent.argtypes = []

cf.CFRunLoopGetMain.restype = c_void_p
cf.CFRunLoopGetMain.argtypes = []


# NSArray.h

NSMutableArray = ObjCClass('NSMutableArray')

# NSURL.h

NSURL = ObjCClass('NSURL')

# NSURLRequest.h

NSURLRequest = ObjCClass('NSURLRequest')

