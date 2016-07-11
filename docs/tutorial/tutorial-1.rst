===========================
A slightly less toy example
===========================

Most applications require a little more than a button on a page. Lets
build a slightly more complex example - a Fahrenheit to Celcius converter:

.. image:: screenshots/tutorial-1.png

Here's the source code::

    from __future__ import print_function, unicode_literals, absolute_import

    import toga


    def build(app):
        c_container = toga.Container()
        f_container = toga.Container()
        container = toga.Container()

        c_input = toga.TextInput(readonly=True)
        f_input = toga.TextInput()

        c_label = toga.Label('Celcius', alignment=toga.LEFT_ALIGNED)
        f_label = toga.Label('Fahrenheit', alignment=toga.LEFT_ALIGNED)
        join_label = toga.Label('is equivalent to', alignment=toga.RIGHT_ALIGNED)

        def calculate(widget):
            try:
                c_input.value = (float(f_input.value) - 32.0) * 5.0 / 9.0
            except:
                c_input.value = '???'

        button = toga.Button('Calculate', on_press=calculate)

        f_container.add(f_label)
        f_container.add(f_input)

        c_container.add(join_label)
        c_container.add(c_input)
        c_container.add(c_label)

        container.add(f_container)
        container.add(c_container)
        container.add(button)

        container.style(flex_direction='column', padding_top=10)
        f_container.style(flex_direction='row', margin=5)
        c_container.style(flex_direction='row', margin=5)

        c_input.style(flex=1)
        f_input.style(flex=1, margin_left=160)
        c_label.style(width=100, margin_left=10)
        f_label.style(width=100, margin_left=10)
        join_label.style(width=150, margin_right=10)

        button.style(margin=5)

        return container

    if __name__ == '__main__':
        app = toga.App('Temperature Converter', 'org.pybee.f_to_c', startup=build)

        app.main_loop()


This example shows off the use of Flexbox in Toga's CSS styling. Flexbox is a
new layout scheme that is part of the CSS3 specification that corrects the
problems with the older box layout scheme in CSS2. Flexbox is not yet
universally available in all web browsers,  but that doesn't matter for Toga -
Toga provides an implemention of the Flexbox layout scheme. `CSS-tricks
provides a good tutorial on Flexbox`_ if you've never come across it before.

.. _CSS-tricks provides a good tutorial on Flexbox: https://css-tricks.com/snippets/css/a-guide-to-flexbox/

In this example app, we've set up an outer container that stacks vertically;
inside that container, we've put 2 horizontal containers and a button.

Since there's no width styling on the horizontal containers, they'll try to
fit the widgets the contain into the available space. The ``TextInput``
widgets have a style of ``flex=1``, but the ``Label`` widgets have a fixed
width; as a result, the ``TextInput`` widgets will be stretched to fit the
available horizontal space. The margin and padding terms then ensure that the
widgets will be aligned vertically and horizontally.
