import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleWebView(toga.App):
    async def on_do_async_js(self, widget, **kwargs):
        self.label.text = repr(await self.webview.evaluate_javascript("2 + 2"))

    def on_do_js(self, widget, **kwargs):
        self.webview.evaluate_javascript(
            'document.body.innerHTML = "I can invoke JS. User agent is " + navigator.userAgent;'
        )

    def on_webview_load(self, widget, **kwargs):
        self.label.text = "www loaded!"

    def on_set_url(self, widget, **kwargs):
        self.label.text = "Loading page..."
        self.webview.url = "https://beeware.org/"

    async def on_load_url(self, widget, **kwargs):
        self.label.text = "Loading page..."
        await self.webview.load_url("https://beeware.org/")
        self.label.text = "Page loaded"

    def on_clear_content(self, widget, **kwargs):
        self.webview.url = None

    def on_set_content(self, widget, **kwargs):
        self.webview.set_content(
            "https://example.com",
            "<b>I'm feeling very <span style='background-color: white;'>content</span></b>",
        )

    def on_get_agent(self, widget, **kwargs):
        self.label.text = self.webview.user_agent

    def on_get_url(self, widget, **kwargs):
        self.label.text = self.webview.url

    def on_set_agent(self, widget, **kwargs):
        self.webview.user_agent = "Mr Roboto"

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        self.label = toga.Label("www is loading |", style=Pack(flex=1, padding=5))

        on_set_url_button = toga.Button("set URL", on_press=self.on_set_url)
        on_load_url_button = toga.Button("load URL", on_press=self.on_load_url)
        on_get_url_button = toga.Button("get URL", on_press=self.on_get_url)
        on_do_async_js_button = toga.Button("2 + 2? ", on_press=self.on_do_async_js)
        on_do_js_button = toga.Button("run js", on_press=self.on_do_js)
        on_set_content_button = toga.Button("set content", on_press=self.on_set_content)
        on_clear_content_button = toga.Button(
            "clear content", on_press=self.on_clear_content
        )
        on_set_agent_button = toga.Button("set agent", on_press=self.on_set_agent)
        on_get_agent_button = toga.Button("get agent", on_press=self.on_get_agent)

        button_box = toga.Box(
            children=[
                on_set_url_button,
                on_load_url_button,
                on_get_url_button,
                on_do_async_js_button,
                on_do_js_button,
                on_set_content_button,
                on_clear_content_button,
                on_set_agent_button,
                on_get_agent_button,
            ],
            style=Pack(flex=0, direction=ROW, padding=5),
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
    return ExampleWebView("Toga WebView Demo", "org.beeware.widgets.webview")


if __name__ == "__main__":
    app = main()
    app.main_loop()
