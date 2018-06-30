##########################################################################
# System/Library/Frameworks/CoreText.framework
##########################################################################
from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################
core_text = cdll.LoadLibrary(util.find_library('CoreText'))
######################################################################

######################################################################
# CTFontDescriptor.h

CTFontOrientation = c_uint32

######################################################################
# CTFontTraits.h

CTFontSymbolicTraits = c_uint32

######################################################################
# CTFont.h
core_text.CTFontGetBoundingRectsForGlyphs.restype = CGRect
core_text.CTFontGetBoundingRectsForGlyphs.argtypes = [c_void_p, CTFontOrientation, POINTER(CGGlyph), POINTER(CGRect), CFIndex]

core_text.CTFontGetAdvancesForGlyphs.restype = c_double
core_text.CTFontGetAdvancesForGlyphs.argtypes = [c_void_p, CTFontOrientation, POINTER(CGGlyph), POINTER(CGSize), CFIndex]

core_text.CTFontGetAscent.restype = CGFloat
core_text.CTFontGetAscent.argtypes = [c_void_p]

core_text.CTFontGetDescent.restype = CGFloat
core_text.CTFontGetDescent.argtypes = [c_void_p]

core_text.CTFontGetSymbolicTraits.restype = CTFontSymbolicTraits
core_text.CTFontGetSymbolicTraits.argtypes = [c_void_p]

core_text.CTFontGetGlyphsForCharacters.restype = c_bool
core_text.CTFontGetGlyphsForCharacters.argtypes = [c_void_p, POINTER(UniChar), POINTER(CGGlyph), CFIndex]

core_text.CTFontCreateWithGraphicsFont.restype = c_void_p
core_text.CTFontCreateWithGraphicsFont.argtypes = [c_void_p, CGFloat, c_void_p, c_void_p]

core_text.CTFontCopyFamilyName.restype = c_void_p
core_text.CTFontCopyFamilyName.argtypes = [c_void_p]

core_text.CTFontCopyFullName.restype = c_void_p
core_text.CTFontCopyFullName.argtypes = [c_void_p]

core_text.CTFontCreateWithFontDescriptor.restype = c_void_p
core_text.CTFontCreateWithFontDescriptor.argtypes = [c_void_p, CGFloat, c_void_p]

core_text.CTFontDescriptorCreateWithAttributes.restype = c_void_p
core_text.CTFontDescriptorCreateWithAttributes.argtypes = [c_void_p]

######################################################################
# CTFontDescriptor.h

kCTFontFamilyNameAttribute = c_void_p.in_dll(core_text, 'kCTFontFamilyNameAttribute')
kCTFontTraitsAttribute = c_void_p.in_dll(core_text, 'kCTFontTraitsAttribute')

######################################################################
# CTFontTraits.h

kCTFontSymbolicTrait = c_void_p.in_dll(core_text, 'kCTFontSymbolicTrait')
kCTFontWeightTrait = c_void_p.in_dll(core_text, 'kCTFontWeightTrait')

kCTFontItalicTrait = (1 << 0)
kCTFontBoldTrait = (1 << 1)

######################################################################
# CTLine.h

core_text.CTLineCreateWithAttributedString.restype = c_void_p
core_text.CTLineCreateWithAttributedString.argtypes = [c_void_p]

core_text.CTLineDraw.restype = None
core_text.CTLineDraw.argtypes = [c_void_p, c_void_p]

######################################################################
# CTStringAttributes.h

kCTFontAttributeName = c_void_p.in_dll(core_text, 'kCTFontAttributeName')
