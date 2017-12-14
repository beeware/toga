===========================
A slightly less toy example
===========================

Most applications require a little more than a button on a page. Lets
build a slightly more complex example - a Fahrenheit to Celsius converter:

.. image:: screenshots/tutorial-1.png

Here's the source code::

.. literalinclude:: /tutorial/source/tutorial-1.py
   :language: python

This example shows off the use of Flexbox in Toga's CSS styling. Flexbox is a
new layout scheme that is part of the CSS3 specification that corrects the
problems with the older box layout scheme in CSS2. Flexbox is not yet
universally available in all web browsers,  but that doesn't matter for Toga -
Toga provides an implementation of the Flexbox layout scheme. `CSS-tricks
provides a good tutorial on Flexbox`_ if you've never come across it before.

.. _CSS-tricks provides a good tutorial on Flexbox: https://css-tricks.com/snippets/css/a-guide-to-flexbox/

In this example app, we've set up an outer box that stacks vertically;
inside that box, we've put 2 horizontal boxes and a button.

Since there's no width styling on the horizontal boxes, they'll try to
fit the widgets they contain into the available space. The ``TextInput``
widgets have a style of ``flex=1``, but the ``Label`` widgets have a fixed
width; as a result, the ``TextInput`` widgets will be stretched to fit the
available horizontal space. The margin and padding terms then ensure that the
widgets will be aligned vertically and horizontally.
