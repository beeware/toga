from ctypes import *
from ctypes import util
from enum import Enum

from rubicon.objc import *

from toga.constants import *

######################################################################

# APPLICATION KIT

# Even though we don't use this directly, it must be loaded so that
# we can find the NSApplication, NSWindow, and NSView classes.
appkit = cdll.LoadLibrary(util.find_library('AppKit'))

NSDefaultRunLoopMode = c_void_p.in_dll(appkit, 'NSDefaultRunLoopMode')
NSEventTrackingRunLoopMode = c_void_p.in_dll(appkit, 'NSEventTrackingRunLoopMode')
NSApplicationDidHideNotification = c_void_p.in_dll(appkit, 'NSApplicationDidHideNotification')
NSApplicationDidUnhideNotification = c_void_p.in_dll(appkit, 'NSApplicationDidUnhideNotification')

# NSEvent.h
NSAnyEventMask = 0xFFFFFFFF  # NSUIntegerMax

NSKeyDown = 10
NSKeyUp = 11
NSFlagsChanged = 12
NSApplicationDefined = 15

NSAlphaShiftKeyMask = 1 << 16
NSShiftKeyMask = 1 << 17
NSControlKeyMask = 1 << 18
NSAlternateKeyMask = 1 << 19
NSCommandKeyMask = 1 << 20
NSNumericPadKeyMask = 1 << 21
NSHelpKeyMask = 1 << 22
NSFunctionKeyMask = 1 << 23

NSInsertFunctionKey = 0xF727
NSDeleteFunctionKey = 0xF728
NSHomeFunctionKey = 0xF729
NSBeginFunctionKey = 0xF72A
NSEndFunctionKey = 0xF72B
NSPageUpFunctionKey = 0xF72C
NSPageDownFunctionKey = 0xF72D

# NSWindow.h
NSBorderlessWindowMask = 0
NSTitledWindowMask = 1 << 0
NSClosableWindowMask = 1 << 1
NSMiniaturizableWindowMask = 1 << 2
NSResizableWindowMask = 1 << 3

NSWindow = ObjCClass('NSWindow')

# NSButton.h
NSButton = ObjCClass('NSButton')

# NSButtonCell.h
NSMomentaryLightButton = 0
NSPushOnPushOffButton = 1
NSToggleButton = 2
NSSwitchButton = 3
NSRadioButton = 4
NSMomentaryChangeButton = 5
NSOnOffButton = 6
NSMomentaryPushInButton = 7

NSRoundedBezelStyle = 1
NSRegularSquareBezelStyle = 2
NSThickSquareBezelStyle = 3
NSThickerSquareBezelStyle = 4
NSDisclosureBezelStyle = 5
NSShadowlessSquareBezelStyle = 6
NSCircularBezelStyle = 7
NSTexturedSquareBezelStyle = 8
NSHelpButtonBezelStyle = 9
NSSmallSquareBezelStyle = 10
NSTexturedRoundedBezelStyle = 11
NSRoundRectBezelStyle = 12
NSRecessedBezelStyle = 13
NSRoundedDisclosureBezelStyle = 14

# NSPanel.h
NSUtilityWindowMask = 1 << 4

# NSGraphics.h
NSBackingStoreRetained = 0
NSBackingStoreNonretained = 1
NSBackingStoreBuffered = 2

# NSTrackingArea.h
NSTrackingMouseEnteredAndExited = 0x01
NSTrackingMouseMoved = 0x02
NSTrackingCursorUpdate = 0x04
NSTrackingActiveInActiveApp = 0x40

