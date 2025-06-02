from toga_cocoa.libs import WKWebView

from .base import SimpleProbe


class WebViewProbe(SimpleProbe):
    native_class = WKWebView
    content_supports_url = True
    javascript_supports_exception = True
    supports_on_load = True

    def extract_cookie(self, cookie_jar, name):
        return next((c for c in cookie_jar if c.name == name), None)

    async def simulate_webview_file_upload_dialog_result(
        self, widget, multiple_select, webkitdirectory, result
    ):
        if result is not None:
            # TODO: Implement simulating the actual file selection and upload (how?)
            # if multiple_select:
            #     simulate selecting :param: result
            # else:
            #     simulate selecting :param: result
            try:
                # simulate pressing "enter" to upload selected files to the DOM
                await self.type_character("<enter>")
            except Exception:
                # if error, return false to signal the test failed
                # workaround until file upload is fully simulated
                return False
            # return true to signal that there was no error and the test passed
            # workaround until file upload is fully simulated
            return True
        else:
            try:
                # simulate pressing "escape" to cancel the upload file dialog
                await self.type_character("<esc>")
            except Exception:
                # if error, return false to signal the test failed
                # workaround until file upload is fully simulated
                return False
            # return true to signal that there was no error and the test passed
            # workaround until file upload is fully simulated
            return True
