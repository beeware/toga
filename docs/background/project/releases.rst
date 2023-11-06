:tocdepth: 2

===============
Release History
===============

.. towncrier release notes start

0.4.0 (2023-11-03)
==================

Features
--------

* The Toga API has been fully audited. All APIs now have 100% test coverage, complete API documentation (including type annotations), and are internally consistent. ( `#1903 <https://github.com/beeware/toga/issues/1903>`__, `#1938 <https://github.com/beeware/toga/issues/1938>`__, `#1944 <https://github.com/beeware/toga/issues/1944>`__, `#1946 <https://github.com/beeware/toga/issues/1946>`__, `#1949 <https://github.com/beeware/toga/issues/1949>`__, `#1951 <https://github.com/beeware/toga/issues/1951>`__, `#1955 <https://github.com/beeware/toga/issues/1955>`__, `#1956 <https://github.com/beeware/toga/issues/1956>`__, `#1964 <https://github.com/beeware/toga/issues/1964>`__, `#1969 <https://github.com/beeware/toga/issues/1969>`__, `#1984 <https://github.com/beeware/toga/issues/1984>`__, `#1996 <https://github.com/beeware/toga/issues/1996>`__, `#2011 <https://github.com/beeware/toga/issues/2011>`__, `#2017 <https://github.com/beeware/toga/issues/2017>`__, `#2025 <https://github.com/beeware/toga/issues/2025>`__, `#2029 <https://github.com/beeware/toga/issues/2029>`__, `#2044 <https://github.com/beeware/toga/issues/2044>`__, `#2058 <https://github.com/beeware/toga/issues/2058>`__, `#2075 <https://github.com/beeware/toga/issues/2075>`__)
* Headings are no longer mandatory for Tree widgets. If headings are not provided, the widget will not display its header bar. (`#1767 <https://github.com/beeware/toga/issues/1767>`__)
* Support for custom font loading was added to the GTK, Cocoa and iOS backends. (`#1837 <https://github.com/beeware/toga/issues/1837>`__)
* The testbed app has better diagnostic output when running in test mode. (`#1847 <https://github.com/beeware/toga/issues/1847>`__)
* A Textual backend was added to support terminal applications. (`#1867 <https://github.com/beeware/toga/issues/1867>`__)
* Support for determining the currently active window was added to Winforms. (`#1872 <https://github.com/beeware/toga/issues/1872>`__)
* Programmatically scrolling to top and bottom in MultilineTextInput is now possible on iOS. (`#1876 <https://github.com/beeware/toga/issues/1876>`__)
* A handler has been added for users confirming the contents of a TextInput by pressing Enter/Return. (`#1880 <https://github.com/beeware/toga/issues/1880>`__)
* An API for giving a window focus was added. (`#1887 <https://github.com/beeware/toga/issues/1887>`__)
* Widgets now have a ``.clear()`` method to remove all child widgets. (`#1893 <https://github.com/beeware/toga/issues/1893>`__)
* Winforms now supports hiding and re-showing the app cursor. (`#1894 <https://github.com/beeware/toga/issues/1894>`__)
* ProgressBar and Switch widgets were added to the Web backend. (`#1901 <https://github.com/beeware/toga/issues/1901>`__)
* Missing value handling was added to the Tree widget. (`#1913 <https://github.com/beeware/toga/issues/1913>`__)
* App paths now include a ``config`` path for storing configuration files. (`#1964 <https://github.com/beeware/toga/issues/1964>`__)
* A more informative error message is returned when a platform backend doesn't support a widget. (`#1992 <https://github.com/beeware/toga/issues/1992>`__)
* The example apps were updated to support being run with ``briefcase run`` on all platforms. (`#1995 <https://github.com/beeware/toga/issues/1995>`__)
* Headings are no longer mandatory Table widgets. (`#2011 <https://github.com/beeware/toga/issues/2011>`__)
* Columns can now be added and removed from a Tree. (`#2017 <https://github.com/beeware/toga/issues/2017>`__)
* The default system notification sound can be played via ``App.beep()``. (`#2018 <https://github.com/beeware/toga/issues/2018>`__)
* DetailedList can now respond to "primary" and "secondary" user actions. These may be implemented as left and right swipe respectively, or using any other platform-appropriate mechanism. (`#2025 <https://github.com/beeware/toga/issues/2025>`__)
* A DetailedList can now provide a value to use when a row doesn't provide the required data. (`#2025 <https://github.com/beeware/toga/issues/2025>`__)
* The accessors used to populate a DetailedList can now be customized. (`#2025 <https://github.com/beeware/toga/issues/2025>`__)
* Transformations can now be applied to *any* canvas context, not just the root context. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* Canvas now provides more ``list``-like methods for manipulating drawing objects in a context. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* On Windows, the default font now follows the system theme. On most devices, this means it has changed from Microsoft Sans Serif 8pt to Segoe UI 9pt. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* Font sizes are now consistently interpreted as CSS points. On Android, iOS and macOS, this means any numeric font sizes will appear 33% larger than before. The default font size on these platforms is unchanged. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* MultilineTextInputs no longer show spelling suggestions when in read-only mode. (`#2136 <https://github.com/beeware/toga/issues/2136>`__)
* Applications now verify that a main window has been created as part of the ``startup()`` method. (`#2047 <https://github.com/beeware/toga/issues/2047>`__)
* An implementation of ActivityIndicator was added to the Web backend. (`#2050 <https://github.com/beeware/toga/issues/2050>`__)
* An implementation of Divider was added to the Web backend. (`#2051 <https://github.com/beeware/toga/issues/2051>`__)
* The ability to capture the contents of a window as an image has been added. (`#2063 <https://github.com/beeware/toga/issues/2063>`__)
* A PasswordInput widget was added to the Web backend. (`#2089 <https://github.com/beeware/toga/issues/2089>`__)
* The WebKit inspector is automatically enabled on all macOS WebViews, provided you're using macOS 13.3 (Ventura) or iOS 16.4, or later. (`#2109 <https://github.com/beeware/toga/issues/2109>`__)
* Text input widgets on macOS now support undo and redo. (`#2151 <https://github.com/beeware/toga/issues/2151>`__)
* The Divider widget was implemented on Android. (`#2181 <https://github.com/beeware/toga/issues/2181>`__)

