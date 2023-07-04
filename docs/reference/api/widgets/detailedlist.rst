DetailedList
============

An ordered list of content where each item has an icon, a main heading, and a line of supplementary text.

.. figure:: /reference/images/DetailedList.png
   :width: 300px
   :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(DetailedList|Component))'}

Usage
-----

A DetailedList uses a :class:`~toga.sources.ListSource` to manage the data being
displayed. options. If ``data`` is not specified as a ListSource, it will be converted
into a ListSource at runtime. Each item in the data source is required to provide 3
values - an icon, a title, and a subtitle.

The simplest instantiation of a DetailedList is to use a list of dictionaries, with
each dictionary containing three keys: ``icon``, ``title``, and ``subtitle``:

.. code-block:: python

    import toga

    table = toga.DetailedList(
        data=[
            {
               "icon": toga.Icon("icons/arthur"),
               "title": "Arthur Dent",
               "subtitle": "Where's the tea?"
            },
            {
               "icon": toga.Icon("icons/ford"),
               "title": "Ford Prefect",
               "subtitle": "Do you know where my towel is?"
            },
            {
               "icon": toga.Icon("icons/tricia"),
               "title": "Tricia McMillan",
               "subtitle": "What planet are you from?"
            },
        ]
    )

If you want to customize the data keys used to provide data, you can do this by
providing an ``accessors`` argument to the DetailedList when it is constructed.
``accessors`` is a tuple, containing the attribute that will be used to provide the
icon, title, and subtitle, respectively:

.. code-block:: python

    import toga

    table = toga.DetailedList(
        accessors=("picture", "name", "quote"),
        data=[
            {
               "picture": toga.Icon("icons/arthur"),
               "name": "Arthur Dent",
               "quote": "Where's the tea?"
            },
            {
               "picture": toga.Icon("icons/ford"),
               "name": "Ford Prefect",
               "quote": "Do you know where my towel is?"
            },
            {
               "picture": toga.Icon("icons/tricia"),
               "name": "Tricia McMillan",
               "quote": "What planet are you from?"
            },
        ]
    )

If the value provided by the accessor for title or subtitle is :any:`None`, or the
accessor isn't defined, the value of ``missing_value`` provided when constructing the
DetailedList will be used to populate the title and subtitle. Any other value will be
converted into a string.

If the value provided by the accessor for icon is :any:`None`, or the accessor isn't
defined, a no icon will be displayed, but space for the icon will remain the the layout.

Reference
---------

.. autoclass:: toga.DetailedList
   :members:
   :undoc-members:
