======================
Let's build a browser!
======================

Although it's possible to build complex GUI layouts, you can get a lot
of functionality with very little code, utilizing the rich components that
are native on modern platforms.

So - lets build a tool that lets our pet yak graze the web - a primitive
web browser, in less than 40 lines of code!

.. image:: screenshots/tutorial-3.png

Here's the source code::

    #!/usr/bin/env python
    from __future__ import print_function, unicode_literals, absolute_import

    import toga
    from colosseum import CSS



    class Graze(toga.App):
        def startup(self):

            self.webview = toga.WebView(style=CSS(flex=1))
            self.url_input = toga.TextInput('http://pybee.org/', style=CSS(flex=1, margin=5))

            container = toga.Container(
                toga.Container(
                    self.url_input,
                    toga.Button('Go', on_press=self.load_page, width=50),
                    style=CSS(
                        flex_direction='row'
                    )
                ),
                self.webview,
                style=CSS(
                    flex_direction='column'
                )
            )

            self.main_window.content = container

        def load_page(self, widget):
            self.webview.url = self.url_input.value

    if __name__ == '__main__':
        app = Graze('Graze', 'org.pybee.graze')

        app.main_loop()

In this example, you can see an application being developed as a class, rather
than as a build method. You can also see containers defined in a declarative
manner - if you don't need to retain a reference to a particular widget, you
can define a widget inline, and pass it as an argument to a container, and it
will become a child of that container.