Bugfixes
--------

* The WinForms event loop was decoupled from the main form, allowing background tasks to run without a main window being present. (`#750 <https://github.com/beeware/toga/issues/750>`__)
* Widgets are now removed from windows when the window is closed, preventing a memory leak on window closure. (`#1215 <https://github.com/beeware/toga/issues/1215>`__)
* Android and iOS apps no longer crash if you invoke ``App.hide_cursor()`` or ``App.show_cursor()``. (`#1235 <https://github.com/beeware/toga/issues/1235>`__)
* A Selection widget with no items now consistently returns a selected value of ``None`` on all platforms. (`#1723 <https://github.com/beeware/toga/issues/1723>`__)
* macOS widget methods that return strings are now guaranteed to return strings, rather than native Objective C string objects. (`#1779 <https://github.com/beeware/toga/issues/1779>`__)
* WebViews on Windows no longer have a black background when they are resized. (`#1855 <https://github.com/beeware/toga/issues/1855>`__)
* The interpretation of ``MultilineTextInput.readonly`` was corrected iOS (`#1866 <https://github.com/beeware/toga/issues/1866>`__)
* A window without an ``on_close`` handler can now be closed using the window frame close button. (`#1872 <https://github.com/beeware/toga/issues/1872>`__)
* Android apps running on devices older than API level 29 (Android 10) no longer crash. (`#1878 <https://github.com/beeware/toga/issues/1878>`__)
* Missing value handling on Tables was fixed on Android and Linux. (`#1879 <https://github.com/beeware/toga/issues/1879>`__)
* The GTK backend is now able to correctly identify the currently active window. (`#1892 <https://github.com/beeware/toga/issues/1892>`__)
* Error handling associated with the creation of Intents on Android has been improved. (`#1909 <https://github.com/beeware/toga/issues/1909>`__)
* The DetailedList widget on GTK now provides an accurate size hint during layout. (`#1920 <https://github.com/beeware/toga/issues/1920>`__)
* Apps on Linux no longer segfault if an X Windows display cannot be identified. (`#1921 <https://github.com/beeware/toga/issues/1921>`__)
* The ``on_result`` handler is now used by Cocoa file dialogs. (`#1947 <https://github.com/beeware/toga/issues/1947>`__)
* Pack layout now honors an explicit width/height setting of 0. (`#1958 <https://github.com/beeware/toga/issues/1958>`__)
* The minimum window size is now correctly recomputed and enforced if window content changes. (`#2020 <https://github.com/beeware/toga/issues/2020>`__)
* The title of windows can now be modified on Winforms. (`#2094 <https://github.com/beeware/toga/issues/2094>`__)
* An error on Winforms when a window has no content has been resolved. (`#2095 <https://github.com/beeware/toga/issues/2095>`__)
* iOS container views are now set to automatically resize with their parent view (`#2161 <https://github.com/beeware/toga/issues/2161>`__)

