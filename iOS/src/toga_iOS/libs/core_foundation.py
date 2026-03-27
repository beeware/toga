from ctypes import c_bool, c_char_p, c_uint32, c_void_p, cdll, util

cf = cdll.LoadLibrary(util.find_library("CoreFoundation"))

kCFStringEncodingUTF8 = 134217984

CFBundleRef = c_void_p
CFURLRef = c_void_p
CFStringRef = c_void_p


cf.CFBundleGetMainBundle.restype = CFBundleRef
cf.CFBundleGetMainBundle.argtypes = []

cf.CFBundleCopyBundleURL.restype = CFURLRef
cf.CFBundleCopyBundleURL.argtypes = [CFBundleRef]

cf.CFBundleCopyInfoDictionaryForURL.restype = c_void_p
cf.CFBundleCopyInfoDictionaryForURL.argtypes = [CFURLRef]

cf.CFDictionaryGetValue.restype = c_void_p
cf.CFDictionaryGetValue.argtypes = [c_void_p, c_void_p]

cf.CFStringCreateWithCString.restype = CFStringRef
cf.CFStringCreateWithCString.argtypes = [c_void_p, c_char_p, c_uint32]

cf.CFBooleanGetValue.restype = c_bool
cf.CFBooleanGetValue.argtypes = [c_void_p]
