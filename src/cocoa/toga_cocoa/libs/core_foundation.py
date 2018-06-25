##########################################################################
# System/Library/Frameworks/CoreFoundation.framework
##########################################################################
from ctypes import *
from ctypes import util

from rubicon.objc.types import register_preferred_encoding
from rubicon.objc import *


######################################################################
core_found = cdll.LoadLibrary(util.find_library('CoreFoundation'))
######################################################################

######################################################################
# CFArray.h


class CFArrayRef(c_void_p):
    pass


register_preferred_encoding(b'^{__CFArray=}', CFArrayRef)


class CFArray(c_void_p):
    pass


core_found.CFArrayGetCount.argtypes = [CFArrayRef]
core_found.CFArrayGetCount.restype = CFIndex

core_found.CFArrayGetValueAtIndex.argtypes = [CFArrayRef, CFIndex]
core_found.CFArrayGetValueAtIndex.restype = c_void_p

CFTypeRef = c_void_p
core_found.CFRelease.argtypes = [CFTypeRef]
core_found.CFRelease.restype = c_void_p
