##########################################################################
# System/Library/Frameworks/UIKit.framework
##########################################################################
from ctypes import *
from ctypes import util
from enum import Enum

from rubicon.objc import *
from toga.constants import *

######################################################################
uikit = cdll.LoadLibrary(util.find_library('UIKit'))
######################################################################

uikit.UIApplicationMain.restype = c_int
uikit.UIApplicationMain.argtypes = [c_int, POINTER(c_char_p), c_void_p, c_void_p]

######################################################################
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


class NSLayoutPriority(Enum):
    Required = 1000
    DefaultHigh = 750
    DragThatCanResizeWindow = 510
    WindowSizeStayPut = 500
    DragThatCannotResizeWindow = 490
    DefaultLow = 250
    FittingSizeCompression = 50

######################################################################
# NSParagraphStyle.h
NSLineBreakByWordWrapping = 0
NSLineBreakByCharWrapping = 1
NSLineBreakByClipping = 2
NSLineBreakByTruncatingHead = 3
NSLineBreakByTruncatingTail = 4
NSLineBreakByTruncatingMiddle = 5

######################################################################
# NSText.h (The order is different on macOS and iOS)
NSLeftTextAlignment = 0
NSCenterTextAlignment = 1
NSRightTextAlignment = 2
NSJustifiedTextAlignment = 3
NSNaturalTextAlignment = 4

def NSTextAlignment(alignment):
    return {
        LEFT: NSLeftTextAlignment,
        RIGHT: NSRightTextAlignment,
        CENTER: NSCenterTextAlignment,
        JUSTIFY: NSJustifiedTextAlignment,
    }[alignment]

######################################################################
# UIApplication.h
UIApplication = ObjCClass('UIApplication')

class UIInterfaceOrientation(Enum):
    Unknown = 0
    Portrait = 1
    PortraitUpsideDown = 2
    LandscapeLeft = 3
    LandscapeRight = 4

######################################################################
# UIBarButtonItem.h
UIBarButtonItem = ObjCClass('UIBarButtonItem')

UIBarButtonSystemItemDone = 0
UIBarButtonSystemItemCancel = 1
UIBarButtonSystemItemEdit = 2
UIBarButtonSystemItemSave = 3
UIBarButtonSystemItemAdd = 4
UIBarButtonSystemItemFlexibleSpace = 5
UIBarButtonSystemItemFixedSpace = 6
UIBarButtonSystemItemCompose = 7
UIBarButtonSystemItemReply = 8
UIBarButtonSystemItemAction = 9
UIBarButtonSystemItemOrganize = 10
UIBarButtonSystemItemBookmarks = 11
UIBarButtonSystemItemSearch = 12
UIBarButtonSystemItemRefresh = 13
UIBarButtonSystemItemStop = 14
UIBarButtonSystemItemCamera = 15
UIBarButtonSystemItemTrash = 16
UIBarButtonSystemItemPlay = 17
UIBarButtonSystemItemPause = 18
UIBarButtonSystemItemRewind = 19
UIBarButtonSystemItemFastForward = 20
UIBarButtonSystemItemUndo = 21
UIBarButtonSystemItemRedo = 22
UIBarButtonSystemItemPageCurl = 23

######################################################################
# UIButton.h
UIButton = ObjCClass('UIButton')
######################################################################
# UIColor.h
UIColor = ObjCClass('UIColor')

# System colors
UIColor.declare_class_property('darkTextColor')
UIColor.declare_class_property('lightTextColor')
UIColor.declare_class_property('groupTableViewBackgroundColor')

# Predefined colors
UIColor.declare_class_property('blackColor')
UIColor.declare_class_property('blueColor')
UIColor.declare_class_property('brownColor')
UIColor.declare_class_property('clearColor')
UIColor.declare_class_property('cyanColor')
UIColor.declare_class_property('darkGrayColor')
UIColor.declare_class_property('grayColor')
UIColor.declare_class_property('greenColor')
UIColor.declare_class_property('lightGrayColor')
UIColor.declare_class_property('magentaColor')
UIColor.declare_class_property('orangeColor')
UIColor.declare_class_property('purpleColor')
UIColor.declare_class_property('redColor')
UIColor.declare_class_property('whiteColor')
UIColor.declare_class_property('yellowColor')

######################################################################
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

######################################################################
# UIFont.h
UIFont = ObjCClass('UIFont')

