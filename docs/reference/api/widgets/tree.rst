Tree
====

A widget for displaying a hierarchical tree of tabular data.

.. figure:: /reference/images/Tree.png
   :width: 300px
   :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Tree|Component)$)'}

Usage
-----

A Table uses a :class:`~toga.sources.TreeSource` to manage the data being displayed.
options. If ``data`` is not specified as a TreeSource, it will be converted into a
TreeSource at runtime.


.. code-block:: python

    import toga

    tree = toga.Tree(['Navigate'])

    tree.insert(None, None, 'root1')

    root2 = tree.insert(None, None, 'root2')

    tree.insert(root2, None, 'root2.1')
    root2_2 = tree.insert(root2, None, 'root2.2')

    tree.insert(root2_2, None, 'root2.2.1')
    tree.insert(root2_2, None, 'root2.2.2')
    tree.insert(root2_2, None, 'root2.2.3')

Reference
---------

.. autoclass:: toga.Tree
   :members:
   :undoc-members:
