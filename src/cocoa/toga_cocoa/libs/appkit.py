##########################################################################
# System/Library/Frameworks/AppKit.framework
##########################################################################
from ctypes import *
from ctypes import util
from enum import Enum

from rubicon.objc import *

from toga.constants import *
from toga.constants.color import *

######################################################################
appkit = cdll.LoadLibrary(util.find_library('AppKit'))
######################################################################

######################################################################
# NSAffineTransform.h
NSAffineTransform = ObjCClass('NSAffineTransform')

######################################################################
# NSAlert.h
NSAlert = ObjCClass('NSAlert')

NSWarningAlertStyle = 0
NSInformationalAlertStyle = 1
NSCriticalAlertStyle = 2

NSAlertFirstButtonReturn = 1000
NSAlertSecondButtonReturn = 1001
NSAlertThirdButtonReturn = 1002

######################################################################
# NSApplication.h
NSApplication = ObjCClass('NSApplication')

NSApplicationPresentationDefault = 0
NSApplicationPresentationHideDock = 1 << 1
NSApplicationPresentationHideMenuBar = 1 << 3
NSApplicationPresentationDisableProcessSwitching = 1 << 5
NSApplicationPresentationDisableHideApplication = 1 << 8

NSEventTrackingRunLoopMode = c_void_p.in_dll(appkit, 'NSEventTrackingRunLoopMode')

NSApplicationDidHideNotification = c_void_p.in_dll(appkit, 'NSApplicationDidHideNotification')
NSApplicationDidUnhideNotification = c_void_p.in_dll(appkit, 'NSApplicationDidUnhideNotification')

######################################################################
# NSAttributedString.h

NSFontAttributeName = objc_const(appkit, "NSFontAttributeName")
NSParagraphStyleAttributeName = objc_const(appkit, "NSParagraphStyleAttributeName")
NSForegroundColorAttributeName = objc_const(appkit, "NSForegroundColorAttributeName")
NSBackgroundColorAttributeName = objc_const(appkit, "NSBackgroundColorAttributeName")
NSLigatureAttributeName = objc_const(appkit, "NSLigatureAttributeName")
NSKernAttributeName = objc_const(appkit, "NSKernAttributeName")
NSStrikethroughStyleAttributeName = objc_const(appkit, "NSStrikethroughStyleAttributeName")
NSUnderlineStyleAttributeName = objc_const(appkit, "NSUnderlineStyleAttributeName")
NSStrokeColorAttributeName = objc_const(appkit, "NSStrokeColorAttributeName")
NSStrokeWidthAttributeName = objc_const(appkit, "NSStrokeWidthAttributeName")
NSShadowAttributeName = objc_const(appkit, "NSShadowAttributeName")
NSTextEffectAttributeName = objc_const(appkit, "NSTextEffectAttributeName")

NSAttachmentAttributeName = objc_const(appkit, "NSAttachmentAttributeName")
NSLinkAttributeName = objc_const(appkit, "NSLinkAttributeName")
NSBaselineOffsetAttributeName = objc_const(appkit, "NSBaselineOffsetAttributeName")
NSUnderlineColorAttributeName = objc_const(appkit, "NSUnderlineColorAttributeName")
NSStrikethroughColorAttributeName = objc_const(appkit, "NSStrikethroughColorAttributeName")
NSObliquenessAttributeName = objc_const(appkit, "NSObliquenessAttributeName")
NSExpansionAttributeName = objc_const(appkit, "NSExpansionAttributeName")

NSWritingDirectionAttributeName = objc_const(appkit, "NSWritingDirectionAttributeName")
NSVerticalGlyphFormAttributeName = objc_const(appkit, "NSVerticalGlyphFormAttributeName")

NSCursorAttributeName = objc_const(appkit, "NSCursorAttributeName")
NSToolTipAttributeName = objc_const(appkit, "NSToolTipAttributeName")

NSMarkedClauseSegmentAttributeName = objc_const(appkit, "NSMarkedClauseSegmentAttributeName")
NSTextAlternativesAttributeName = objc_const(appkit, "NSTextAlternativesAttributeName")

