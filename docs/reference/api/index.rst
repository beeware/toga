.. _api-reference:

==============
API Reference
==============

Core application components
---------------------------

=============================================== ========================
 Component                                       Description
=============================================== ========================
 :doc:`Application </reference/api/app>`         The application itself
 :doc:`Window </reference/api/window>`           Window object
 :doc:`MainWindow </reference/api/mainwindow>`   Main Window
=============================================== ========================

General widgets
---------------

======================================================================= ====================================
 Component                                                               Description
======================================================================= ====================================
 :doc:`ActivityIndicator </reference/api/widgets/activityindicator>`     A (spinning) activity indicator
 :doc:`Button </reference/api/widgets/button>`                           Basic clickable Button
 :doc:`Canvas </reference/api/widgets/canvas>`                           Area you can draw on
 :doc:`DetailedList </reference/api/widgets/detailedlist>`               A list of complex content
 :doc:`Divider </reference/api/widgets/divider>`                         A horizontal or vertical line
 :doc:`ImageView </reference/api/widgets/imageview>`                     Image Viewer
 :doc:`Label </reference/api/widgets/label>`                             Text label
 :doc:`MultilineTextInput </reference/api/widgets/multilinetextinput>`   Multi-line Text Input field
 :doc:`NumberInput </reference/api/widgets/numberinput>`                 Number Input field
 :doc:`PasswordInput </reference/api/widgets/passwordinput>`             A text input that hides it's input
 :doc:`ProgressBar </reference/api/widgets/progressbar>`                 Progress Bar
 :doc:`Selection </reference/api/widgets/selection>`                     Selection
 :doc:`Slider </reference/api/widgets/slider>`                           Slider
 :doc:`Switch </reference/api/widgets/switch>`                           Switch
 :doc:`Table </reference/api/widgets/table>`                             Table of data
 :doc:`TextInput </reference/api/widgets/textinput>`                     Text Input field
 :doc:`Tree </reference/api/widgets/tree>`                               Tree of data
 :doc:`WebView </reference/api/widgets/webview>`                         A panel for displaying HTML
 :doc:`Widget </reference/api/widgets/widget>`                           The base widget
======================================================================= ====================================

Layout widgets
--------------

==================================================================== ==========================
 Usage                                                                Description
==================================================================== ==========================
 :doc:`Box </reference/api/containers/box>`                           Container for components
 :doc:`ScrollContainer </reference/api/containers/scrollcontainer>`   Scrollable Container
 :doc:`SplitContainer </reference/api/containers/splitcontainer>`     Split Container
 :doc:`OptionContainer </reference/api/containers/optioncontainer>`   Option Container
==================================================================== ==========================

Resources
---------

=================================================== =================================
 Component                                           Description
=================================================== =================================
 :doc:`Font </reference/api/resources/fonts>`        Fonts
 :doc:`Command </reference/api/resources/command>`   Command
 :doc:`Group </reference/api/resources/group>`       Command group
 :doc:`Icon </reference/api/resources/icons>`        An icon for buttons, menus, etc
 :doc:`Image </reference/api/resources/images>`      An image
=================================================== =================================

Data Sources
------------

========================================================= =================================
 Component                                                Description
========================================================= =================================
 :doc:`TreeSource </reference/api/sources/tree_source>`   Data source for tree-like data
 :doc:`ListSource </reference/api/sources/table_source>`  Data source for list-like data
 :doc:`Base </reference/api/sources/base>`                Base class for data sources
========================================================= =================================

.. |y| image:: /_static/yes.png
    :width: 16

.. toctree::
   :hidden:

   app
   mainwindow
   window
   containers/index
   resources/index
   sources/index
   widgets/index
