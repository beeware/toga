##########################################################################
# System/Library/Frameworks/WebKit.framework
##########################################################################

from enum import IntFlag

from rubicon.objc import ObjCClass, ObjCProtocol
from rubicon.objc.runtime import load_library

######################################################################
webkit = load_library("WebKit")
######################################################################

######################################################################
# WKWebView.h
WKWebView = ObjCClass("WKWebView")

######################################################################
# WKFrameInfo.h
WKUIDelegate = ObjCProtocol("WKUIDelegate")


######################################################################
# WkNavigationDelegate.h
class WKNavigationResponsePolicy(IntFlag):
    Cancel = 0
    Allow = 1
    Download = 2
