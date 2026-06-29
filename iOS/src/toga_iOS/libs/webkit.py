##########################################################################
# System/Library/Frameworks/WebKit.framework
##########################################################################
from ctypes import cdll, util
from enum import IntFlag

from rubicon.objc import ObjCClass, ObjCProtocol

######################################################################
webkit = cdll.LoadLibrary(util.find_library("WebKit"))
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
