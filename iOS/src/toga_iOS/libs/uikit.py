##########################################################################
# System/Library/Frameworks/UIKit.framework
##########################################################################
from ctypes import POINTER, c_char_p, c_int, c_void_p, cdll, util
from enum import Enum, IntEnum

from rubicon.objc import ObjCClass, ObjCProtocol, objc_const

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT
from toga_iOS.libs.core_graphics import CGContextRef

######################################################################
uikit = cdll.LoadLibrary(util.find_library("UIKit"))
######################################################################

uikit.UIApplicationMain.restype = c_int
uikit.UIApplicationMain.argtypes = [c_int, POINTER(c_char_p), c_void_p, c_void_p]

uikit.UIImageJPEGRepresentation.restype = c_void_p
uikit.UIImageJPEGRepresentation.argtypes = [c_void_p]

uikit.UIImagePNGRepresentation.restype = c_void_p
uikit.UIImagePNGRepresentation.argtypes = [c_void_p]

######################################################################
# NSAttributedString.h
NSAttributedString = ObjCClass("NSAttributedString")

NSFontAttributeName = objc_const(uikit, "NSFontAttributeName")
NSForegroundColorAttributeName = objc_const(uikit, "NSForegroundColorAttributeName")
NSStrokeColorAttributeName = objc_const(uikit, "NSStrokeColorAttributeName")
NSStrokeWidthAttributeName = objc_const(uikit, "NSStrokeWidthAttributeName")

######################################################################
# NSLayoutConstraint.h
NSLayoutConstraint = ObjCClass("NSLayoutConstraint")

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

NSLayoutFormatAlignAllLeft = 1 << NSLayoutAttributeLeft
NSLayoutFormatAlignAllRight = 1 << NSLayoutAttributeRight
NSLayoutFormatAlignAllTop = 1 << NSLayoutAttributeTop
NSLayoutFormatAlignAllBottom = 1 << NSLayoutAttributeBottom
NSLayoutFormatAlignAllLeading = 1 << NSLayoutAttributeLeading
NSLayoutFormatAlignAllTrailing = 1 << NSLayoutAttributeTrailing
NSLayoutFormatAlignAllCenterX = 1 << NSLayoutAttributeCenterX
NSLayoutFormatAlignAllCenterY = 1 << NSLayoutAttributeCenterY
NSLayoutFormatAlignAllBaseline = 1 << NSLayoutAttributeBaseline

NSLayoutFormatAlignmentMask = 0xFFFF

NSLayoutFormatDirectionLeadingToTrailing = 0 << 16
NSLayoutFormatDirectionLeftToRight = 1 << 16
NSLayoutFormatDirectionRightToLeft = 2 << 16

NSLayoutFormatDirectionMask = 0x3 << 16

NSLayoutConstraintOrientationHorizontal = (0,)
NSLayoutConstraintOrientationVertical = 1


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
# UIAction.h

UIKeyInput = ObjCProtocol("UIKeyInput")

######################################################################
# UIActivityIndicatorView.h
UIActivityIndicatorView = ObjCClass("UIActivityIndicatorView")

######################################################################
# UIAlertController.h
UIAlertController = ObjCClass("UIAlertController")
UIAlertAction = ObjCClass("UIAlertAction")


class UIAlertControllerStyle(Enum):
    ActionSheet = 0
    Alert = 1


class UIAlertActionStyle(Enum):
    Default = 0
    Cancel = 1
    Destructive = 2


######################################################################
# UIApplication.h
UIApplication = ObjCClass("UIApplication")


class UIInterfaceOrientation(Enum):
    Unknown = 0
    Portrait = 1
    PortraitUpsideDown = 2
    LandscapeLeft = 3
    LandscapeRight = 4


######################################################################
# UIBarButtonItem.h
UIBarButtonItem = ObjCClass("UIBarButtonItem")


class UIBarButtonSystemItem(Enum):
    Done = 0
    Cancel = 1
    Edit = 2
    Save = 3
    Add = 4
    FlexibleSpace = 5
    FixedSpace = 6
    Compose = 7
    Reply = 8
    Action = 9
    Organize = 10
    Bookmarks = 11
    Search = 12
    Refresh = 13
    Stop = 14
    Camera = 15
    Trash = 16
    Play = 17
    Pause = 18
    Rewind = 19
    FastForward = 20
    Undo = 21
    Redo = 22
    PageCurl = 23


######################################################################
# UIButton.h
UIButton = ObjCClass("UIButton")


######################################################################
# UIColor.h
UIColor = ObjCClass("UIColor")

# System colors
UIColor.declare_class_property("darkTextColor")
UIColor.declare_class_property("lightTextColor")
UIColor.declare_class_property("groupTableViewBackgroundColor")

# Predefined colors
UIColor.declare_class_property("blackColor")
UIColor.declare_class_property("blueColor")
UIColor.declare_class_property("brownColor")
UIColor.declare_class_property("clearColor")
UIColor.declare_class_property("cyanColor")
UIColor.declare_class_property("darkGrayColor")
UIColor.declare_class_property("grayColor")
UIColor.declare_class_property("greenColor")
UIColor.declare_class_property("lightGrayColor")
UIColor.declare_class_property("magentaColor")
UIColor.declare_class_property("orangeColor")
UIColor.declare_class_property("purpleColor")
UIColor.declare_class_property("redColor")
UIColor.declare_class_property("whiteColor")
UIColor.declare_class_property("yellowColor")

