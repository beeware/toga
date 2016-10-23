from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################

# QUARTZ / COREGRAPHICS

quartz = cdll.LoadLibrary(util.find_library('quartz'))

CGDirectDisplayID = c_uint32  # CGDirectDisplay.h
CGError = c_int32  # CGError.h
CGBitmapInfo = c_uint32  # CGImage.h

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#     ImageIO.framework/Headers/CGImageProperties.h
kCGImagePropertyGIFDictionary = c_void_p.in_dll(quartz, 'kCGImagePropertyGIFDictionary')
kCGImagePropertyGIFDelayTime = c_void_p.in_dll(quartz, 'kCGImagePropertyGIFDelayTime')

# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/...
#     CoreGraphics.framework/Headers/CGColorSpace.h
kCGRenderingIntentDefault = 0

quartz.CGDisplayIDToOpenGLDisplayMask.restype = c_uint32
quartz.CGDisplayIDToOpenGLDisplayMask.argtypes = [c_uint32]

quartz.CGMainDisplayID.restype = CGDirectDisplayID
quartz.CGMainDisplayID.argtypes = []

quartz.CGShieldingWindowLevel.restype = c_int32
quartz.CGShieldingWindowLevel.argtypes = []

quartz.CGCursorIsVisible.restype = c_bool

quartz.CGDisplayCopyAllDisplayModes.restype = c_void_p
quartz.CGDisplayCopyAllDisplayModes.argtypes = [CGDirectDisplayID, c_void_p]

quartz.CGDisplaySetDisplayMode.restype = CGError
quartz.CGDisplaySetDisplayMode.argtypes = [CGDirectDisplayID, c_void_p, c_void_p]

quartz.CGDisplayCapture.restype = CGError
quartz.CGDisplayCapture.argtypes = [CGDirectDisplayID]

quartz.CGDisplayRelease.restype = CGError
quartz.CGDisplayRelease.argtypes = [CGDirectDisplayID]

quartz.CGDisplayCopyDisplayMode.restype = c_void_p
quartz.CGDisplayCopyDisplayMode.argtypes = [CGDirectDisplayID]

quartz.CGDisplayModeGetRefreshRate.restype = c_double
quartz.CGDisplayModeGetRefreshRate.argtypes = [c_void_p]

quartz.CGDisplayModeRetain.restype = c_void_p
quartz.CGDisplayModeRetain.argtypes = [c_void_p]

quartz.CGDisplayModeRelease.restype = None
quartz.CGDisplayModeRelease.argtypes = [c_void_p]

quartz.CGDisplayModeGetWidth.restype = c_size_t
quartz.CGDisplayModeGetWidth.argtypes = [c_void_p]

quartz.CGDisplayModeGetHeight.restype = c_size_t
quartz.CGDisplayModeGetHeight.argtypes = [c_void_p]

quartz.CGDisplayModeCopyPixelEncoding.restype = c_void_p
quartz.CGDisplayModeCopyPixelEncoding.argtypes = [c_void_p]

quartz.CGGetActiveDisplayList.restype = CGError
quartz.CGGetActiveDisplayList.argtypes = [c_uint32, POINTER(CGDirectDisplayID), POINTER(c_uint32)]

quartz.CGDisplayBounds.restype = CGRect
quartz.CGDisplayBounds.argtypes = [CGDirectDisplayID]

quartz.CGImageSourceCreateWithData.restype = c_void_p
quartz.CGImageSourceCreateWithData.argtypes = [c_void_p, c_void_p]

quartz.CGImageSourceCreateImageAtIndex.restype = c_void_p
quartz.CGImageSourceCreateImageAtIndex.argtypes = [c_void_p, c_size_t, c_void_p]

quartz.CGImageSourceCopyPropertiesAtIndex.restype = c_void_p
quartz.CGImageSourceCopyPropertiesAtIndex.argtypes = [c_void_p, c_size_t, c_void_p]

quartz.CGImageGetDataProvider.restype = c_void_p
quartz.CGImageGetDataProvider.argtypes = [c_void_p]

quartz.CGDataProviderCopyData.restype = c_void_p
quartz.CGDataProviderCopyData.argtypes = [c_void_p]

quartz.CGDataProviderCreateWithCFData.restype = c_void_p
quartz.CGDataProviderCreateWithCFData.argtypes = [c_void_p]

quartz.CGImageCreate.restype = c_void_p
quartz.CGImageCreate.argtypes = [c_size_t, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, c_uint32, c_void_p, c_void_p, c_bool, c_int]

quartz.CGImageRelease.restype = None
quartz.CGImageRelease.argtypes = [c_void_p]

quartz.CGImageGetBytesPerRow.restype = c_size_t
quartz.CGImageGetBytesPerRow.argtypes = [c_void_p]

quartz.CGImageGetWidth.restype = c_size_t
quartz.CGImageGetWidth.argtypes = [c_void_p]

quartz.CGImageGetHeight.restype = c_size_t
quartz.CGImageGetHeight.argtypes = [c_void_p]

quartz.CGImageGetBitsPerPixel.restype = c_size_t
quartz.CGImageGetBitsPerPixel.argtypes = [c_void_p]

quartz.CGImageGetBitmapInfo.restype = CGBitmapInfo
quartz.CGImageGetBitmapInfo.argtypes = [c_void_p]

quartz.CGColorSpaceCreateDeviceRGB.restype = c_void_p
quartz.CGColorSpaceCreateDeviceRGB.argtypes = []

quartz.CGDataProviderRelease.restype = None
quartz.CGDataProviderRelease.argtypes = [c_void_p]

quartz.CGColorSpaceRelease.restype = None
quartz.CGColorSpaceRelease.argtypes = [c_void_p]

quartz.CGWarpMouseCursorPosition.restype = CGError
quartz.CGWarpMouseCursorPosition.argtypes = [CGPoint]

quartz.CGDisplayMoveCursorToPoint.restype = CGError
quartz.CGDisplayMoveCursorToPoint.argtypes = [CGDirectDisplayID, CGPoint]

quartz.CGAssociateMouseAndMouseCursorPosition.restype = CGError
quartz.CGAssociateMouseAndMouseCursorPosition.argtypes = [c_bool]

quartz.CGBitmapContextCreate.restype = c_void_p
quartz.CGBitmapContextCreate.argtypes = [c_void_p, c_size_t, c_size_t, c_size_t, c_size_t, c_void_p, CGBitmapInfo]

quartz.CGBitmapContextCreateImage.restype = c_void_p
quartz.CGBitmapContextCreateImage.argtypes = [c_void_p]

quartz.CGFontCreateWithDataProvider.restype = c_void_p
quartz.CGFontCreateWithDataProvider.argtypes = [c_void_p]

quartz.CGFontCreateWithFontName.restype = c_void_p
quartz.CGFontCreateWithFontName.argtypes = [c_void_p]

quartz.CGContextDrawImage.restype = None
quartz.CGContextDrawImage.argtypes = [c_void_p, CGRect, c_void_p]

quartz.CGContextRelease.restype = None
quartz.CGContextRelease.argtypes = [c_void_p]

quartz.CGContextSetTextPosition.restype = None
quartz.CGContextSetTextPosition.argtypes = [c_void_p, CGFloat, CGFloat]

quartz.CGContextSetShouldAntialias.restype = None
quartz.CGContextSetShouldAntialias.argtypes = [c_void_p, c_bool]
