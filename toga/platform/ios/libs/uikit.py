from __future__ import print_function, absolute_import, division

from ctypes import *
from ctypes import util

from .objc import ObjCClass
from .types import *

from toga.constants import *

######################################################################

# UIKit

uikit = cdll.LoadLibrary(util.find_library('UIKit'))

uikit.UIApplicationMain.restype = c_int
uikit.UIApplicationMain.argtypes = [c_int, POINTER(c_char_p), c_void_p, c_void_p]


# NSView.h
NSView = ObjCClass('UIView')

# NSLayoutConstraint.h
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

NSLayoutRelationLessThanOrEqual = -1
NSLayoutRelationEqual = 0
NSLayoutRelationGreaterThanOrEqual = 1

NSLayoutAttributeLeft = 1
NSLayoutAttributeRight = 2
NSLayoutAttributeTop = 3
NSLayoutAttributeBottom = 4
NSLayoutAttributeLeading = 5
NSLayoutAttributeTrailing = 6
NSLayoutAttributeWidth = 7
NSLayoutAttributeHeight = 8
NSLayoutAttributeCenterX = 9
NSLayoutAttributeCenterY = 10
NSLayoutAttributeBaseline = 11

NSLayoutAttributeNotAnAttribute = 0

NSLayoutFormatAlignAllLeft = (1 << NSLayoutAttributeLeft)
NSLayoutFormatAlignAllRight = (1 << NSLayoutAttributeRight)
NSLayoutFormatAlignAllTop = (1 << NSLayoutAttributeTop)
NSLayoutFormatAlignAllBottom = (1 << NSLayoutAttributeBottom)
NSLayoutFormatAlignAllLeading = (1 << NSLayoutAttributeLeading)
NSLayoutFormatAlignAllTrailing = (1 << NSLayoutAttributeTrailing)
NSLayoutFormatAlignAllCenterX = (1 << NSLayoutAttributeCenterX)
NSLayoutFormatAlignAllCenterY = (1 << NSLayoutAttributeCenterY)
NSLayoutFormatAlignAllBaseline = (1 << NSLayoutAttributeBaseline)

NSLayoutFormatAlignmentMask = 0xFFFF

NSLayoutFormatDirectionLeadingToTrailing = 0 << 16
NSLayoutFormatDirectionLeftToRight = 1 << 16
NSLayoutFormatDirectionRightToLeft = 2 << 16

NSLayoutFormatDirectionMask = 0x3 << 16

NSLayoutConstraintOrientationHorizontal = 0,
NSLayoutConstraintOrientationVertical = 1

class NSEdgetInsets(Structure):
    _fields_ = [
        ("top", CGFloat),
        ("left", CGFloat),
        ("bottom", CGFloat),
        ("right", CGFloat),
    ]

def NSEdgeInsetsMake(top, left, bottom, right):
    return NSEdgeInsets(top, left, bottom, right)

NSLayoutPriorityRequired = 1000
NSLayoutPriorityDefaultHigh = 750
NSLayoutPriorityDragThatCanResizeWindow = 510
NSLayoutPriorityWindowSizeStayPut = 500
NSLayoutPriorityDragThatCannotResizeWindow = 490
NSLayoutPriorityDefaultLow = 250
NSLayoutPriorityFittingSizeCompression = 50

# NSText.h
NSLeftTextAlignment = 0
NSRightTextAlignment = 1
NSCenterTextAlignment = 2
NSJustifiedTextAlignment = 3
NSNaturalTextAlignment = 4

def NSTextAlignment(alignment):
    return {
        LEFT_ALIGNED: NSLeftTextAlignment,
        RIGHT_ALIGNED: NSRightTextAlignment,
        CENTER_ALIGNED: NSCenterTextAlignment,
        JUSTIFIED_ALIGNED: NSJustifiedTextAlignment,
        NATURAL_ALIGNED: NSNaturalTextAlignment,
    }[alignment]

# UIControl.h

# UIControlEvents
UIControlEventTouchDown = 1 << 0
UIControlEventTouchDownRepeat = 1 << 1
UIControlEventTouchDragInside = 1 << 2
UIControlEventTouchDragOutside = 1 << 3
UIControlEventTouchDragEnter = 1 << 4
UIControlEventTouchDragExit = 1 << 5
UIControlEventTouchUpInside = 1 << 6
UIControlEventTouchUpOutside = 1 << 7
UIControlEventTouchCancel = 1 << 8

UIControlEventValueChanged = 1 << 12

UIControlEventEditingDidBegin = 1 << 16
UIControlEventEditingChanged = 1 << 17
UIControlEventEditingDidEnd = 1 << 18
UIControlEventEditingDidEndOnExit = 1 << 19

UIControlEventAllTouchEvents = 0x00000FFF
UIControlEventAllEditingEvents = 0x000F0000
UIControlEventApplicationReserved = 0x0F000000
UIControlEventSystemReserved = 0xF0000000
UIControlEventAllEvents = 0xFFFFFFFF

#  UIControlContentVerticalAlignment
UIControlContentVerticalAlignmentCenter = 0
UIControlContentVerticalAlignmentTop = 1
UIControlContentVerticalAlignmentBottom = 2
UIControlContentVerticalAlignmentFill = 3

# UIControlContentHorizontalAlignment
UIControlContentHorizontalAlignmentCenter = 0
UIControlContentHorizontalAlignmentLeft = 1
UIControlContentHorizontalAlignmentRight = 2
UIControlContentHorizontalAlignmentFill = 3

# UIControlState
UIControlStateNormal = 0
UIControlStateHighlighted = 1 << 0
UIControlStateDisabled = 1 << 1
UIControlStateSelected = 1 << 2
UIControlStateApplication = 0x00FF0000
UIControlStateReserved = 0xFF000000


# UIWindow.h
UIWindow = ObjCClass('UIWindow')

# UIScreen.h
UIScreen = ObjCClass('UIScreen')

# UIColor.h
UIColor = ObjCClass('UIColor')

# UIView.h
UIView = ObjCClass('UIView')

# UIWindow.h
UIWindow = ObjCClass('UIWindow')

# UILabel.h
UILabel = ObjCClass('UILabel')

# UIButton.h
UIButton = ObjCClass('UIButton')

# UIViewController.h
UIViewController = ObjCClass('UIViewController')

# UITextField.h
UITextField = ObjCClass('UITextField')

UITextBorderStyleNone = 0
UITextBorderStyleLine = 1
UITextBorderStyleBezel = 2
UITextBorderStyleRoundedRect = 3

