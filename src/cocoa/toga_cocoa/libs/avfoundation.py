##########################################################################
# System/Library/Frameworks/AVFoundation.framework
##########################################################################
from ctypes import cdll
from ctypes import util

from rubicon.objc import ObjCClass

######################################################################
avfoundation = cdll.LoadLibrary(util.find_library('AVFoundation'))
######################################################################

######################################################################
# NSBundle.h
AVMIDIPlayer = ObjCClass('AVMIDIPlayer')
