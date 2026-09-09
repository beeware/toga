########################################################################################
# NativeApp is derived from Yukihiro Nakadaira's XamlApplication:
# github.com/ynkdir/py-win32more/blob/main/packages/appsdk/src/win32more/winui3/__init__.py  # noqa: E501
#
# ======================================================================================
#
# MIT License
#
# Copyright (c) 2022 Yukihiro Nakadaira
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ======================================================================================
#
########################################################################################

from __future__ import annotations

from win32more import FAILED, WinError
from win32more.Microsoft.UI.Xaml import Application, Window
from win32more.Windows.Win32.System.Com import (
    COINIT_APARTMENTTHREADED,
    CoInitializeEx,
    CoUninitialize,
)
from win32more.winui3 import XamlApplication

from .nativeevents import events_handled


class NativeApp(XamlApplication):
    def CreateWindow(self):
        return events_handled(Window)

    @classmethod
    def Start(cls):

        hr = CoInitializeEx(None, COINIT_APARTMENTTHREADED)
        if FAILED(hr):  # pragma: no cover
            raise WinError(hr)

        def ApplicationInitializationCallback(*_args):
            return cls()

        Application.Start(ApplicationInitializationCallback)

        # This line occurs after shutdown, which can't be covered by the testbed.
        CoUninitialize()  # pragma: no cover
