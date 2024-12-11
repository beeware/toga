import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleWebView(toga.App):
    async def on_do_async_js(self, widget, **kwargs):
        self.label.text = repr(await self.webview.evaluate_javascript("2 + 2"))

    def on_good_js(self, widget, **kwargs):
        self.webview.evaluate_javascript(
            'document.body.innerHTML = "I can invoke JS. User agent is "'
            "+ navigator.userAgent;"
        )

    def on_bad_js(self, widget, **kwargs):
        self.webview.evaluate_javascript("invalid js", on_result=self.on_bad_js_result)

    def on_bad_js_result(self, result, *, exception=None):
        self.label.text = f"{result=!r}, {exception=!r}"

    def on_webview_load(self, widget, **kwargs):
        self.label.text = "www loaded!"

    def on_set_url(self, widget, **kwargs):
        self.label.text = "Loading page..."
        self.webview.url = "https://beeware.org/"

    async def on_load_url(self, widget, **kwargs):
        self.label.text = "Loading page..."
        await self.webview.load_url("https://beeware.org/")
        self.label.text = "Page loaded"

    def on_clear_url(self, widget, **kwargs):
        self.webview.url = None

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
        self.label = toga.Label("www is loading |", style=Pack(flex=1, margin=5))

        button_box = toga.Box(
            children=[
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        toga.Button("set URL", on_press=self.on_set_url),
                        toga.Button("load URL", on_press=self.on_load_url),
                        toga.Button("clear URL", on_press=self.on_clear_url),
                        toga.Button("get URL", on_press=self.on_get_url),
                    ],
                ),
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        toga.Button("2 + 2", on_press=self.on_do_async_js),
                        toga.Button("good js", on_press=self.on_good_js),
                        toga.Button("bad js", on_press=self.on_bad_js),
                        toga.Button("set content", on_press=self.on_set_content),
                    ],
                ),
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        toga.Button("set agent", on_press=self.on_set_agent),
                        toga.Button("get agent", on_press=self.on_get_agent),
                    ],
                ),
            ],
            style=Pack(flex=0, direction=COLUMN, margin=5),
        )

        self.webview = toga.WebView(
            url="https://beeware.org/",
            on_webview_load=self.on_webview_load,
            style=Pack(flex=1),
        )

        box = toga.Box(
            children=[
                button_box,
                self.label,
                self.webview,
            ],
            style=Pack(flex=1, direction=COLUMN),
        )

        self.main_window.content = box
        self.main_window.show()


def main():
    return ExampleWebView("Toga WebView Demo", "org.beeware.toga.examples.webview")


if __name__ == "__main__":
    app = main()
    app.main_loop()
