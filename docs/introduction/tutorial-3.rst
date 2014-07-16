=====================
Lets build a browser!
=====================

Although it's possible to build complex APIs, it isn't always necessary.
This example builds a simple web browser, in less than 40 lines of code!

    #!/usr/bin/env python
    from __future__ import print_function, unicode_literals, absolute_import

    import toga

    if __name__ == '__main__':
        app = toga.App('Cricket', 'org.pybee.cricket')

        container = toga.Container()

        webview = toga.WebView()
        url_input = toga.TextInput('http://pybee.org/')

        def load_page(widget):
            webview.url = url_input.value

        go_button = toga.Button('Go', on_press=load_page)

        container.add(webview)
        container.add(url_input)
        container.add(go_button)

        container.constrain(url_input.TOP == container.TOP + 5)
        container.constrain(url_input.LEFT == container.LEFT + 5)
        container.constrain(url_input.RIGHT + 5 == go_button.LEFT)

        container.constrain(go_button.TOP == container.TOP + 5)
        container.constrain(go_button.RIGHT + 5 == container.RIGHT)

        container.constrain(webview.TOP == url_input.BOTTOM + 20)
        container.constrain(webview.BOTTOM == container.BOTTOM)
        container.constrain(webview.RIGHT == container.RIGHT)
        container.constrain(webview.LEFT == container.LEFT)

        app.main_window.content = container

        app.main_loop()
