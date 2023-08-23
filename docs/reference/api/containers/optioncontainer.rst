OptionContainer
===============

A container that can display multiple labeled tabs of content.

.. figure:: /reference/images/OptionContainer.png
    :align: center
    :width: 300px

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(OptionContainer|Component))'}


Usage
-----

.. code-block:: python

    import toga

    pizza = toga.Box()
    pasta = toga.Box()

    container = toga.OptionContainer(
        content=[("Pizza", pizza), ("Pasta", pasta)]
    )

    # Add another tab of content
    salad = toga.Box()
    container.content.append("Salad", salad)

When retrieving or deleting items, or when specifying the
currently selected item, you can specify an item using:

* The index of the item in the list of content:

  .. code-block:: python

      # Insert a new second tab
      container.content.insert(1, "Soup", toga.Box())
      # Make the third tab the currently active tab
      container.current_tab = 2
      # Delete the second tab
      del container.content[1]

* The string label of the tab:

  .. code-block:: python

      # Insert a tab at the index currently occupied by a tab labeled "Pasta"
      container.content.insert("Pasta", "Soup", toga.Box())
      # Make the tab labeled "Pasta" the currently active tab
      container.current_tab = "Pasta"
      # Delete tab labeled "Pasta"
      del container.content["Pasta"]

* A reference to an :any:`OptionItem`:

  .. code-block:: python

      # Get a reference to the "Pasta" tab
      pasta_tab = container.content["Pasta"]
      # Insert content at the index currently occupied by the pasta tab
      container.content.insert(pasta_tab, "Soup", toga.Box())
      # Make the pasta tab the currently active tab
      container.current_tab = pasta_tab
      # Delete the pasta tab
      del container.content[pasta_tab]

Reference
---------

.. autoclass:: toga.OptionContainer
   :exclude-members: app, window

.. autoclass:: toga.widgets.optioncontainer.OptionList
    :special-members: __getitem__, __delitem__

.. autoclass:: toga.widgets.optioncontainer.OptionItem
