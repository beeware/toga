##########################################################################
# System/Library/Frameworks/WebKit.framework
##########################################################################

from rubicon.objc import ObjCClass
from rubicon.objc.runtime import load_library

######################################################################
webkit = load_library("WebKit")
######################################################################

######################################################################
# WebView.h
WebView = ObjCClass("WebView")

######################################################################
# WKWebView.h
WKWebView = ObjCClass("WKWebView")
