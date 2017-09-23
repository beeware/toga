:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Scroll Container
================

The Scroll Container is similar to the iframe or scrollable div element in HTML, it contains an object with
its own scrollable selection.

.. figure:: /reference/images/ScrollContainer.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga
    
    content = toga.WebView()
    
    container = toga.ScrollContainer(content=content)

Scroll settings
---------------

Horizontal or vertical scroll can be set via the initializer or using the property.

.. code-block:: Python

    import toga
    
    content = toga.WebView()
    
    container = toga.ScrollContainer(content=content, horizontal=False)
    
    container.vertical = False

Supported Platforms
-------------------

.. include:: ../supported_platforms/ScrollContainer.rst

Reference
---------

.. autoclass:: toga.widgets.scrollcontainer.ScrollContainer
   :members:
   :undoc-members:
   :inherited-members: