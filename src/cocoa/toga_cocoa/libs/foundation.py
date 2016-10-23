from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################

# FOUNDATION

foundation = cdll.LoadLibrary(util.find_library('Foundation'))

foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]


# NSArray.h

NSArray = ObjCClass('NSArray')
NSMutableArray = ObjCClass('NSMutableArray')

# NSBundle.h

NSBundle = ObjCClass('NSBundle')

# NSCursor.h

NSCursor = ObjCClass('NSCursor')

# NSDictionary.h

NSDictionary = ObjCClass('NSDictionary')

# NSDocument.h

NSDocument = ObjCClass('NSDocument')

# NSDocumentController.h

NSDocumentController = ObjCClass('NSDocumentController')

# NSEvent.h

NSAlphaShiftKeyMask = 1 << 16
NSShiftKeyMask = 1 << 17
NSControlKeyMask = 1 << 18
NSAlternateKeyMask = 1 << 19
NSCommandKeyMask = 1 << 20
NSNumericPadKeyMask = 1 << 21
NSHelpKeyMask = 1 << 22
NSFunctionKeyMask = 1 << 23
NSDeviceIndependentModifierFlagsMask = 0xffff0000

# NSFileWrapper.h

NSFileWrapper = ObjCClass('NSFileWrapper')

# NSNumber.h

NSNumber = ObjCClass('NSNumber')

# NSSavePanel.h

NSSavePanel = ObjCClass('NSSavePanel')
NSFileHandlingPanelOKButton = 1

# NSOpenPanel.h

NSOpenPanel = ObjCClass('NSOpenPanel')

# NSScreen.h

NSScreen = ObjCClass('NSScreen')

# NSURL.h

NSURL = ObjCClass('NSURL')

# NSURLRequest.h

NSURLRequest = ObjCClass('NSURLRequest')

# NSFont.h

NSFont = ObjCClass('NSFont')