NSSuperscriptAttributeName = objc_const(appkit, "NSSuperscriptAttributeName")
NSGlyphInfoAttributeName = objc_const(appkit, "NSGlyphInfoAttributeName")

NSViewBoundsDidChangeNotification = objc_const(appkit, 'NSViewBoundsDidChangeNotification')

######################################################################
# NSBezierPath.h
NSBezierPath = ObjCClass('NSBezierPath')

######################################################################
# NSBrowserCell.h
NSBrowserCell = ObjCClass('NSBrowserCell')

######################################################################
# NSButton.h
NSButton = ObjCClass('NSButton')

NSOnState = 1
NSOffState = 0
NSMixedState = -1

######################################################################
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

######################################################################
# NSCell.h
NSCell = ObjCClass('NSCell')

######################################################################
# NSClipView.h
NSClipView = ObjCClass('NSClipView')

######################################################################
# NSColor.h
NSColor = ObjCClass('NSColor')

# System colors
NSColor.declare_class_property('alternateSelectedControlColor')
NSColor.declare_class_property('alternateSelectedControlTextColor')
NSColor.declare_class_property('controlBackgroundColor')
NSColor.declare_class_property('controlColor')
NSColor.declare_class_property('controlAlternatingRowBackgroundColors')
NSColor.declare_class_property('controlHighlightColor')
NSColor.declare_class_property('controlLightHighlightColor')
NSColor.declare_class_property('controlShadowColor')
NSColor.declare_class_property('controlDarkShadowColor')
NSColor.declare_class_property('controlTextColor')
NSColor.declare_class_property('currentControlTint')
NSColor.declare_class_property('disabledControlTextColor')
NSColor.declare_class_property('gridColor')
NSColor.declare_class_property('headerColor')
NSColor.declare_class_property('headerTextColor')
NSColor.declare_class_property('highlightColor')
NSColor.declare_class_property('keyboardFocusIndicatorColor')
NSColor.declare_class_property('knobColor')
NSColor.declare_class_property('scrollBarColor')
NSColor.declare_class_property('secondarySelectedControlColor')
NSColor.declare_class_property('selectedControlColor')
NSColor.declare_class_property('selectedControlTextColor')
NSColor.declare_class_property('selectedMenuItemColor')
NSColor.declare_class_property('selectedMenuItemTextColor')
NSColor.declare_class_property('selectedTextBackgroundColor')
NSColor.declare_class_property('selectedTextColor')
NSColor.declare_class_property('selectedKnobColor')
NSColor.declare_class_property('shadowColor')
NSColor.declare_class_property('textBackgroundColor')
NSColor.declare_class_property('textColor')
NSColor.declare_class_property('windowBackgroundColor')
NSColor.declare_class_property('windowFrameColor')
NSColor.declare_class_property('windowFrameTextColor')
NSColor.declare_class_property('underPageBackgroundColor')

# System Label Colors
NSColor.declare_class_property('labelColor')
NSColor.declare_class_property('secondaryLabelColor')
NSColor.declare_class_property('tertiaryLabelColor')
NSColor.declare_class_property('quaternaryLabelColor')

# Predefined Colors
NSColor.declare_class_property('blackColor')
NSColor.declare_class_property('blueColor')
NSColor.declare_class_property('brownColor')
NSColor.declare_class_property('clearColor')
NSColor.declare_class_property('cyanColor')
NSColor.declare_class_property('darkGrayColor')
NSColor.declare_class_property('grayColor')
NSColor.declare_class_property('greenColor')
NSColor.declare_class_property('lightGrayColor')
NSColor.declare_class_property('magentaColor')
NSColor.declare_class_property('orangeColor')
NSColor.declare_class_property('purpleColor')
NSColor.declare_class_property('redColor')
NSColor.declare_class_property('whiteColor')
NSColor.declare_class_property('yellowColor')

def NSColorUsingColorName(background_color):
    return {
        Black: NSColor.blackColor,
        Blue: NSColor.blueColor,
        Brown: NSColor.brownColor,
        Clear : NSColor.clearColor,
        Cyan: NSColor.cyanColor,
        DarkGray: NSColor.darkGrayColor,
        Gray: NSColor.grayColor,
        Green: NSColor.greenColor,
        LightGray: NSColor.lightGrayColor,
        Magenta: NSColor.magentaColor,
        Orange: NSColor.orangeColor,
        Purple: NSColor.purpleColor,
        Red: NSColor.redColor,
        White: NSColor.whiteColor,
        Yellow: NSColor.yellowColor,
    }[background_color]