######################################################################
# UIImage.h
UIImage = ObjCClass('UIImage')

######################################################################
# UIImageView.h
UIImageView = ObjCClass('UIImageView')

######################################################################
# UILabel.h
UILabel = ObjCClass('UILabel')

######################################################################
# UINavigationController.h
UINavigationController = ObjCClass('UINavigationController')

######################################################################
# UIPickerView.h
UIPickerView = ObjCClass('UIPickerView')

######################################################################
# UIRefreshControl.h
UIRefreshControl = ObjCClass('UIRefreshControl')

######################################################################
# UIResponder.h
UIResponder = ObjCClass('UIResponder')

######################################################################
# UIScreen.h
UIScreen = ObjCClass('UIScreen')
UIScreen.declare_class_property('mainScreen')

######################################################################
# UISlider.h
UISlider = ObjCClass('UISlider')

######################################################################
# UISwitch.h
UISwitch = ObjCClass('UISwitch')

######################################################################
# UITableView.h
UITableView = ObjCClass('UITableView')
UITableViewController = ObjCClass('UITableViewController')

UITableViewScrollPositionNone = 0
UITableViewScrollPositionTop = 1
UITableViewScrollPositionMiddle = 2
UITableViewScrollPositionBottom = 3

UITableViewRowAnimationFade = 0
UITableViewRowAnimationRight = 1
UITableViewRowAnimationLeft = 2
UITableViewRowAnimationTop = 3
UITableViewRowAnimationBottom = 4
UITableViewRowAnimationNone = 5
UITableViewRowAnimationMiddle = 6
UITableViewRowAnimationAutomatic = 100

######################################################################
# UITableViewCell.h
UITableViewCell = ObjCClass('UITableViewCell')

UITableViewCellStyleDefault = 0
UITableViewCellStyleValue1 = 1
UITableViewCellStyleValue2 = 2
UITableViewCellStyleSubtitle = 3

UITableViewCellEditingStyleNone = 0
UITableViewCellEditingStyleDelete = 1
UITableViewCellEditingStyleInsert = 2

UITableViewCellSeparatorStyleNone = 0
UITableViewCellSeparatorStyleSingleLine = 1

######################################################################
# UITextField.h
UITextField = ObjCClass('UITextField')

class UITextBorderStyle(Enum):
    NoBorder = 0
    Line = 1
    Bezel = 2
    RoundedRect = 3

######################################################################
# UITextInputTraits.h

class UIKeyboardType(Enum):
    Default = 0
    ASCIICapable = 1
    NumbersAndPunctuation = 2
    URL = 3
    NumberPad = 4
    PhonePad = 5
    NamePhonePad = 6
    EmailAddress = 7
    DecimalPad = 8
    Twitter = 9
    WebSearch = 10
    ASCIICapableNumberPad = 11

######################################################################
# UIView.h
UIView = ObjCClass('UIView')

class UIViewContentMode(Enum):
    ScaleToFill = 0
    ScaleAspectFit = 1
    ScaleAspectFill = 2
    Redraw = 3
    Center = 4
    Top = 5
    Bottom = 6
    Left = 7
    Right = 8
    TopLeft = 9
    TopRight = 10
    BottomLeft = 11
    BottomRight = 12

######################################################################
# UIViewController.h
UIViewController = ObjCClass('UIViewController')

######################################################################
# UIWebView.h
UIWebView = ObjCClass('UIWebView')

######################################################################
# UIWindow.h
UIWindow = ObjCClass('UIWindow')

UIKeyboardWillShowNotification = objc_const(uikit, 'UIKeyboardWillShowNotification')
UIKeyboardDidShowNotification = objc_const(uikit, 'UIKeyboardDidShowNotification')
UIKeyboardWillHideNotification = objc_const(uikit, 'UIKeyboardWillHideNotification')
UIKeyboardDidHideNotification = objc_const(uikit, 'UIKeyboardDidHideNotification')

UIKeyboardFrameEndUserInfoKey = objc_const(uikit, 'UIKeyboardFrameEndUserInfoKey')

UIKeyboardWillChangeFrameNotification = objc_const(uikit, 'UIKeyboardWillChangeFrameNotification')
UIKeyboardDidChangeFrameNotification = objc_const(uikit, 'UIKeyboardDidChangeFrameNotification')