# NSOpenGL.h
NSOpenGLPFAAllRenderers = 1  # choose from all available renderers
NSOpenGLPFADoubleBuffer = 5  # choose a double buffered pixel format
NSOpenGLPFAStereo = 6  # stereo buffering supported
NSOpenGLPFAAuxBuffers = 7  # number of aux buffers
NSOpenGLPFAColorSize = 8  # number of color buffer bits
NSOpenGLPFAAlphaSize = 11  # number of alpha component bits
NSOpenGLPFADepthSize = 12  # number of depth buffer bits
NSOpenGLPFAStencilSize = 13  # number of stencil buffer bits
NSOpenGLPFAAccumSize = 14  # number of accum buffer bits
NSOpenGLPFAMinimumPolicy = 51  # never choose smaller buffers than requested
NSOpenGLPFAMaximumPolicy = 52  # choose largest buffers of type requested
NSOpenGLPFAOffScreen = 53  # choose an off-screen capable renderer
NSOpenGLPFAFullScreen = 54  # choose a full-screen capable renderer
NSOpenGLPFASampleBuffers = 55  # number of multi sample buffers
NSOpenGLPFASamples = 56  # number of samples per multi sample buffer
NSOpenGLPFAAuxDepthStencil = 57  # each aux buffer has its own depth stencil
NSOpenGLPFAColorFloat = 58  # color buffers store floating point pixels
NSOpenGLPFAMultisample = 59  # choose multisampling
NSOpenGLPFASupersample = 60  # choose supersampling
NSOpenGLPFASampleAlpha = 61  # request alpha filtering
NSOpenGLPFARendererID = 70  # request renderer by ID
NSOpenGLPFASingleRenderer = 71  # choose a single renderer for all screens
NSOpenGLPFANoRecovery = 72  # disable all failure recovery systems
NSOpenGLPFAAccelerated = 73  # choose a hardware accelerated renderer
NSOpenGLPFAClosestPolicy = 74  # choose the closest color buffer to request
NSOpenGLPFARobust = 75  # renderer does not need failure recovery
NSOpenGLPFABackingStore = 76  # back buffer contents are valid after swap
NSOpenGLPFAMPSafe = 78  # renderer is multi-processor safe
NSOpenGLPFAWindow = 80  # can be used to render to an onscreen window
NSOpenGLPFAMultiScreen = 81  # single window can span multiple screens
NSOpenGLPFACompliant = 83  # renderer is opengl compliant
NSOpenGLPFAScreenMask = 84  # bit mask of supported physical screens
NSOpenGLPFAPixelBuffer = 90  # can be used to render to a pbuffer
NSOpenGLPFARemotePixelBuffer = 91  # can be used to render offline to a pbuffer
NSOpenGLPFAAllowOfflineRenderers = 96  # allow use of offline renderers
NSOpenGLPFAAcceleratedCompute = 97  # choose a hardware accelerated compute device
NSOpenGLPFAVirtualScreenCount = 128  # number of virtual screens in this format

NSOpenGLCPSwapInterval = 222

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

# NSLayoutFormatAlignAllLeft = (1 << NSLayoutAttributeLeft)
# NSLayoutFormatAlignAllRight = (1 << NSLayoutAttributeRight)
# NSLayoutFormatAlignAllTop = (1 << NSLayoutAttributeTop)
# NSLayoutFormatAlignAllBottom = (1 << NSLayoutAttributeBottom)
# NSLayoutFormatAlignAllLeading = (1 << NSLayoutAttributeLeading)
# NSLayoutFormatAlignAllTrailing = (1 << NSLayoutAttributeTrailing)
# NSLayoutFormatAlignAllCenterX = (1 << NSLayoutAttributeCenterX)
# NSLayoutFormatAlignAllCenterY = (1 << NSLayoutAttributeCenterY)
# NSLayoutFormatAlignAllBaseline = (1 << NSLayoutAttributeBaseline)

# NSLayoutFormatAlignmentMask = 0xFFFF

# NSLayoutFormatDirectionLeadingToTrailing = 0 << 16
# NSLayoutFormatDirectionLeftToRight = 1 << 16
# NSLayoutFormatDirectionRightToLeft = 2 << 16

# NSLayoutFormatDirectionMask = 0x3 << 16

# NSLayoutConstraintOrientationHorizontal = 0,
# NSLayoutConstraintOrientationVertical = 1


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


# NSAlert.h
NSWarningAlertStyle = 0
NSInformationalAlertStyle = 1
NSCriticalAlertStyle = 2

NSAlertFirstButtonReturn = 1000
NSAlertSecondButtonReturn = 1001
NSAlertThirdButtonReturn = 1002

