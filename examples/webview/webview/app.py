import asyncio
import webbrowser

import toga
from toga.constants import COLUMN, ROW


class WebViewApp(toga.App):
    allowed_base_url = "https://beeware.org/"

    async def on_do_async_js(self, widget, **kwargs):
        self.label.text = repr(await self.webview.evaluate_javascript("2 + 2"))

    def on_good_js(self, widget, **kwargs):
        self.webview.evaluate_javascript(
            'document.body.innerHTML = "I can invoke JS. User agent is "'
            "+ navigator.userAgent;"
        )

    async def on_bad_js(self, widget, **kwargs):
        try:
            result = await self.webview.evaluate_javascript("invalid js")
            exception = None
        except Exception as exc:
            result = None
            exception = exc
        self.label.text = f"{result=!r}, {exception=!r}"

    def on_webview_load(self, widget, **kwargs):
        self.label.text = f"Loaded: {widget.url}"
        print(f"on_webview_load: {widget.url}")

    async def on_navigate_js(self, widget, **kwargs):
        await self.webview.evaluate_javascript(
            'window.location.assign("https://github.com/beeware/toga/")'
        )

    def on_navigation_starting_sync(self, widget, url, **kwargs):
        # By default, on_navigation_starting_async is enabled
        # To use this synchronous handler here, make a code edit below where
        # self.webview is created.
        print(f"on_navigation_starting_sync: {url}")
        allow = True
        if not url.startswith(self.allowed_base_url):
            allow = False
            message = f"Navigation not allowed to: {url}"
            dialog = toga.InfoDialog("on_navigation_starting()", message)
            asyncio.create_task(self.dialog(dialog))
        return allow

    async def on_navigation_starting_async(self, widget, url, **kwargs):
        print(f"on_navigation_starting_async: {url}")
        if not url.startswith(self.allowed_base_url):
            message = f"Do you want to allow navigation to: {url}"
            dialog = toga.QuestionDialog("on_navigation_starting_async()", message)
            return await self.main_window.dialog(dialog)
        return True

    def on_set_url(self, widget, **kwargs):
        self.label.text = "Loading page..."
        self.webview.url = "https://beeware.org/"

    async def on_load_url(self, widget, **kwargs):
        self.label.text = "Loading page..."
        await self.webview.load_url("https://beeware.org/")
        self.label.text = "Page loaded"

    def on_clear_url(self, widget, **kwargs):
        self.webview.url = None

    def on_open_browser(self, widget, **kwargs):
        webbrowser.open("https://github.com/beeware/toga")

    def on_set_content(self, widget, **kwargs):
        self.webview.set_content(
            "https://example.com",
            (
                "<b>I'm feeling very "
                "<span style='background-color: white;'>content</span></b>"
            ),
        )

    def on_get_agent(self, widget, **kwargs):
        self.label.text = self.webview.user_agent

    def on_get_url(self, widget, **kwargs):
        self.label.text = self.webview.url

    def on_set_agent(self, widget, **kwargs):
        self.webview.user_agent = "Mr Roboto"

    def startup(self):
        self.main_window = toga.MainWindow()
        self.label = toga.Label("www is loading |", flex=1, margin=5)

        button_box = toga.Box(
            children=[
                toga.Box(
                    direction=ROW,
                    children=[
                        toga.Button("set URL", on_press=self.on_set_url),
                        toga.Button("load URL", on_press=self.on_load_url),
                        toga.Button("clear URL", on_press=self.on_clear_url),
                        toga.Button("get URL", on_press=self.on_get_url),
                        toga.Button("JS navigate", on_press=self.on_navigate_js),
                    ],
                ),
                toga.Box(
                    direction=ROW,
                    children=[
                        toga.Button("2 + 2", on_press=self.on_do_async_js),
                        toga.Button("good js", on_press=self.on_good_js),
                        toga.Button("bad js", on_press=self.on_bad_js),
                        toga.Button("set content", on_press=self.on_set_content),
                    ],
                ),
                toga.Box(
                    direction=ROW,
                    children=[
                        toga.Button("set agent", on_press=self.on_set_agent),
                        toga.Button("get agent", on_press=self.on_get_agent),
                        toga.Button("open browser", on_press=self.on_open_browser),
                    ],
                ),
            ],
            flex=0,
            direction=COLUMN,
            margin=5,
        )

        self.webview = toga.WebView(
            url="https://beeware.org/",
            on_webview_load=self.on_webview_load,
            flex=1,
            on_navigation_starting=self.on_navigation_starting_async,
            # on_navigation_starting=self.on_navigation_starting_sync,
        )

        box = toga.Box(
            children=[
                button_box,
                self.label,
                self.webview,
            ],
            flex=1,
            direction=COLUMN,
        )

        self.main_window.content = box
        self.main_window.show()


def main():
    return WebViewApp("Toga WebView Demo", "org.beeware.toga.examples.webview")


if __name__ == "__main__":
    main().main_loop()