Backward Incompatible Changes
-----------------------------

* The ``weight``, ``style`` and ``variant`` arguments for ``Font`` and ``Font.register`` are now keyword-only. (`#1903 <https://github.com/beeware/toga/issues/1903>`__)
* The ``clear()`` method for resetting the value of a MultilineTextInput, TextInput and PasswordInput has been removed. This method was an ambiguous override of the ``clear()`` method on Widget that removed all child nodes. To remove all content from a text input widget, use ``widget.value = ""``. (`#1938 <https://github.com/beeware/toga/issues/1938>`__)
* The ability to perform multiple substring matches in a ``Contains`` validator has been removed. (`#1944 <https://github.com/beeware/toga/issues/1944>`__)
* The ``TextInput.validate`` method has been removed. Validation now happens automatically whenever the ``value`` or ``validators`` properties are changed. (`#1944 <https://github.com/beeware/toga/issues/1944>`__)
* The argument names used to construct validators have changed. Error message arguments now all end with ``_message``; ``compare_count`` has been renamed ``count``; and ``min_value`` and ``max_value`` have been renamed ``min_length`` and ``max_length``, respectively. (`#1944 <https://github.com/beeware/toga/issues/1944>`__)
* The ``get_dom()`` method on WebView has been removed. This method wasn't implemented on most platforms, and wasn't working on any of the platforms where it *was* implemented, as modern web view implementations don't provide a synchronous API for accessing web content in this way. (`#1949 <https://github.com/beeware/toga/issues/1949>`__)
* The ``evaluate_javascript()`` method on WebView has been modified to work in both synchronous and asynchronous contexts. In a synchronous context you can invoke the method and use a functional ``on_result`` callback to be notified when evaluation is complete. In an asynchronous context, you can await the result. (`#1949 <https://github.com/beeware/toga/issues/1949>`__)
* The ``on_key_down`` handler has been removed from WebView. If you need to catch user input, either use a handler in the embedded JavaScript, or create a ``Command`` with a key shortcut. (`#1949 <https://github.com/beeware/toga/issues/1949>`__)
* The ``invoke_javascript()`` method has been removed. All usage of ``invoke_javascript()`` can be replaced with ``evaluate_javascript()``. (`#1949 <https://github.com/beeware/toga/issues/1949>`__)
* The usage of local ``file://`` URLs has been explicitly prohibited. ``file://`` URLs have not been reliable for some time; their usage is now explicitly prohibited. (`#1949 <https://github.com/beeware/toga/issues/1949>`__)
* ``DatePicker`` has been renamed ``DateInput``. (`#1951 <https://github.com/beeware/toga/issues/1951>`__)
* ``TimePicker`` has been renamed ``TimeInput``. (`#1951 <https://github.com/beeware/toga/issues/1951>`__)
* The ``on_select`` handler on the Selection widget has been renamed ``on_change`` for consistency with other widgets. (`#1955 <https://github.com/beeware/toga/issues/1955>`__)
* The ``_notify()`` method on data sources has been renamed ``notify()``, reflecting its status as a public API. (`#1955 <https://github.com/beeware/toga/issues/1955>`__)
* The ``prepend()`` method was removed from the ``ListSource`` and ``TreeSource`` APIs. Calls to ``prepend(...)`` can be replaced with ``insert(0, ...)``. (`#1955 <https://github.com/beeware/toga/issues/1955>`__)
* The ``insert()`` and ``append()`` APIs on ``ListSource`` and ``TreeSource`` have been modified to provide an interface that is closer to that ``list`` API. These methods previously accepted a variable list of positional and keyword arguments; these arguments should be combined into a single tuple or dictionary. This matches the API provided by ``__setitem__()``. (`#1955 <https://github.com/beeware/toga/issues/1955>`__)
* Images and ImageViews no longer support loading images from URLs. If you need to display an image from a URL, use a background task to obtain the image data asynchronously, then create the Image and/or set the ImageView ``image`` property on the completion of the asynchronous load. (`#1956 <https://github.com/beeware/toga/issues/1956>`__)
* A row box contained inside a row box will now expand to the full height of its parent, rather than collapsing to the maximum height of the inner box's child content. (`#1958 <https://github.com/beeware/toga/issues/1958>`__)
* A column box contained inside a column box will now expand to the full width of its parent, rather than collapsing to the maximum width of the inner box's child content. (`#1958 <https://github.com/beeware/toga/issues/1958>`__)
* On Android, the user data folder is now a ``data`` sub-directory of the location returned by ``context.getFilesDir()``, rather than the bare ``context.getFilesDir()`` location. (`#1964 <https://github.com/beeware/toga/issues/1964>`__)
* GTK now returns ``~/.local/state/appname/log`` as the log file location, rather than ``~/.cache/appname/log``. (`#1964 <https://github.com/beeware/toga/issues/1964>`__)
* The location returned by ``toga.App.paths.app`` is now the folder that contains the Python source file that defines the app class used by the app. If you are using a ``toga.App`` instance directly, this may alter the path that is returned. (`#1964 <https://github.com/beeware/toga/issues/1964>`__)
* On Winforms, if an application doesn't define an author, an author of ``Unknown`` is now used in application data paths, rather than ``Toga``. (`#1964 <https://github.com/beeware/toga/issues/1964>`__)
* Winforms now returns ``%USERPROFILE%/AppData/Local/<Author Name>/<App Name>/Data`` as the user data file location, rather than ``%USERPROFILE%/AppData/Local/<Author Name>/<App Name>``. (`#1964 <https://github.com/beeware/toga/issues/1964>`__)
* Support for SplitContainers with more than 2 panels of content has been removed. (`#1984 <https://github.com/beeware/toga/issues/1984>`__)
* Support for 3-tuple form of specifying SplitContainer items, used to prevent panels from resizing, has been removed. (`#1984 <https://github.com/beeware/toga/issues/1984>`__)
* The ability to increment and decrement the current OptionContainer tab was removed. Instead of `container.current_tab += 1`, use `container.current_tab = container.current_tab.index + 1` (`#1996 <https://github.com/beeware/toga/issues/1996>`__)
* ``OptionContainer.add()``, ``OptionContainer.remove()`` and ``OptionContainer.insert()`` have been removed, due to being ambiguous with base widget methods of the same name. Use the ``OptionContainer.content.append()``, ``OptionContainer.content.remove()`` and ``OptionContainer.content.insert()`` APIs instead. (`#1996 <https://github.com/beeware/toga/issues/1996>`__)
* The ``on_select`` handler for OptionContainer no longer receives the ``option`` argument providing the selected tab. Use ``current_tab`` to obtain the currently selected tab. (`#1996 <https://github.com/beeware/toga/issues/1996>`__)
* ``TimePicker.min_time`` and ``TimePicker.max_time`` has been renamed ``TimeInput.min`` and ``TimeInput.max``, respectively. (`#1999 <https://github.com/beeware/toga/issues/1999>`__)
* ``DatePicker.min_date`` and ``DatePicker.max_date`` has been renamed ``DateInput.min`` and ``DateInput.max``, respectively. (`#1999 <https://github.com/beeware/toga/issues/1999>`__)
* ``NumberInput.min_value`` and ``NumberInput.max_value`` have been renamed ``NumberInput.min`` and ``NumberInput.max``, respectively. (`#1999 <https://github.com/beeware/toga/issues/1999>`__)
* ``Slider.range`` has been replaced by ``Slider.min`` and ``Slider.max``. (`#1999 <https://github.com/beeware/toga/issues/1999>`__)
* Tables now use an empty string for the default missing value, rather than warning about missing values. (`#2011 <https://github.com/beeware/toga/issues/2011>`__)
* ``Table.add_column()`` has been deprecated in favor of ``Table.append_column()`` and ``Table.insert_column()`` (`#2011 <https://github.com/beeware/toga/issues/2011>`__)
* ``Table.on_double_click`` has been renamed ``Table.on_activate``. (`#2011 <https://github.com/beeware/toga/issues/2011>`__, `#2017 <https://github.com/beeware/toga/issues/2017>`__)
* Trees now use an empty string for the default missing value, rather than warning about missing values. (`#2017 <https://github.com/beeware/toga/issues/2017>`__)
* The ``parent`` argument has been removed from the ``insert`` and ``append`` calls on ``TreeSource``. This improves consistency between the API for ``TreeSource`` and the API for ``list``. To insert or append a row in to a descendant of a TreeSource root, use ``insert`` and ``append`` on the parent node itself - i.e., ``source.insert(parent, index, ...)`` becomes ``parent.insert(index, ...)``, and ``source.insert(None, index, ...)`` becomes ``source.insert(index, ...)``. (`#2017 <https://github.com/beeware/toga/issues/2017>`__)
* When constructing a DetailedList from a list of tuples, or a list of lists, the required order of values has changed from (icon, title, subtitle) to (title, subtitle, icon). (`#2025 <https://github.com/beeware/toga/issues/2025>`__)
* The ``on_select`` handler for DetailedList no longer receives the selected row as an argument. (`#2025 <https://github.com/beeware/toga/issues/2025>`__)
* The handling of row deletion in DetailedList widgets has been significantly altered. The ``on_delete`` event handler has been renamed ``on_primary_action``, and is now *only* a notification that a "swipe left" event (or platform equivalent) has been confirmed. This was previously inconsistent across platforms. Some platforms would update the data source to remove the row; some treated ``on_delete`` as a notification event and expected the application to handle the deletion. It is now the application's responsibility to perform the data deletion. (`#2025 <https://github.com/beeware/toga/issues/2025>`__)
* Support for Python 3.7 was removed. (`#2027 <https://github.com/beeware/toga/issues/2027>`__)
* ``fill()`` and ``stroke()`` now return simple drawing operations, rather than context managers. If you attempt to use ``fill()`` or ``stroke()`` on a context as a context manager, an exception will be raised; using these methods on Canvas will raise a warning, but return the appropriate context manager. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* The ``clicks`` argument to ``Canvas.on_press`` has been removed. Instead, to detect "double clicks", you should use ``Canvas.on_activate``. The ``clicks`` argument has also been removed from ``Canvas.on_release``, ``Canvas.on_drag``, ``Canvas.on_alt_press``, ``Canvas.on_alt_release``, and ``Canvas.on_alt_drag``. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* The ``new_path`` operation has been renamed ``begin_path`` for consistency with the HTML5 Canvas API. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* Methods that generate new contexts have been renamed: ``context()``, ``closed_path()``, ``fill()`` and ``stroke()`` have become ``Context()``, ``ClosedPath()``, ``Fill()`` and ``Stroke()`` respectively. This has been done to make it easier to differentiate between primitive drawing operations and context-generating operations. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* A Canvas is no longer implicitly a context object. The ``Canvas.context`` property now returns the root context of the canvas. If you were previously using ``Canvas.context()`` to generate an empty context, it should be replaced with ``Canvas.Context()``. Any operations to ``remove()`` drawing objects from the canvas or ``clear()`` the canvas of drawing objects should be made on ``Canvas.context``. Invoking these methods on ``Canvas`` will now call the base ``Widget`` implementations, which will throw an exception because ``Canvas`` widgets cannot have children. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* The ``preserve`` option on ``Fill()`` operations has been deprecated. It was required for an internal optimization and can be safely removed without impact. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* Drawing operations (e.g., ``arc``, ``line_to``, etc) can no longer be invoked directly on a Canvas. Instead, they should be invoked on the root context of the canvas, retrieved with via the `canvas` property. Context creating operations (``Fill``, ``Stroke`` and ``ClosedPath``) are not affected. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* The ``tight`` argument to ``Canvas.measure_text()`` has been deprecated. It was a GTK implementation detail, and can be safely removed without impact. (`#2029 <https://github.com/beeware/toga/issues/2029>`__)
* The ``multiselect`` argument to Open File and Select Folder dialogs has been renamed ``multiple_select``, for consistency with other widgets that have multiple selection capability. (`#2058 <https://github.com/beeware/toga/issues/2058>`__)
* ``Window.resizeable`` and ``Window.closeable`` have been renamed ``Window.resizable`` and ``Window.closable``, to adhere to US spelling conventions. (`#2058 <https://github.com/beeware/toga/issues/2058>`__)
* Windows no longer need to be explicitly added to the app's window list. When a window is created, it will be automatically added to the windows for the currently running app. (`#2058 <https://github.com/beeware/toga/issues/2058>`__)
* The optional arguments of ``Command`` and ``Group`` are now keyword-only. (`#2075 <https://github.com/beeware/toga/issues/2075>`__)
* In ``App``, the properties ``id`` and ``name`` have been deprecated in favor of ``app_id`` and ``formal_name`` respectively, and the property ``module_name`` has been removed. (`#2075 <https://github.com/beeware/toga/issues/2075>`__)
* ``GROUP_BREAK``, ``SECTION_BREAK`` and ``CommandSet`` were removed from the ``toga`` namespace. End users generally shouldn't need to use these classes. If your code *does* need them for some reason, you can access them from the ``toga.command`` namespace. (`#2075 <https://github.com/beeware/toga/issues/2075>`__)
* The ``windows`` constructor argument of ``toga.App`` has been removed. Windows are now automatically added to the current app. (`#2075 <https://github.com/beeware/toga/issues/2075>`__)
* The ``filename`` argument and property of ``toga.Document`` has been renamed ``path``, and is now guaranteed to be a ``pathlib.Path`` object. (`#2075 <https://github.com/beeware/toga/issues/2075>`__)
* Documents must now provide a ``create()`` method to instantiate a ``main_window`` instance. (`#2075 <https://github.com/beeware/toga/issues/2075>`__)
* ``App.exit()`` now unconditionally exits the app, rather than confirming that the ``on_exit`` handler will permit the exit. (`#2075 <https://github.com/beeware/toga/issues/2075>`__)