######################################################################
# UIContextualAction.h
UIContextualAction = ObjCClass("UIContextualAction")


class UIContextualActionStyle(Enum):
    Normal = 0
    Destructive = 1


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
UIFont = ObjCClass("UIFont")
UIFont.declare_class_property("labelFontSize")
UIFontDescriptorTraitItalic = 1 << 0
UIFontDescriptorTraitBold = 1 << 1

######################################################################
# UIGraphics.h
uikit.UIGraphicsGetCurrentContext.restype = CGContextRef

######################################################################
# UIGraphicsImageRenderer.h
UIGraphicsImageRenderer = ObjCClass("UIGraphicsImageRenderer")
UIGraphicsImageRendererContext = ObjCClass("UIGraphicsImageRendererContext")

######################################################################
# UIImage.h
UIImage = ObjCClass("UIImage")

######################################################################
# UIImagePicker.h

# Camera
UIImagePickerController = ObjCClass("UIImagePickerController")

# PhotoLibrary and SavedPhotosAlbumn constants also exist, but they're marked as deprecated
UIImagePickerControllerSourceTypeCamera = 1


class UIImagePickerControllerQualityType(Enum):
    High = 0
    Medium = 1
    Low = 2


class UIImagePickerControllerCameraCaptureMode(Enum):
    Photo = 0
    Video = 1


class UIImagePickerControllerCameraDevice(Enum):
    Rear = 0
    Front = 1


class UIImagePickerControllerCameraFlashMode(Enum):
    Off = -1
    Auto = 0
    On = 1


######################################################################
# UIImageView.h
UIImageView = ObjCClass("UIImageView")

######################################################################
# UILabel.h
UILabel = ObjCClass("UILabel")

######################################################################
# UINavigationController.h
UINavigationController = ObjCClass("UINavigationController")

######################################################################
# UIPickerView.h
UIPickerView = ObjCClass("UIPickerView")

######################################################################
# UIProgressView.h
UIProgressView = ObjCClass("UIProgressView")


class UIProgressViewStyle(Enum):
    Default = 0
    Bar = 1


######################################################################
# UIRefreshControl.h
UIRefreshControl = ObjCClass("UIRefreshControl")

######################################################################
# UIResponder.h
UIResponder = ObjCClass("UIResponder")

######################################################################
# UIScreen.h
UIScreen = ObjCClass("UIScreen")
UIScreen.declare_class_property("mainScreen")

#####################################################################
# UIScrollView.h
UIScrollView = ObjCClass("UIScrollView")

######################################################################
# UISlider.h
UISlider = ObjCClass("UISlider")

######################################################################
# UIStackView.h
UIStackView = ObjCClass("UIStackView")


class UIStackViewAlignment(Enum):
    Fill = 0
    Leading = 1
    Top = 1
    FirstBaseline = 2
    Center = 3
    Trailing = 4
    Bottom = 4
    LastBaseline = 5


######################################################################
# UISwipeActionsConfiguration.h
UISwipeActionsConfiguration = ObjCClass("UISwipeActionsConfiguration")

######################################################################
# UISwitch.h
UISwitch = ObjCClass("UISwitch")

######################################################################
# UITableView.h
UITableView = ObjCClass("UITableView")
UITableViewController = ObjCClass("UITableViewController")

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
UITableViewCell = ObjCClass("UITableViewCell")

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
# UITabBarController.h

UITabBarController = ObjCClass("UITabBarController")

######################################################################
# UITabBarItem.h
UITabBarItem = ObjCClass("UITabBarItem")

######################################################################
# UITextField.h
UITextField = ObjCClass("UITextField")


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
# UITextView.h
UITextView = ObjCClass("UITextView")

######################################################################
# UIView.h
UIView = ObjCClass("UIView")


class UILayoutConstraintAxis(Enum):
    Horizontal = 0
    Vertical = 1


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


class UIViewAutoresizing(IntEnum):
    NoResizing = 0
    FlexibleLeftMargin = 1 << 0
    FlexibleWidth = 1 << 1
    FlexibleRightMargin = 1 << 2
    FlexibleTopMargin = 1 << 3
    FlexibleHeight = 1 << 4
    FlexibleBottomMargin = 1 << 5


######################################################################
# UIViewController.h
UIViewController = ObjCClass("UIViewController")

######################################################################
# UIWindow.h
UIWindow = ObjCClass("UIWindow")

UIKeyboardWillShowNotification = objc_const(uikit, "UIKeyboardWillShowNotification")
UIKeyboardDidShowNotification = objc_const(uikit, "UIKeyboardDidShowNotification")
UIKeyboardWillHideNotification = objc_const(uikit, "UIKeyboardWillHideNotification")
UIKeyboardDidHideNotification = objc_const(uikit, "UIKeyboardDidHideNotification")

UIKeyboardFrameEndUserInfoKey = objc_const(uikit, "UIKeyboardFrameEndUserInfoKey")

UIKeyboardWillChangeFrameNotification = objc_const(
    uikit, "UIKeyboardWillChangeFrameNotification"
)
UIKeyboardDidChangeFrameNotification = objc_const(
    uikit, "UIKeyboardDidChangeFrameNotification"
)