######################################################################
# NSCursor.h

NSCursor = ObjCClass('NSCursor')

######################################################################
# NSDocument.h
NSDocument = ObjCClass('NSDocument')

######################################################################
# NSDocumentController.h
NSDocumentController = ObjCClass('NSDocumentController')

######################################################################
# NSEvent.h
NSEvent = ObjCClass('NSEvent')

NSEventPhaseNone = 0
NSEventPhaseBegan = 0x1 << 0
NSEventPhaseStationary = 0x1 << 1
NSEventPhaseChanged = 0x1 << 2
NSEventPhaseEnded = 0x1 << 3
NSEventPhaseCancelled = 0x1 << 4
NSEventPhaseMayBegin = 0x1 << 5

NSAlphaShiftKeyMask = 1 << 16
NSShiftKeyMask = 1 << 17
NSControlKeyMask = 1 << 18
NSAlternateKeyMask = 1 << 19
NSCommandKeyMask = 1 << 20
NSNumericPadKeyMask = 1 << 21
NSHelpKeyMask = 1 << 22
NSFunctionKeyMask = 1 << 23
NSDeviceIndependentModifierFlagsMask = 0xffff0000

NSAnyEventMask = 0xFFFFFFFF  # NSUIntegerMax

NSKeyDown = 10
NSKeyUp = 11
NSFlagsChanged = 12
NSApplicationDefined = 15

NSInsertFunctionKey = 0xF727
NSDeleteFunctionKey = 0xF728
NSHomeFunctionKey = 0xF729
NSBeginFunctionKey = 0xF72A
NSEndFunctionKey = 0xF72B
NSPageUpFunctionKey = 0xF72C
NSPageDownFunctionKey = 0xF72D

######################################################################
# NSFont.h
NSFont = ObjCClass('NSFont')

######################################################################
# NSGraphics.h

NSBackingStoreRetained = 0
NSBackingStoreNonretained = 1
NSBackingStoreBuffered = 2

######################################################################
# NSGraphicsContext.h
NSGraphicsContext = ObjCClass('NSGraphicsContext')

NSImageInterpolationDefault = 0
NSImageInterpolationNone = 1
NSImageInterpolationLow = 2
NSImageInterpolationMedium = 4
NSImageInterpolationHigh = 3

######################################################################
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

######################################################################
# NSImageCell.h

NSImageFrameNone = 0
NSImageFramePhoto = 1
NSImageFrameGrayBezel = 2
NSImageFrameGroove = 3
NSImageFrameButton = 4

######################################################################
# NSImageView.h
NSImageView = ObjCClass('NSImageView')

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


######################################################################
# NSMenu.h
NSMenu = ObjCClass('NSMenu')
NSMenuItem = ObjCClass('NSMenuItem')

######################################################################
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

######################################################################
# NSOpenPanel.h
NSOpenPanel = ObjCClass('NSOpenPanel')

######################################################################
# NSOutlineView.h
NSOutlineView = ObjCClass('NSOutlineView')

######################################################################
# NSPanel.h

NSUtilityWindowMask = 1 << 4

######################################################################
# NSPopUpButton.h
NSPopUpButton = ObjCClass('NSPopUpButton')

######################################################################
# NSProgressIndicator.h
NSProgressIndicator = ObjCClass('NSProgressIndicator')

NSProgressIndicatorBarStyle = 0
NSProgressIndicatorSpinningStyle = 1

######################################################################
# NSRunLoop.h

NSDefaultRunLoopMode = c_void_p.in_dll(appkit, 'NSDefaultRunLoopMode')

######################################################################
# NSRunningApplication.h

NSApplicationActivationPolicyRegular = 0
NSApplicationActivationPolicyAccessory = 1
NSApplicationActivationPolicyProhibited = 2

