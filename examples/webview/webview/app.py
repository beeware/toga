import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack


class ExampleWebView(toga.App):
    # This example exercises all the Toga 0.3 WebView methods.
    async def do_math_in_js(self, _widget):
        self.top_label.text = await self.webview.evaluate_javascript("2 + 2")

    def mutate_page(self, _widget):
        innerhtml = "Looks like I can invoke JS. Sincerely, "
        self.webview.invoke_javascript(
            'document.body.innerHTML = ' + '"' + innerhtml + '"'
            + '+ ' + 'navigator.userAgent' ';')

    def on_webview_button_press(self, _whatever, key, modifiers):
        self.top_label.text = "got key={key} mod={modifiers}".format(
            key=key.value,
            modifiers=', '.join(m.value for m in modifiers)
        )

    def on_webview_load(self, _interface):
        self.top_label.text = "www loaded!"

    def set_content(self, _interface):
        self.webview.set_content(
            "https://example.com",
            "<b>I'm feeling very <span style='background-color: white;'>content<span></b>",
        )

    def set_agent(self, _interface):
        self.webview.user_agent = 'Mr Roboto'

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)
        self.top_label = toga.Label('www is loading |', style=Pack(flex=1, padding_left=10))
        self.math_button = toga.Button("2 + 2? ", on_press=self.do_math_in_js)
        self.mutate_page_button = toga.Button("mutate page!", on_press=self.mutate_page)
        self.set_content_button = toga.Button("set content!", on_press=self.set_content)
        self.set_agent_button = toga.Button("set agent!", on_press=self.set_agent)
        self.top_box = toga.Box(
            children=[
                self.math_button,
                self.mutate_page_button,
                self.set_content_button,
                self.set_agent_button,
                self.top_label,
            ],
            style=Pack(flex=0, direction=ROW)
        )
        self.webview = toga.WebView(
            url='https://beeware.org/',
            on_key_down=self.on_webview_button_press,
            on_webview_load=self.on_webview_load,
            style=Pack(flex=1)
        )

        box = toga.Box(
            children=[
                self.top_box,
                self.webview,
            ],
            style=Pack(flex=1, direction=COLUMN)
        )

        self.main_window.content = box
        self.main_window.show()


def main():
    return ExampleWebView('Toga WebView Demo', 'org.beeware.widgets.webview')


if __name__ == '__main__':
    app = main()
    app.main_loop()