Documentation
-------------

* Documentation for application paths was added. (`#1849 <https://github.com/beeware/toga/issues/1849>`__)
* The contribution guide was expanded to include more suggestions for potential projects, and to explain how the backend tests work. (`#1868 <https://github.com/beeware/toga/issues/1868>`__)
* All code blocks were updated to add a button to copy the relevant contents on to the user's clipboard. (`#1897 <https://github.com/beeware/toga/issues/1897>`__)
* Class references were updated to reflect their preferred import location, rather than location where they are defined in code. (`#2001 <https://github.com/beeware/toga/issues/2001>`__)
* The Linux system dependencies were updated to reflect current requirements for developing and using Toga. (`#2021 <https://github.com/beeware/toga/issues/2021>`__)

Misc
----

* `#1865 <https://github.com/beeware/toga/issues/1865>`__, `#1875 <https://github.com/beeware/toga/issues/1875>`__, `#1881 <https://github.com/beeware/toga/issues/1881>`__, `#1882 <https://github.com/beeware/toga/issues/1882>`__, `#1886 <https://github.com/beeware/toga/issues/1886>`__, `#1889 <https://github.com/beeware/toga/issues/1889>`__, `#1895 <https://github.com/beeware/toga/issues/1895>`__, `#1900 <https://github.com/beeware/toga/issues/1900>`__, `#1902 <https://github.com/beeware/toga/issues/1902>`__, `#1906 <https://github.com/beeware/toga/issues/1906>`__, `#1916 <https://github.com/beeware/toga/issues/1916>`__, `#1917 <https://github.com/beeware/toga/issues/1917>`__, `#1918 <https://github.com/beeware/toga/issues/1918>`__, `#1926 <https://github.com/beeware/toga/issues/1926>`__, `#1933 <https://github.com/beeware/toga/issues/1933>`__, `#1948 <https://github.com/beeware/toga/issues/1948>`__, `#1950 <https://github.com/beeware/toga/issues/1950>`__, `#1952 <https://github.com/beeware/toga/issues/1952>`__, `#1954 <https://github.com/beeware/toga/issues/1954>`__, `#1963 <https://github.com/beeware/toga/issues/1963>`__, `#1972 <https://github.com/beeware/toga/issues/1972>`__, `#1977 <https://github.com/beeware/toga/issues/1977>`__, `#1980 <https://github.com/beeware/toga/issues/1980>`__, `#1988 <https://github.com/beeware/toga/issues/1988>`__, `#1989 <https://github.com/beeware/toga/issues/1989>`__, `#1998 <https://github.com/beeware/toga/issues/1998>`__, `#2008 <https://github.com/beeware/toga/issues/2008>`__, `#2014 <https://github.com/beeware/toga/issues/2014>`__, `#2019 <https://github.com/beeware/toga/issues/2019>`__, `#2022 <https://github.com/beeware/toga/issues/2022>`__, `#2028 <https://github.com/beeware/toga/issues/2028>`__, `#2034 <https://github.com/beeware/toga/issues/2034>`__, `#2035 <https://github.com/beeware/toga/issues/2035>`__, `#2039 <https://github.com/beeware/toga/issues/2039>`__, `#2052 <https://github.com/beeware/toga/issues/2052>`__, `#2053 <https://github.com/beeware/toga/issues/2053>`__, `#2055 <https://github.com/beeware/toga/issues/2055>`__, `#2056 <https://github.com/beeware/toga/issues/2056>`__, `#2057 <https://github.com/beeware/toga/issues/2057>`__, `#2059 <https://github.com/beeware/toga/issues/2059>`__, `#2067 <https://github.com/beeware/toga/issues/2067>`__, `#2068 <https://github.com/beeware/toga/issues/2068>`__, `#2069 <https://github.com/beeware/toga/issues/2069>`__, `#2085 <https://github.com/beeware/toga/issues/2085>`__, `#2090 <https://github.com/beeware/toga/issues/2090>`__, `#2092 <https://github.com/beeware/toga/issues/2092>`__, `#2093 <https://github.com/beeware/toga/issues/2093>`__, `#2101 <https://github.com/beeware/toga/issues/2101>`__, `#2102 <https://github.com/beeware/toga/issues/2102>`__, `#2113 <https://github.com/beeware/toga/issues/2113>`__, `#2114 <https://github.com/beeware/toga/issues/2114>`__, `#2115 <https://github.com/beeware/toga/issues/2115>`__, `#2116 <https://github.com/beeware/toga/issues/2116>`__, `#2118 <https://github.com/beeware/toga/issues/2118>`__, `#2119 <https://github.com/beeware/toga/issues/2119>`__, `#2123 <https://github.com/beeware/toga/issues/2123>`__, `#2124 <https://github.com/beeware/toga/issues/2124>`__, `#2127 <https://github.com/beeware/toga/issues/2127>`__, `#2128 <https://github.com/beeware/toga/issues/2128>`__, `#2131 <https://github.com/beeware/toga/issues/2131>`__, `#2132 <https://github.com/beeware/toga/issues/2132>`__, `#2146 <https://github.com/beeware/toga/issues/2146>`__, `#2147 <https://github.com/beeware/toga/issues/2147>`__, `#2148 <https://github.com/beeware/toga/issues/2148>`__, `#2149 <https://github.com/beeware/toga/issues/2149>`__, `#2150 <https://github.com/beeware/toga/issues/2150>`__, `#2163 <https://github.com/beeware/toga/issues/2163>`__, `#2165 <https://github.com/beeware/toga/issues/2165>`__, `#2166 <https://github.com/beeware/toga/issues/2166>`__, `#2171 <https://github.com/beeware/toga/issues/2171>`__, `#2177 <https://github.com/beeware/toga/issues/2177>`__, `#2180 <https://github.com/beeware/toga/issues/2180>`__, `#2184 <https://github.com/beeware/toga/issues/2184>`__, `#2186 <https://github.com/beeware/toga/issues/2186>`__