######################################################################
# NSSavePanel.h
NSSavePanel = ObjCClass('NSSavePanel')

NSFileHandlingPanelOKButton = 1

######################################################################
# NSScreen.h
NSScreen = ObjCClass('NSScreen')

######################################################################
# NSScrollView.h
NSScrollView = ObjCClass('NSScrollView')

NSScrollElasticityAutomatic = 0
NSScrollElasticityNone = 1
NSScrollElasticityAllowed = 2

######################################################################
# NSSecureTextField.h
NSSecureTextField = ObjCClass('NSSecureTextField')

######################################################################
# NSSlider.h
NSSlider = ObjCClass('NSSlider')
NSSliderCell = ObjCClass('NSSliderCell')

######################################################################
# NSSplitView.h
NSSplitView = ObjCClass('NSSplitView')

######################################################################
# NSStepper.h
NSStepper = ObjCClass('NSStepper')

######################################################################
# NSTableView.h
NSTableColumn = ObjCClass('NSTableColumn')
NSTableView = ObjCClass('NSTableView')

NSTableViewNoColumnAutoresizing = 0
NSTableViewUniformColumnAutoresizingStyle = 1
NSTableViewSequentialColumnAutoresizingStyle = 2
NSTableViewReverseSequentialColumnAutoresizingStyle = 3
NSTableViewLastColumnOnlyAutoresizingStyle = 4
NSTableViewFirstColumnOnlyAutoresizingStyle = 5


######################################################################
# NSTabView.h
NSTabView = ObjCClass('NSTabView')
NSTabViewItem = ObjCClass('NSTabViewItem')

######################################################################
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

######################################################################
# NSTextField.h
NSTextField = ObjCClass('NSTextField')
NSTextFieldCell = ObjCClass('NSTextFieldCell')

######################################################################
# NSTextFieldCell.h

NSTextFieldSquareBezel = 0
NSTextFieldRoundedBezel = 1

######################################################################
# NSTextView.h
NSTextView = ObjCClass('NSTextView')

######################################################################
# NSTimer.h
NSTimer = ObjCClass('NSTimer')

######################################################################
# NSToolbar.h
NSToolbar = ObjCClass('NSToolbar')
NSToolbarItem = ObjCClass('NSToolbarItem')

######################################################################
# NSTrackingArea.h
NSTrackingMouseEnteredAndExited = 0x01
NSTrackingMouseMoved = 0x02
NSTrackingCursorUpdate = 0x04
NSTrackingActiveInActiveApp = 0x40

######################################################################
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

######################################################################
# NSWindow.h
NSWindow = ObjCClass('NSWindow')

NSBorderlessWindowMask = 0
NSTitledWindowMask = 1 << 0
NSClosableWindowMask = 1 << 1
NSMiniaturizableWindowMask = 1 << 2
NSResizableWindowMask = 1 << 3

# NSCompositingOperationXXX is equivalent to NSCompositeXXX
NSCompositingOperationClear = 0
NSCompositingOperationCopy = 1
NSCompositingOperationSourceOver = 2
NSCompositingOperationSourceIn = 3
NSCompositingOperationSourceOut = 4
NSCompositingOperationSourceAtop = 5
NSCompositingOperationDestinationOver = 6
NSCompositingOperationDestinationIn = 7
NSCompositingOperationDestinationOut = 8
NSCompositingOperationDestinationAtop = 9
NSCompositingOperationXOR = 10
NSCompositingOperationPlusDarker = 11
NSCompositingOperationHighlight = 12
NSCompositingOperationPlusLighter = 13

NSCompositingOperationMultiply = 14
NSCompositingOperationScreen = 15
NSCompositingOperationOverlay = 16
NSCompositingOperationDarken = 17
NSCompositingOperationLighten = 18
NSCompositingOperationColorDodge = 19
NSCompositingOperationColorBurn = 20
NSCompositingOperationSoftLight = 21
NSCompositingOperationHardLight = 22
NSCompositingOperationDifference = 23
NSCompositingOperationExclusion = 24

NSCompositingOperationHue = 25
NSCompositingOperationSaturation = 26
NSCompositingOperationColor = 27
NSCompositingOperationLuminosity = 28

