from __future__ import print_function, absolute_import, division

from ctypes import *
from . import constants


_debug_win32 = True

if _debug_win32:
    import traceback
    _GetLastError = windll.kernel32.GetLastError
    _SetLastError = windll.kernel32.SetLastError
    _FormatMessageA = windll.kernel32.FormatMessageA

    _log_win32 = open('debug_win32.log', 'w')

    def format_error(err):
        msg = create_string_buffer(256)
        _FormatMessageA(constants.FORMAT_MESSAGE_FROM_SYSTEM,
                          c_void_p(),
                          err,
                          0,
                          msg,
                          len(msg),
                          c_void_p())
        return msg.value

    class DebugLibrary(object):
        def __init__(self, lib):
            self.lib = lib

        def __getattr__(self, name):
            fn = getattr(self.lib, name)
            def f(*args):
                _SetLastError(0)
                result = fn(*args)
                err = _GetLastError()
                if err != 0:
                    for entry in traceback.format_list(traceback.extract_stack()[:-1]):
                        _log_win32.write(entry)
                    print >> _log_win32, format_error(err)
                return result
            return f
else:
    DebugLibrary = lambda lib: lib

