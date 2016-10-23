from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################

# CORETEXT
ct = cdll.LoadLibrary(util.find_library('CoreText'))

# Types
CTFontOrientation = c_uint32  # CTFontDescriptor.h
CTFontSymbolicTraits = c_uint32  # CTFontTraits.h

# CoreText constants
kCTFontAttributeName = c_void_p.in_dll(ct, 'kCTFontAttributeName')
kCTFontFamilyNameAttribute = c_void_p.in_dll(ct, 'kCTFontFamilyNameAttribute')
kCTFontSymbolicTrait = c_void_p.in_dll(ct, 'kCTFontSymbolicTrait')
kCTFontWeightTrait = c_void_p.in_dll(ct, 'kCTFontWeightTrait')
kCTFontTraitsAttribute = c_void_p.in_dll(ct, 'kCTFontTraitsAttribute')

# constants from CTFontTraits.h
kCTFontItalicTrait = (1 << 0)
kCTFontBoldTrait = (1 << 1)

ct.CTLineCreateWithAttributedString.restype = c_void_p
ct.CTLineCreateWithAttributedString.argtypes = [c_void_p]

ct.CTLineDraw.restype = None
ct.CTLineDraw.argtypes = [c_void_p, c_void_p]

ct.CTFontGetBoundingRectsForGlyphs.restype = CGRect
ct.CTFontGetBoundingRectsForGlyphs.argtypes = [c_void_p, CTFontOrientation, POINTER(CGGlyph), POINTER(CGRect), CFIndex]

ct.CTFontGetAdvancesForGlyphs.restype = c_double
ct.CTFontGetAdvancesForGlyphs.argtypes = [c_void_p, CTFontOrientation, POINTER(CGGlyph), POINTER(CGSize), CFIndex]

ct.CTFontGetAscent.restype = CGFloat
ct.CTFontGetAscent.argtypes = [c_void_p]

ct.CTFontGetDescent.restype = CGFloat
ct.CTFontGetDescent.argtypes = [c_void_p]

ct.CTFontGetSymbolicTraits.restype = CTFontSymbolicTraits
ct.CTFontGetSymbolicTraits.argtypes = [c_void_p]

ct.CTFontGetGlyphsForCharacters.restype = c_bool
ct.CTFontGetGlyphsForCharacters.argtypes = [c_void_p, POINTER(UniChar), POINTER(CGGlyph), CFIndex]

ct.CTFontCreateWithGraphicsFont.restype = c_void_p
ct.CTFontCreateWithGraphicsFont.argtypes = [c_void_p, CGFloat, c_void_p, c_void_p]

ct.CTFontCopyFamilyName.restype = c_void_p
ct.CTFontCopyFamilyName.argtypes = [c_void_p]

ct.CTFontCopyFullName.restype = c_void_p
ct.CTFontCopyFullName.argtypes = [c_void_p]

ct.CTFontCreateWithFontDescriptor.restype = c_void_p
ct.CTFontCreateWithFontDescriptor.argtypes = [c_void_p, CGFloat, c_void_p]

ct.CTFontDescriptorCreateWithAttributes.restype = c_void_p
ct.CTFontDescriptorCreateWithAttributes.argtypes = [c_void_p]