0.3.1 (2023-04-12)
==================

Features
--------

* The Button widget now has 100% test coverage, and complete API documentation. (`#1761 <https://github.com/beeware/toga/pull/1761>`__)
* The mapping between Pack layout and HTML/CSS has been formalized. (`#1778 <https://github.com/beeware/toga/pull/1778>`__)
* The Label widget now has 100% test coverage, and complete API documentation. (`#1799 <https://github.com/beeware/toga/pull/1799>`__)
* TextInput now supports focus handlers and changing alignment on GTK. (`#1817 <https://github.com/beeware/toga/pull/1817>`__)
* The ActivityIndicator widget now has 100% test coverage, and complete API documentation. (`#1819 <https://github.com/beeware/toga/pull/1819>`__)
* The Box widget now has 100% test coverage, and complete API documentation. (`#1820 <https://github.com/beeware/toga/pull/1820>`__)
* NumberInput now supports changing alignment on GTK. (`#1821 <https://github.com/beeware/toga/pull/1821>`__)
* The Divider widget now has 100% test coverage, and complete API documentation. (`#1823 <https://github.com/beeware/toga/pull/1823>`__)
* The ProgressBar widget now has 100% test coverage, and complete API documentation. (`#1825 <https://github.com/beeware/toga/pull/1825>`__)
* The Switch widget now has 100% test coverage, and complete API documentation. (`#1832 <https://github.com/beeware/toga/pull/1832>`__)
* Event handlers have been internally modified to simplify their definition and use on backends. (`#1833 <https://github.com/beeware/toga/pull/1833>`__)
* The base Toga Widget now has 100% test coverage, and complete API documentation. (`#1834 <https://github.com/beeware/toga/pull/1834>`__)
* Support for FreeBSD was added. (`#1836 <https://github.com/beeware/toga/pull/1836>`__)
* The Web backend now uses Shoelace to provide web components. (`#1838 <https://github.com/beeware/toga/pull/1838>`__)
* Winforms apps can now go full screen. (`#1863 <https://github.com/beeware/toga/pull/1863>`__)


