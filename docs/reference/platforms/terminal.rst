========
Terminal
========

.. .. image:: /reference/screenshots/terminal.png
..    :align: center
..    :width: 300

The Toga backend for terminal applications is `toga-textual
<https://github.com/beeware/toga/tree/main/textual>`__.

Prerequisites
-------------

``toga-textual`` should run on any terminal or command shell provided by macOS, Windows
or Linux.

Installation
------------

``toga-textual`` must be manually installed by running:

.. code-block:: console

    $ python -m pip install toga-textual

If ``toga-textual`` is the only Toga backend that is installed, it will be picked up
automatically on any desktop operating system. If you have another backend installed
(usually, this will be the default GUI for your operating system), you will need to set
the ``TOGA_BACKEND`` environment variable to ``toga-textual`` to force the selection of
the backend.

Implementation details
----------------------

``toga-textual`` uses the `Textual <https://textual.textualize.io>`__ UI toolkit.

macOS Terminal.app limitations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are some `known issues with the default macOS Terminal.app
<https://github.com/Textualize/textual/blob/main/FAQ.md#why-doesnt-textual-look-good-on-macos>`__.
In some layouts, box outlines render badly; this can *sometimes* be resolved by altering
the line spacing of the font used in the terminal. The default Terminal.app also has a
limited color palette. The maintainers of Textual recommend using an alternative
terminal application to avoid these problems.
