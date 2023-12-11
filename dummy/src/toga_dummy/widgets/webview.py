from toga.widgets.webview import JavaScriptResult

from .base import Widget


class WebView(Widget):
    def create(self):
        self._action("create WebView")

    def set_content(self, root_url, content):
        self._action("set content", root_url=root_url, content=content)

    def get_user_agent(self):
        agent = self._get_value("user_agent")
        return "Toga dummy backend" if agent is None else agent

    def set_user_agent(self, value):
        self._set_value("user_agent", value)

    def get_url(self):
        return self._get_value("url", None)

    def set_url(self, value, future=None):
        self._set_value("url", value)
        self._set_value("loaded_future", future)

    def evaluate_javascript(self, javascript, on_result=None):
        self._action("evaluate_javascript", javascript=javascript)
        self._js_result = JavaScriptResult(on_result)
        return self._js_result

    def simulate_page_loaded(self):
        self.interface.on_webview_load()

        loaded_future = self._get_value("loaded_future", None)
        if loaded_future:
            loaded_future.set_result(None)
            self._set_value("loaded_future", None)

    def simulate_javascript_result(self, value):
        self._js_result.set_result(42)
