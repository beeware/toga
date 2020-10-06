##########################################################################
# System/Library/Frameworks/WebKit.framework
##########################################################################
from ctypes import cdll, util

from rubicon.objc import ObjCClass
from rubicon.objc.runtime import load_library

######################################################################
webkit = load_library('WebKit')
######################################################################

######################################################################
# WebView.h
WebView = ObjCClass('WebView')

######################################################################
# WKWebView.h
WKWebView = ObjCClass('WKWebView')