Bugfixes
--------

* Issues with reducing the size of windows on GTK have been resolved. (`#1205 <https://github.com/beeware/toga/issues/1205>`__)
* iOS now supports newlines in Labels. (`#1501 <https://github.com/beeware/toga/issues/1501>`__)
* The Slider widget now has 100% test coverage, and complete API documentation. (`#1708 <https://github.com/beeware/toga/pull/1708>`__)
* The GTK backend no longer raises a warning about the use of a deprecated ``set_wmclass`` API. (`#1718 <https://github.com/beeware/toga/issues/1718>`__)
* MultilineTextInput now correctly adapts to Dark Mode on macOS. (`#1783 <https://github.com/beeware/toga/issues/1783>`__)
* The handling of GTK layouts has been modified to reduce the frequency and increase the accuracy of layout results. (`#1794 <https://github.com/beeware/toga/pull/1794>`__)
* The text alignment of MultilineTextInput on Android has been fixed to be TOP aligned. (`#1808 <https://github.com/beeware/toga/pull/1808>`__)
* GTK widgets that involve animation (such as Switch or ProgressBar) are now redrawn correctly. (`#1826 <https://github.com/beeware/toga/issues/1826>`__)


Improved Documentation
----------------------

* API support tables now distinguish partial vs full support on each platform. (`#1762 <https://github.com/beeware/toga/pull/1762>`__)
* Some missing settings and constant values were added to the documentation of Pack. (`#1786 <https://github.com/beeware/toga/pull/1786>`__)
* Added documentation for ``toga.App.widgets``. (`#1852 <https://github.com/beeware/toga/pull/1852>`__)


