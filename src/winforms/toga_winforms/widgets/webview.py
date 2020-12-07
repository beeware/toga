import sys
import winreg
from os import path
from travertino.size import at_least
from toga_winforms.libs import Uri, WinForms

from .base import Widget


ie_updated = False


def _set_ie_mode():
    """
    By default hosted IE control emulates IE7 regardless which version of IE is installed. To fix this, a proper value
    must be set for the executable.
    See http://msdn.microsoft.com/en-us/library/ee330730%28v=vs.85%29.aspx#browser_emulation for details on this
    behaviour.
    """

    global ie_updated

    if ie_updated:
        return

    executable_name = path.basename(sys.executable)

    def write(key, mode):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0,
                                 winreg.KEY_ALL_ACCESS)
        except WindowsError:
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, key, 0,
                                     winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, executable_name, 0, winreg.REG_DWORD, mode)
        winreg.CloseKey(key)

    # Get the installed version of IE
    ie_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"Software\Microsoft\Internet Explorer")
    try:
        version, type = winreg.QueryValueEx(ie_key, "svcVersion")
    except Exception:
        version, type = winreg.QueryValueEx(ie_key, "Version")

    winreg.CloseKey(ie_key)

    if version.startswith("11"):
        mode = 0x2AF9
    elif version.startswith("10"):
        mode = 0x2711
    elif version.startswith("9"):
        mode = 0x270F
    elif version.startswith("8"):
        mode = 0x22B8
    else:
        mode = 0x2AF9  # Set IE11 as default
    write(
        r'Software\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BROWSER_EMULATION',
        mode)
    write(
        r'Software\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_96DPI_PIXEL',
        mode)

    ie_updated = True


class TogaWebBrowser(WinForms.WebBrowser):
    def __init__(self, interface):
        _set_ie_mode()
        super().__init__()
        self.ScriptErrorsSuppressed = True
        self.DpiAware = True
        self.interface = interface


class WebView(Widget):
    def create(self):
        self.native = TogaWebBrowser(self)

    def set_on_key_down(self, handler):
        pass

    def set_on_webview_load(self, handler):
        pass

    def set_url(self, value):
        if value:
            self.native.Navigate(Uri(self.interface.url), "_self", None,
                                 "User-Agent: %s" % self.interface.user_agent)

    def set_content(self, root_url, content):
        self.native.Url = Uri(root_url)
        self.native.DocumentText = content

    def get_dom(self):
        self.interface.factory.not_implemented('WebView.get_dom()')

    def set_user_agent(self, value):
        user_agent = value if value else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"  # NOQA
        self.native.customUserAgent = user_agent

    async def evaluate_javascript(self, javascript):
        self.interface.factory.not_implemented('WebView.evaluate_javascript()')

    def invoke_javascript(self, javascript):
        self.interface.factory.not_implemented('WebView.invoke_javascript()')

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
