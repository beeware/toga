from ctypes import *
from ctypes import util


from rubicon.objc import *

######################################################################

# FOUNDATION

foundation = cdll.LoadLibrary(util.find_library('Foundation'))

foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]


# NSArray.h

NSMutableArray = ObjCClass('NSMutableArray')

# NSData.h

NSData = ObjCClass('NSData')

# NSURL.h

NSURL = ObjCClass('NSURL')

# NSURLRequest.h

NSURLRequest = ObjCClass('NSURLRequest')

# UIFont.h

UIFont = ObjCClass('UIFont')