Misc
----

* `#1750 <https://github.com/beeware/toga/issues/1750>`__, `#1764 <https://github.com/beeware/toga/pull/1764>`__, `#1765 <https://github.com/beeware/toga/pull/1765>`__, `#1766 <https://github.com/beeware/toga/pull/1766>`__, `#1770 <https://github.com/beeware/toga/pull/1770>`__, `#1771 <https://github.com/beeware/toga/pull/1771>`__, `#1777 <https://github.com/beeware/toga/pull/1777>`__, `#1797 <https://github.com/beeware/toga/pull/1797>`__, `#1802 <https://github.com/beeware/toga/pull/1802>`__, `#1813 <https://github.com/beeware/toga/pull/1813>`__, `#1818 <https://github.com/beeware/toga/pull/1818>`__, `#1822 <https://github.com/beeware/toga/pull/1822>`__, `#1829 <https://github.com/beeware/toga/pull/1829>`__, `#1830 <https://github.com/beeware/toga/pull/1830>`__, `#1835 <https://github.com/beeware/toga/pull/1835>`__, `#1839 <https://github.com/beeware/toga/pull/1839>`__, `#1854 <https://github.com/beeware/toga/pull/1854>`__, `#1861 <https://github.com/beeware/toga/pull/1861>`__


0.3.0 (2023-01-30)
==================

Features
--------

* Widgets now use a three-layered (Interface/Implementation/Native) structure.
* A GUI testing framework was added.
* A simplified "Pack" layout algorithm was added.
* Added a web backend.

Bugfixes
--------

* Too many to count!

0.2.15
======

* Added more widgets and cross-platform support, especially for GTK+ and Winforms

0.2.14
======

* Removed use of ``namedtuple``

0.2.13
======

* Various fixes in preparation for PyCon AU demo

0.2.12
======

* Migrated to CSS-based layout, rather than Cassowary/constraint layout.
* Added Windows backend
* Added Django backend
* Added Android backend

0.2.0 - 0.2.11
==============

Internal development releases.

0.1.2
=====

* Further improvements to multiple-repository packaging strategy.
* Ensure Ctrl-C is honored by apps.
* **Cocoa:** Added runtime warnings when minimum OS X version is not met.

0.1.1
=====

* Refactored code into multiple repositories, so that users of one backend don't
  have to carry the overhead of other installed platforms

* Corrected a range of bugs, mostly related to problems under Python 3.

0.1.0
=====

Initial public release. Includes:

* A Cocoa (OS X) backend
* A GTK+ backend
* A proof-of-concept Win32 backend
* A proof-of-concept iOS backend
