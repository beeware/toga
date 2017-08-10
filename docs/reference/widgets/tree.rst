:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Tree
====

The tree widget is still under development.

Usage
-----

.. code-block:: Python

    import toga

    tree = toga.Tree(['Navigate'])

    tree.insert(None, None, 'root1')

    root2 = tree.insert(None, None, 'root2')

    tree.insert(root2, None, 'root2.1')
    root2_2 = tree.insert(root2, None, 'root2.2')

    tree.insert(root2_2, None, 'root2.2.1')
    tree.insert(root2_2, None, 'root2.2.2')
    tree.insert(root2_2, None, 'root2.2.3')


Supported Platforms
-------------------

.. include:: ../supported_platforms/Tree.rst

Reference
---------

.. autoclass:: toga.widgets.tree.Tree
   :members:
   :undoc-members:
   :inherited-members: