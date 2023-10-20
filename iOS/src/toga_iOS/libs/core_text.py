##########################################################################
# System/Library/Frameworks/CoreText.framework
##########################################################################
from ctypes import c_bool, c_uint32, c_void_p, cdll, util

######################################################################
core_text = cdll.LoadLibrary(util.find_library("CoreText"))
######################################################################

######################################################################
# CTFont.h

core_text.CTFontManagerRegisterFontsForURL.restype = c_bool
core_text.CTFontManagerRegisterFontsForURL.argtypes = [c_void_p, c_uint32, c_void_p]

######################################################################
# CTFontManagerScope.h

kCTFontManagerScopeNone = 0
kCTFontManagerScopeProcess = 1
kCTFontManagerScopePersistent = 2
kCTFontManagerScopeSession = 3
kCTFontManagerScopeUser = 2