NSAlert = ObjCClass('NSAlert')

# NSApplication.h
NSApplication = ObjCClass('NSApplication')

NSApplicationPresentationDefault = 0
NSApplicationPresentationHideDock = 1 << 1
NSApplicationPresentationHideMenuBar = 1 << 3
NSApplicationPresentationDisableProcessSwitching = 1 << 5
NSApplicationPresentationDisableHideApplication = 1 << 8

# NSColor.h
NSColor = ObjCClass('NSColor')

# NSImage.h
NSImage = ObjCClass('NSImage')

NSImageAlignCenter = 0
NSImageAlignTop = 2
NSImageAlignTopLeft = 3
NSImageAlignTopRight = 4
NSImageAlignLeft = 5
NSImageAlignBottom = 6
NSImageAlignBottomLeft = 7
NSImageAlignBottomRight = 8
NSImageAlignRight = 9

NSImageScaleProportionallyDown = 0
NSImageScaleAxesIndependently = 1
NSImageScaleNone = 2
NSImageScaleProportionallyUpOrDown = 3

# NSImageView.h
NSImageView = ObjCClass('NSImageView')

# NSImageCell.h

NSImageFrameNone = 0
NSImageFramePhoto = 1
NSImageFrameGrayBezel = 2
NSImageFrameGroove = 3
NSImageFrameButton = 4

# NSMenu.h
NSMenu = ObjCClass('NSMenu')
NSMenuItem = ObjCClass('NSMenuItem')

# NSOutlineView.h
NSOutlineView = ObjCClass('NSOutlineView')

# NSRunningApplication.h
NSApplicationActivationPolicyRegular = 0
NSApplicationActivationPolicyAccessory = 1
NSApplicationActivationPolicyProhibited = 2

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

# NSTextField.h
NSTextField = ObjCClass('NSTextField')

# NSTextFieldCell.h
NSTextFieldSquareBezel = 0
NSTextFieldRoundedBezel = 1

# NSView.h
NSView = ObjCClass('NSView')

NSViewNotSizable = 0
NSViewMinXMargin = 1
NSViewWidthSizable = 2
NSViewMaxXMargin = 4
NSViewMinYMargin = 8
NSViewHeightSizable = 16
NSViewMaxYMargin = 32

NSNoBorder = 0
NSLineBorder = 1
NSBezelBorder = 2
NSGrooveBorder = 3

# NSProgressIndicator.h

NSProgressIndicatorBarStyle = 0
NSProgressIndicatorSpinningStyle = 1

NSProgressIndicator = ObjCClass('NSProgressIndicator')

# NSScreen.h
NSScreen = ObjCClass('NSScreen')

# NSScrollView.h
NSScrollView = ObjCClass('NSScrollView')

# NSSplitView.h
NSSplitView = ObjCClass('NSSplitView')

# NSSecureTextField.h
NSSecureTextField = ObjCClass('NSSecureTextField')

# NSTabView.h
NSTabView = ObjCClass('NSTabView')
NSTabViewItem = ObjCClass('NSTabViewItem')

# NSTableView.h
NSTableViewNoColumnAutoresizing = 0
NSTableViewUniformColumnAutoresizingStyle = 1
NSTableViewSequentialColumnAutoresizingStyle = 2
NSTableViewReverseSequentialColumnAutoresizingStyle = 3
NSTableViewLastColumnOnlyAutoresizingStyle = 4
NSTableViewFirstColumnOnlyAutoresizingStyle = 5

NSTableView = ObjCClass('NSTableView')
NSTableColumn = ObjCClass('NSTableColumn')

# NSTextView
NSTextView = ObjCClass('NSTextView')

# NSTimer
NSTimer = ObjCClass('NSTimer')

# NSToolbar.h

NSToolbar = ObjCClass('NSToolbar')
NSToolbarItem = ObjCClass('NSToolbarItem')

# NSPopUpButton

NSPopUpButton = ObjCClass('NSPopUpButton')

# NSStepper

NSStepper = ObjCClass('NSStepper')
