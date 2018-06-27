##########################################################################
# System/Library/Frameworks/CoreText.framework
##########################################################################
from ctypes import *
from ctypes import util
from ctypes import POINTER

from rubicon.objc.types import register_preferred_encoding
from rubicon.objc import *

from .core_graphics import CGPathRef, CGContextRef
from .core_foundation import CFArrayRef

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
# CTFrame.h

CTFrameRef = c_void_p
register_preferred_encoding(b'^{__CTFrame=}', CTFrameRef)

core_text.CTFrameGetLines.restype = CFArrayRef
core_text.CTFrameGetLines.argtypes = [CTFrameRef]

core_text.CTFrameGetLineOrigins.restype = c_void_p
# ctypes allows array instances of CGPoint to be passed to POINTER(CGPoint)
core_text.CTFrameGetLineOrigins.argtypes = [CTFrameRef, CFRange, POINTER(CGPoint)]

######################################################################
# CTFramesetter.h


class CTFramesetterRef(c_void_p):
    pass

register_preferred_encoding(b'^{__CTFramesetter=}', CTFramesetterRef)

NSAttributedStringRef = c_void_p
register_preferred_encoding(b'^{__NSAttributedString=}', NSAttributedStringRef)

core_text.CTFramesetterCreateWithAttributedString.restype = CTFramesetterRef
core_text.CTFramesetterCreateWithAttributedString.argtypes = [NSAttributedStringRef]


class CTFrameRef(c_void_p):
    pass


register_preferred_encoding(b'^{__CTFrame=}', CTFrameRef)

core_text.CTFramesetterCreateFrame.restype = CTFrameRef
core_text.CTFramesetterCreateFrame.argtypes = [CTFramesetterRef, CFRange, CGPathRef, c_void_p]

######################################################################
# CTLine.h

CTLineRef = c_void_p
register_preferred_encoding(b'^{__CTLine=}', CTLineRef)

core_text.CTLineCreateWithAttributedString.restype = CTLineRef
core_text.CTLineCreateWithAttributedString.argtypes = [NSAttributedStringRef]

core_text.CTLineDraw.restype = c_void_p
core_text.CTLineDraw.argtypes = [CTLineRef, CGContextRef]

######################################################################
# CTStringAttributes.h

kCTFontAttributeName = c_void_p.in_dll(core_text, 'kCTFontAttributeName')
