:tocdepth: 2

===============
Release History
===============

.. towncrier release notes start

0.4.9 (2025-02-07)
==================

This release contains no new features. The primary purpose of this release is to add an upper version pin to Toga's Travertino requirement, protecting against the upcoming Toga 0.5.0 release that will include backwards incompatible changes in Travertino.  (`#3167 <https://github.com/beeware/toga/issues/3167>`__)

Bugfixes
--------

* The testbed app can now be run on *any* supported Python version. (`#2883 <https://github.com/beeware/toga/issues/2883>`__)
* App.app is now set to an initial value of ``None``, before an app instance is created. This avoids a potential ``AttributeError`` when the test suite finishes. (`#2918 <https://github.com/beeware/toga/issues/2918>`__)

Misc
----

* `#2476 <https://github.com/beeware/toga/issues/2476>`__, `#2913 <https://github.com/beeware/toga/issues/2913>`__

0.4.8 (2024-10-16)
==================

Bugfixes
--------

* On macOS, apps that specify both `document_types` and a `main_window` no longer display the document selection dialog on startup. (`#2860 <https://github.com/beeware/toga/issues/2860>`__)
* The integration with Android's event loop has been updated to support Python 3.13. (`#2907 <https://github.com/beeware/toga/issues/2907>`__)


Backward Incompatible Changes
-----------------------------

* Toga no longer supports Python 3.8. (`#2888 <https://github.com/beeware/toga/issues/2888>`__)
* Android applications should update their Gradle requirements to use version 1.12.0 of the Material library (``com.google.android.material:material:1.12.0``). (`#2890 <https://github.com/beeware/toga/issues/2890>`__)
* Android applications should update their Gradle requirements to use version 6.1.20 of the OSMDroid library (``org.osmdroid:osmdroid-android:6.1.20``). (`#2890 <https://github.com/beeware/toga/issues/2890>`__)


Misc
----

* `#2868 <https://github.com/beeware/toga/issues/2868>`__, `#2869 <https://github.com/beeware/toga/issues/2869>`__, `#2870 <https://github.com/beeware/toga/issues/2870>`__, `#2876 <https://github.com/beeware/toga/issues/2876>`__, `#2877 <https://github.com/beeware/toga/issues/2877>`__, `#2884 <https://github.com/beeware/toga/issues/2884>`__, `#2885 <https://github.com/beeware/toga/issues/2885>`__, `#2886 <https://github.com/beeware/toga/issues/2886>`__, `#2887 <https://github.com/beeware/toga/issues/2887>`__, `#2893 <https://github.com/beeware/toga/issues/2893>`__, `#2897 <https://github.com/beeware/toga/issues/2897>`__, `#2898 <https://github.com/beeware/toga/issues/2898>`__, `#2899 <https://github.com/beeware/toga/issues/2899>`__, `#2900 <https://github.com/beeware/toga/issues/2900>`__, `#2901 <https://github.com/beeware/toga/issues/2901>`__, `#2902 <https://github.com/beeware/toga/issues/2902>`__, `#2903 <https://github.com/beeware/toga/issues/2903>`__, `#2904 <https://github.com/beeware/toga/issues/2904>`__, `#2905 <https://github.com/beeware/toga/issues/2905>`__, `#2906 <https://github.com/beeware/toga/issues/2906>`__, `#2912 <https://github.com/beeware/toga/issues/2912>`__


0.4.7 (2024-09-18)
==================

Features
--------

* The GTK backend was modified to use PyGObject's native asyncio handling, instead of GBulb. (`#2550 <https://github.com/beeware/toga/issues/2550>`__)
* The ActivityIndicator widget is now supported on iOS. (`#2829 <https://github.com/beeware/toga/issues/2829>`__)

Bugfixes
--------

* Windows retain their original size after being unminimized on Windows. (`#2729 <https://github.com/beeware/toga/issues/2729>`__)
* DOM storage is now enabled for WebView on Android. (`#2767 <https://github.com/beeware/toga/issues/2767>`__)
* A macOS app in full-screen mode now correctly displays the contents of windows that use a ``toga.Box()`` as the top-level content. (`#2796 <https://github.com/beeware/toga/issues/2796>`__)
* Asynchronous tasks are now protected from garbage collection while they are running. This could lead to asynchronous tasks terminating unexpectedly with an error under some conditions. (`#2809 <https://github.com/beeware/toga/issues/2809>`__)
* When a handler is a generator, control will now always be released to the event loop between iterations, even if no sleep interval or a sleep interval of 0 is yielded. (`#2811 <https://github.com/beeware/toga/issues/2811>`__)
* When the X button is clicked for the About dialog on GTK, it is now properly destroyed. (`#2812 <https://github.com/beeware/toga/issues/2812>`__)
* The Textual backend is now compatible with versions of Textual after v0.63.3. (`#2822 <https://github.com/beeware/toga/issues/2822>`__)
* The event loop is now guaranteed to be running when your app's ``startup()`` method is invoked. This wasn't previously the case on macOS and Windows. (`#2834 <https://github.com/beeware/toga/issues/2834>`__)
* iOS apps now correctly account for the size of the navigation bar when laying out app content. (`#2836 <https://github.com/beeware/toga/issues/2836>`__)
* A memory leak when using Divider or Switch widgets on iOS was resolved. (`#2849 <https://github.com/beeware/toga/issues/2849>`__)
* Apps bundled as standalone frozen binaries (e.g., POSIX builds made with PyInstaller) no longer crash on startup when trying to resolve the app icon. (`#2852 <https://github.com/beeware/toga/issues/2852>`__)


Misc
----

* `#2088 <https://github.com/beeware/toga/issues/2088>`__, `#2708 <https://github.com/beeware/toga/issues/2708>`__, `#2715 <https://github.com/beeware/toga/issues/2715>`__, `#2792 <https://github.com/beeware/toga/issues/2792>`__, `#2799 <https://github.com/beeware/toga/issues/2799>`__, `#2802 <https://github.com/beeware/toga/issues/2802>`__, `#2803 <https://github.com/beeware/toga/issues/2803>`__, `#2804 <https://github.com/beeware/toga/issues/2804>`__, `#2807 <https://github.com/beeware/toga/issues/2807>`__, `#2823 <https://github.com/beeware/toga/issues/2823>`__, `#2824 <https://github.com/beeware/toga/issues/2824>`__, `#2825 <https://github.com/beeware/toga/issues/2825>`__, `#2826 <https://github.com/beeware/toga/issues/2826>`__, `#2846 <https://github.com/beeware/toga/issues/2846>`__, `#2847 <https://github.com/beeware/toga/issues/2847>`__, `#2848 <https://github.com/beeware/toga/issues/2848>`__


0.4.6 (2024-08-28)
==================

Features
--------

* Toga can now define apps that persist in the background without having any open windows. (`#97 <https://github.com/beeware/toga/issues/97>`__)
* Apps can now add items to the system tray. (`#97 <https://github.com/beeware/toga/issues/97>`__)
* It is now possible to use an instance of Window as the main window of an app. This allows the creation of windows that don't have a menu bar or toolbar decoration. (`#1870 <https://github.com/beeware/toga/issues/1870>`__)
* The initial position of each newly created window is now different, cascading down the screen as windows are created. (`#2023 <https://github.com/beeware/toga/issues/2023>`__)
* The API for Documents and document types has been finalized. Document handling behavior is now controlled by declaring document types as part of your ``toga.App`` definition. (`#2209 <https://github.com/beeware/toga/issues/2209>`__)
* Toga can now define an app whose life cycle isn't tied to a single main window. (`#2209 <https://github.com/beeware/toga/issues/2209>`__)
* The Divider widget was implemented on iOS. (`#2478 <https://github.com/beeware/toga/issues/2478>`__)
* Commands can now be retrieved by ID. System-installed commands (such as "About" and "Visit Homepage") are installed using a known ID that can be used at runtime to manipulate those commands. (`#2636 <https://github.com/beeware/toga/issues/2636>`__)
* A ``MainWindow`` can now have an ``on_close`` handler. If a request is made to close the main window, the ``on_close`` handler will be evaluated; app exit handling will only be processed if the close handler allows the close to continue. (`#2643 <https://github.com/beeware/toga/issues/2643>`__)
* Dialogs can now be displayed relative to an app, in addition to be being modal to a window. (`#2669 <https://github.com/beeware/toga/issues/2669>`__)
* An ``on_running`` event handler was added to ``toga.App``. This event will be triggered when the app's main loop starts. (`#2678 <https://github.com/beeware/toga/issues/2678>`__)
* The ``on_exit`` handler for an app can now be defined by overriding the method on the ``toga.App`` subclass. (`#2678 <https://github.com/beeware/toga/issues/2678>`__)
* CommandSet now exposes a full set and dictionary interface. Commands can be added to a CommandSet using ``[]`` notation and a command ID; they can be removed using set-like ``remove()`` or ``discard()`` calls with a Command instance, or using dictionary-like ``pop()`` or ``del`` calls with the command ID. (`#2701 <https://github.com/beeware/toga/issues/2701>`__)
* WebView2 on Winforms now uses the v1.0.2592.51 WebView2 runtime DLLs. (`#2764 <https://github.com/beeware/toga/issues/2764>`__)

Bugfixes
--------

* The order of creation of system-level commands is now consistent between platforms. Menu creation is guaranteed to be deferred until the user's startup method has been invoked. (`#2619 <https://github.com/beeware/toga/issues/2619>`__)
* The type of SplitContainer's content was modified to be a list, rather than a tuple. (`#2638 <https://github.com/beeware/toga/issues/2638>`__)
* Programmatically invoking ``close()`` on the main window will now trigger ``on_exit`` handling. Previously ``on_exit`` handling would only be triggered if the close was initiated by a user action. (`#2643 <https://github.com/beeware/toga/issues/2643>`__)
* GTK apps no longer have extra padding between the menu bar and the window content when the app does not have a toolbar. (`#2646 <https://github.com/beeware/toga/issues/2646>`__)
* On Winforms, the window of an application that is set as the main window is no longer shown as a result of assigning the window as ``App.main_window``. (`#2653 <https://github.com/beeware/toga/issues/2653>`__)
* Menu items on macOS are now able to correctly bind to the arrow and home/end/delete keys. (`#2661 <https://github.com/beeware/toga/issues/2661>`__)
* On GTK, the currently selected tab index on an ``OptionContainer`` can now be retrieved inside an ``on_select`` handler. (`#2703 <https://github.com/beeware/toga/issues/2703>`__)
* The WebView can now be loaded when using Python from the Windows Store. (`#2752 <https://github.com/beeware/toga/issues/2752>`__)
* The WebView and MapView widgets now log an error if initialization fails. (`#2779 <https://github.com/beeware/toga/issues/2779>`__)


Backward Incompatible Changes
-----------------------------

* The ``add_background_task()`` API on ``toga.App`` has been deprecated. Background tasks can be implemented using the new ``on_running`` event handler, or by using :any:`asyncio.create_task`. (`#2099 <https://github.com/beeware/toga/issues/2099>`__)
* The API for Documents and Document-based apps has been significantly modified. Unfortunately, these changes are not backwards compatible; any existing Document-based app will require modification.

  The ``DocumentApp`` base class is no longer required. Apps can subclass ``App`` directly, passing the document types as a ``list`` of ``Document`` classes, rather than a mapping of extension to document type.

  The API for ``Document`` subclasses has also changed:

  * A path is no longer provided as an argument to the Document constructor;

  * The ``document_type`` is now specified as a class property called ``description``; and

  * Extensions are now defined as a class property of the ``Document``; and

  * The ``can_close()`` handler is no longer honored. Documents now track if they are modified, and have a default ``on_close`` handler that uses the modification status of a document to control whether a document can close. Invoking ``touch()`` on document will mark a document as modified. This modification flag is cleared by saving the document. (`#2209 <https://github.com/beeware/toga/issues/2209>`__)
* It is no longer possible to create a toolbar on a ``Window`` instance. Toolbars can only be added to ``MainWindow`` (or subclass). (`#2646 <https://github.com/beeware/toga/issues/2646>`__)
* The default title of a ``toga.Window`` is now the name of the app, rather than ``"Toga"``. (`#2646 <https://github.com/beeware/toga/issues/2646>`__)
* The APIs on ``Window`` for displaying dialogs (``info_dialog()``, ``question_dialog()``, etc) have been deprecated. They can be replaced with creating an instance of a ``Dialog`` class (e.g., ``InfoDialog``), and passing that instance to ``window.dialog()``. (`#2669 <https://github.com/beeware/toga/issues/2669>`__)

Documentation
-------------

* Building Toga's documentation now requires the use of Python 3.12. (`#2745 <https://github.com/beeware/toga/issues/2745>`__)

Misc
----

* `#2382 <https://github.com/beeware/toga/issues/2382>`__, `#2635 <https://github.com/beeware/toga/issues/2635>`__, `#2640 <https://github.com/beeware/toga/issues/2640>`__, `#2647 <https://github.com/beeware/toga/issues/2647>`__, `#2648 <https://github.com/beeware/toga/issues/2648>`__, `#2654 <https://github.com/beeware/toga/issues/2654>`__, `#2657 <https://github.com/beeware/toga/issues/2657>`__, `#2660 <https://github.com/beeware/toga/issues/2660>`__, `#2665 <https://github.com/beeware/toga/issues/2665>`__, `#2668 <https://github.com/beeware/toga/issues/2668>`__, `#2675 <https://github.com/beeware/toga/issues/2675>`__, `#2676 <https://github.com/beeware/toga/issues/2676>`__, `#2677 <https://github.com/beeware/toga/issues/2677>`__, `#2682 <https://github.com/beeware/toga/issues/2682>`__, `#2683 <https://github.com/beeware/toga/issues/2683>`__, `#2684 <https://github.com/beeware/toga/issues/2684>`__, `#2689 <https://github.com/beeware/toga/issues/2689>`__, `#2693 <https://github.com/beeware/toga/issues/2693>`__, `#2694 <https://github.com/beeware/toga/issues/2694>`__, `#2695 <https://github.com/beeware/toga/issues/2695>`__, `#2696 <https://github.com/beeware/toga/issues/2696>`__, `#2697 <https://github.com/beeware/toga/issues/2697>`__, `#2698 <https://github.com/beeware/toga/issues/2698>`__, `#2699 <https://github.com/beeware/toga/issues/2699>`__, `#2709 <https://github.com/beeware/toga/issues/2709>`__, `#2710 <https://github.com/beeware/toga/issues/2710>`__, `#2711 <https://github.com/beeware/toga/issues/2711>`__, `#2712 <https://github.com/beeware/toga/issues/2712>`__, `#2722 <https://github.com/beeware/toga/issues/2722>`__, `#2723 <https://github.com/beeware/toga/issues/2723>`__, `#2724 <https://github.com/beeware/toga/issues/2724>`__, `#2726 <https://github.com/beeware/toga/issues/2726>`__, `#2727 <https://github.com/beeware/toga/issues/2727>`__, `#2728 <https://github.com/beeware/toga/issues/2728>`__, `#2733 <https://github.com/beeware/toga/issues/2733>`__, `#2734 <https://github.com/beeware/toga/issues/2734>`__, `#2735 <https://github.com/beeware/toga/issues/2735>`__, `#2736 <https://github.com/beeware/toga/issues/2736>`__, `#2739 <https://github.com/beeware/toga/issues/2739>`__, `#2740 <https://github.com/beeware/toga/issues/2740>`__, `#2742 <https://github.com/beeware/toga/issues/2742>`__, `#2743 <https://github.com/beeware/toga/issues/2743>`__, `#2755 <https://github.com/beeware/toga/issues/2755>`__, `#2756 <https://github.com/beeware/toga/issues/2756>`__, `#2757 <https://github.com/beeware/toga/issues/2757>`__, `#2758 <https://github.com/beeware/toga/issues/2758>`__, `#2760 <https://github.com/beeware/toga/issues/2760>`__, `#2771 <https://github.com/beeware/toga/issues/2771>`__, `#2775 <https://github.com/beeware/toga/issues/2775>`__, `#2776 <https://github.com/beeware/toga/issues/2776>`__, `#2777 <https://github.com/beeware/toga/issues/2777>`__, `#2783 <https://github.com/beeware/toga/issues/2783>`__, `#2788 <https://github.com/beeware/toga/issues/2788>`__, `#2789 <https://github.com/beeware/toga/issues/2789>`__, `#2790 <https://github.com/beeware/toga/issues/2790>`__


0.4.5 (2024-06-11)
==================

Features
--------

* The typing for Toga's API surface was updated to be more precise. (`#2252 <https://github.com/beeware/toga/issues/2252>`__)
* APIs were added for replacing a widget in an existing layout, and for obtaining the index of a widget in a list of children. (`#2301 <https://github.com/beeware/toga/issues/2301>`__)
* The content of a window can now be set when the window is constructed. (`#2307 <https://github.com/beeware/toga/issues/2307>`__)
* Size and position properties now return values as a ``Size`` and ``Position`` ``namedtuple``, respectively. ``namedtuple`` objects support addition and subtraction operations. Basic tuples can still be used to *set* these properties. (`#2388 <https://github.com/beeware/toga/issues/2388>`__)
* Android deployments no longer require the SwipeRefreshLayout component unless the app uses the Toga DetailedList widget. (`#2454 <https://github.com/beeware/toga/issues/2454>`__)

Bugfixes
--------

* Invocation order of TextInput on_change and validation is now correct. (`#2325 <https://github.com/beeware/toga/issues/2325>`__)
* Dialog windows are now properly modal when using the GTK backend. (`#2446 <https://github.com/beeware/toga/issues/2446>`__)
* The Button testbed tests can accommodate minor rendering differences on Fedora 40. (`#2583 <https://github.com/beeware/toga/issues/2583>`__)
* On macOS, apps will now raise a warning if camera permissions have been requested, but those permissions have not been declared as part of the application metadata. (`#2589 <https://github.com/beeware/toga/issues/2589>`__)

Documentation
-------------

* The instructions for adding a change note to a pull request have been clarified. (`#2565 <https://github.com/beeware/toga/issues/2565>`__)
* The minimum supported Linux release requirements were updated to Ubuntu 20.04 or Fedora 32. (`#2566 <https://github.com/beeware/toga/issues/2566>`__)
* The first-time contributor README link has been updated. (`#2588 <https://github.com/beeware/toga/issues/2588>`__)
* Typos in the usage examples of ``toga.MapPin`` were corrected. (`#2617 <https://github.com/beeware/toga/issues/2617>`__)

Misc
----

* `#2567 <https://github.com/beeware/toga/issues/2567>`__, `#2568 <https://github.com/beeware/toga/issues/2568>`__, `#2569 <https://github.com/beeware/toga/issues/2569>`__, `#2570 <https://github.com/beeware/toga/issues/2570>`__, `#2571 <https://github.com/beeware/toga/issues/2571>`__, `#2576 <https://github.com/beeware/toga/issues/2576>`__, `#2577 <https://github.com/beeware/toga/issues/2577>`__, `#2578 <https://github.com/beeware/toga/issues/2578>`__, `#2579 <https://github.com/beeware/toga/issues/2579>`__, `#2580 <https://github.com/beeware/toga/issues/2580>`__, `#2593 <https://github.com/beeware/toga/issues/2593>`__, `#2600 <https://github.com/beeware/toga/issues/2600>`__, `#2601 <https://github.com/beeware/toga/issues/2601>`__, `#2602 <https://github.com/beeware/toga/issues/2602>`__, `#2604 <https://github.com/beeware/toga/issues/2604>`__, `#2605 <https://github.com/beeware/toga/issues/2605>`__, `#2606 <https://github.com/beeware/toga/issues/2606>`__, `#2614 <https://github.com/beeware/toga/issues/2614>`__, `#2621 <https://github.com/beeware/toga/issues/2621>`__, `#2625 <https://github.com/beeware/toga/issues/2625>`__, `#2626 <https://github.com/beeware/toga/issues/2626>`__, `#2627 <https://github.com/beeware/toga/issues/2627>`__, `#2629 <https://github.com/beeware/toga/issues/2629>`__, `#2631 <https://github.com/beeware/toga/issues/2631>`__, `#2632 <https://github.com/beeware/toga/issues/2632>`__


0.4.4 (2024-05-08)
==================

Bugfixes
--------

* The mechanism for loading application icons on macOS was corrected to account for how Xcode populates ``Info.plist`` metadata. (`#2558 <https://github.com/beeware/toga/issues/2558>`__)

Misc
----

* `#2555 <https://github.com/beeware/toga/issues/2555>`__, `#2557 <https://github.com/beeware/toga/issues/2557>`__, `#2560 <https://github.com/beeware/toga/issues/2560>`__

0.4.3 (2024-05-06)
==================

Features
--------

* A MapView widget was added. (`#727 <https://github.com/beeware/toga/issues/727>`__)
* Toga apps can now access details about the screens attached to the computer. Window position APIs have been extended to allow for placement on a specific screen, and positioning relative to a specific screen. (`#1930 <https://github.com/beeware/toga/issues/1930>`__)
* Key definitions were added for number pad keys on GTK. (`#2232 <https://github.com/beeware/toga/issues/2232>`__)
* Toga can now be extended, via plugins, to create Toga Images from external image classes (and vice-versa). (`#2387 <https://github.com/beeware/toga/issues/2387>`__)
* Non-implemented features now raise a formal warning, rather than logging to the console. (`#2398 <https://github.com/beeware/toga/issues/2398>`__)
* Support for Python 3.13 was added. (`#2404 <https://github.com/beeware/toga/issues/2404>`__)
* Toga's release processes now include automated testing on ARM64. (`#2404 <https://github.com/beeware/toga/issues/2404>`__)
* An action for a Toga command can now be easily modified after initial construction. (`#2433 <https://github.com/beeware/toga/issues/2433>`__)
* A geolocation service was added for Android, iOS and macOS. (`#2462 <https://github.com/beeware/toga/issues/2462>`__)
* When a Toga app is packaged as a binary, and no icon is explicitly configured, Toga will now use the binary's icon as the app icon. This means it is no longer necessary to include the app icon as data in a ``resources`` folder if you are packaging your app for distribution. (`#2527 <https://github.com/beeware/toga/issues/2527>`__)

Bugfixes
--------

* Compatibility with macOS 14 (Sonoma) was added. (`#2188 <https://github.com/beeware/toga/issues/2188>`__, `#2383 <https://github.com/beeware/toga/issues/2383>`__)
* Key handling for Insert, Delete, NumLock, ScrollLock, and some other esoteric keys was added for GTK and Winforms. Some uses of bare Shift on GTK were also improved. (`#2220 <https://github.com/beeware/toga/issues/2220>`__)
* A crash observed on iOS devices when taking photographs has been resolved. (`#2381 <https://github.com/beeware/toga/issues/2381>`__)
* Key shortcuts for punctuation and special keys (like Page Up and Escape) were added for GTK and Winforms. (`#2414 <https://github.com/beeware/toga/issues/2414>`__)
* The placement of menu items relative to sub-menus was corrected on GTK. (`#2418 <https://github.com/beeware/toga/issues/2418>`__)
* Tree data nodes can now be modified prior to tree expansion. (`#2439 <https://github.com/beeware/toga/issues/2439>`__)
* Some memory leaks associated with macOS Icon and Image storage were resolved. (`#2472 <https://github.com/beeware/toga/issues/2472>`__)
* The stack trace dialog no longer raises an ``asyncio.TimeoutError`` when displayed. (`#2474 <https://github.com/beeware/toga/issues/2474>`__)
* The integration of the ``asyncio`` event loop was simplified on Android. As a result, ``asyncio.loop.run_in_executor()`` now works as expected. (`#2479 <https://github.com/beeware/toga/issues/2479>`__)
* Some memory leaks associated with the macOS Table, Tree and DetailedList widgets were resolved. (`#2482 <https://github.com/beeware/toga/issues/2482>`__)
* Widget IDs can now be reused after the associated widget's window is closed. (`#2514 <https://github.com/beeware/toga/issues/2514>`__)
* :class:`~toga.WebView` is now compatible with Linux GTK environments only providing WebKit2 version 4.1 without version 4.0. (`#2527 <https://github.com/beeware/toga/issues/2527>`__)

Backward Incompatible Changes
-----------------------------

* The macOS implementations of ``Window.as_image()`` and ``Canvas.as_image()`` APIs now return images in native device resolution, not CSS pixel resolution. This will result in images that are double the previous size on Retina displays. (`#1930 <https://github.com/beeware/toga/issues/1930>`__)

Documentation
-------------

* The camera permission requirements on macOS apps have been clarified. (`#2381 <https://github.com/beeware/toga/issues/2381>`__)
* Documentation for the class property ``toga.App.app`` was added. (`#2413 <https://github.com/beeware/toga/issues/2413>`__)
* The documentation landing page and some documentation sections were reorganized. (`#2463 <https://github.com/beeware/toga/issues/2463>`__)
* The README badges were updated to display correctly on GitHub. (`#2491 <https://github.com/beeware/toga/issues/2491>`__)
* The links to ReadTheDocs were updated to better arbitrate between linking to the stable version or the latest version. (`#2510 <https://github.com/beeware/toga/issues/2510>`__)
* An explicit system requirements section was added to the documentation for widgets that require the installation of additional system components. (`#2544 <https://github.com/beeware/toga/issues/2544>`__)
* The system requirements were updated to be more explicit and now include details for OpenSUSE Tumbleweed. (`#2549 <https://github.com/beeware/toga/issues/2549>`__)

Misc
----

* `#2153 <https://github.com/beeware/toga/issues/2153>`__, `#2372 <https://github.com/beeware/toga/issues/2372>`__, `#2389 <https://github.com/beeware/toga/issues/2389>`__, `#2390 <https://github.com/beeware/toga/issues/2390>`__, `#2391 <https://github.com/beeware/toga/issues/2391>`__, `#2392 <https://github.com/beeware/toga/issues/2392>`__, `#2393 <https://github.com/beeware/toga/issues/2393>`__, `#2394 <https://github.com/beeware/toga/issues/2394>`__, `#2396 <https://github.com/beeware/toga/issues/2396>`__, `#2397 <https://github.com/beeware/toga/issues/2397>`__, `#2400 <https://github.com/beeware/toga/issues/2400>`__, `#2403 <https://github.com/beeware/toga/issues/2403>`__, `#2405 <https://github.com/beeware/toga/issues/2405>`__, `#2406 <https://github.com/beeware/toga/issues/2406>`__, `#2407 <https://github.com/beeware/toga/issues/2407>`__, `#2408 <https://github.com/beeware/toga/issues/2408>`__, `#2409 <https://github.com/beeware/toga/issues/2409>`__, `#2422 <https://github.com/beeware/toga/issues/2422>`__, `#2423 <https://github.com/beeware/toga/issues/2423>`__, `#2427 <https://github.com/beeware/toga/issues/2427>`__, `#2440 <https://github.com/beeware/toga/issues/2440>`__, `#2442 <https://github.com/beeware/toga/issues/2442>`__, `#2445 <https://github.com/beeware/toga/issues/2445>`__, `#2448 <https://github.com/beeware/toga/issues/2448>`__, `#2449 <https://github.com/beeware/toga/issues/2449>`__, `#2450 <https://github.com/beeware/toga/issues/2450>`__, `#2457 <https://github.com/beeware/toga/issues/2457>`__, `#2458 <https://github.com/beeware/toga/issues/2458>`__, `#2459 <https://github.com/beeware/toga/issues/2459>`__, `#2460 <https://github.com/beeware/toga/issues/2460>`__, `#2464 <https://github.com/beeware/toga/issues/2464>`__, `#2465 <https://github.com/beeware/toga/issues/2465>`__, `#2466 <https://github.com/beeware/toga/issues/2466>`__, `#2467 <https://github.com/beeware/toga/issues/2467>`__, `#2470 <https://github.com/beeware/toga/issues/2470>`__, `#2471 <https://github.com/beeware/toga/issues/2471>`__, `#2476 <https://github.com/beeware/toga/issues/2476>`__, `#2487 <https://github.com/beeware/toga/issues/2487>`__, `#2488 <https://github.com/beeware/toga/issues/2488>`__, `#2498 <https://github.com/beeware/toga/issues/2498>`__, `#2501 <https://github.com/beeware/toga/issues/2501>`__, `#2502 <https://github.com/beeware/toga/issues/2502>`__, `#2503 <https://github.com/beeware/toga/issues/2503>`__, `#2504 <https://github.com/beeware/toga/issues/2504>`__, `#2509 <https://github.com/beeware/toga/issues/2509>`__, `#2518 <https://github.com/beeware/toga/issues/2518>`__, `#2519 <https://github.com/beeware/toga/issues/2519>`__, `#2520 <https://github.com/beeware/toga/issues/2520>`__, `#2521 <https://github.com/beeware/toga/issues/2521>`__, `#2522 <https://github.com/beeware/toga/issues/2522>`__, `#2523 <https://github.com/beeware/toga/issues/2523>`__, `#2532 <https://github.com/beeware/toga/issues/2532>`__, `#2533 <https://github.com/beeware/toga/issues/2533>`__, `#2534 <https://github.com/beeware/toga/issues/2534>`__, `#2535 <https://github.com/beeware/toga/issues/2535>`__, `#2536 <https://github.com/beeware/toga/issues/2536>`__, `#2537 <https://github.com/beeware/toga/issues/2537>`__, `#2538 <https://github.com/beeware/toga/issues/2538>`__, `#2539 <https://github.com/beeware/toga/issues/2539>`__, `#2540 <https://github.com/beeware/toga/issues/2540>`__, `#2541 <https://github.com/beeware/toga/issues/2541>`__, `#2542 <https://github.com/beeware/toga/issues/2542>`__, `#2546 <https://github.com/beeware/toga/issues/2546>`__, `#2552 <https://github.com/beeware/toga/issues/2552>`__

0.4.2 (2024-02-06)
==================

Features
--------

* Buttons can now be created with an icon, instead of a text label. (`#774 <https://github.com/beeware/toga/issues/774>`__)
* Widgets and Windows can now be sorted. The ID of the widget is used for the sorting order. (`#2190 <https://github.com/beeware/toga/issues/2190>`__)
* The main window generated by the default ``startup()`` method of an app now has an ID of ``main``. (`#2190 <https://github.com/beeware/toga/issues/2190>`__)
* A cross-platform API for camera access was added. (`#2266 <https://github.com/beeware/toga/issues/2266>`__, `#2353 <https://github.com/beeware/toga/issues/2353>`__)
* An OptionContainer widget was added for Android. (`#2346 <https://github.com/beeware/toga/issues/2346>`__)

Bugfixes
--------

* New widgets with an ID matching an ID that was previously used no longer cause an error. (`#2190 <https://github.com/beeware/toga/issues/2190>`__)
* ``App.current_window`` on GTK now returns ``None`` when all windows are hidden. (`#2211 <https://github.com/beeware/toga/issues/2211>`__)
* Selection widgets on macOS can now include duplicated titles. (`#2319 <https://github.com/beeware/toga/issues/2319>`__)
* The padding around DetailedList on Android has been reduced. (`#2338 <https://github.com/beeware/toga/issues/2338>`__)
* The error returned when an Image is created with no source has been clarified. (`#2347 <https://github.com/beeware/toga/issues/2347>`__)
* On macOS, ``toga.Image`` objects can now be created from raw data that didn't originate from a file. (`#2355 <https://github.com/beeware/toga/issues/2355>`__)
* Winforms no longer generates a system beep when pressing Enter in a TextInput. (`#2374 <https://github.com/beeware/toga/issues/2374>`__)

Backward Incompatible Changes
-----------------------------

* Widgets must now be added to a window to be available in the widget registry for lookup by ID. (`#2190 <https://github.com/beeware/toga/issues/2190>`__)
* If the label for a Selection contains newlines, only the text up to the first newline will be displayed. (`#2319 <https://github.com/beeware/toga/issues/2319>`__)
* The internal Android method ``intent_result`` has been deprecated. This was an internal API, and not formally documented, but it was the easiest mechanism for invoking Intents on the Android backend. It has been replaced by the synchronous ``start_activity`` method that allows you to register a callback when the intent completes. (`#2353 <https://github.com/beeware/toga/issues/2353>`__)

Documentation
-------------

* Initial documentation of backend-specific features has been added. (`#1798 <https://github.com/beeware/toga/issues/1798>`__)
* The difference between Icon and Image was clarified, and a note about the lack of an ``on_press`` handler on ImageView was added. (`#2348 <https://github.com/beeware/toga/issues/2348>`__)

Misc
----

* `#2298 <https://github.com/beeware/toga/issues/2298>`__, `#2299 <https://github.com/beeware/toga/issues/2299>`__, `#2302 <https://github.com/beeware/toga/issues/2302>`__, `#2312 <https://github.com/beeware/toga/issues/2312>`__, `#2313 <https://github.com/beeware/toga/issues/2313>`__, `#2318 <https://github.com/beeware/toga/issues/2318>`__, `#2331 <https://github.com/beeware/toga/issues/2331>`__, `#2332 <https://github.com/beeware/toga/issues/2332>`__, `#2333 <https://github.com/beeware/toga/issues/2333>`__, `#2336 <https://github.com/beeware/toga/issues/2336>`__, `#2337 <https://github.com/beeware/toga/issues/2337>`__, `#2339 <https://github.com/beeware/toga/issues/2339>`__, `#2340 <https://github.com/beeware/toga/issues/2340>`__, `#2357 <https://github.com/beeware/toga/issues/2357>`__, `#2358 <https://github.com/beeware/toga/issues/2358>`__, `#2359 <https://github.com/beeware/toga/issues/2359>`__, `#2363 <https://github.com/beeware/toga/issues/2363>`__, `#2367 <https://github.com/beeware/toga/issues/2367>`__, `#2368 <https://github.com/beeware/toga/issues/2368>`__, `#2369 <https://github.com/beeware/toga/issues/2369>`__, `#2370 <https://github.com/beeware/toga/issues/2370>`__, `#2371 <https://github.com/beeware/toga/issues/2371>`__, `#2375 <https://github.com/beeware/toga/issues/2375>`__, `#2376 <https://github.com/beeware/toga/issues/2376>`__

0.4.1 (2023-12-21)
==================

Features
--------

* Toga images can now be created from (and converted to) PIL images. (`#2142 <https://github.com/beeware/toga/issues/2142>`__)
* A wider range of command shortcut keys are now supported on WinForms. (`#2198 <https://github.com/beeware/toga/issues/2198>`__)
* Most widgets with flexible sizes now default to a minimum size of 100 CSS pixels. An explicit size will still override this value. (`#2200 <https://github.com/beeware/toga/issues/2200>`__)
* OptionContainer content can now be constructed using ``toga.OptionItem`` objects. (`#2259 <https://github.com/beeware/toga/issues/2259>`__)
* An OptionContainer widget was added for iOS. (`#2259 <https://github.com/beeware/toga/issues/2259>`__)
* Apps can now specify platform-specific icon resources by appending the platform name (e.g., ``-macOS`` or ``-windows``) to the icon filename. (`#2260 <https://github.com/beeware/toga/issues/2260>`__)
* Images can now be created from the native platform representation of an image, without needing to be transformed to bytes. (`#2263 <https://github.com/beeware/toga/issues/2263>`__)

Bugfixes
--------

* TableViews on macOS will no longer crash if a drag operation is initiated from inside the table. (`#1156 <https://github.com/beeware/toga/issues/1156>`__)
* Separators before and after command sub-groups are now included in menus. (`#2193 <https://github.com/beeware/toga/issues/2193>`__)
* The web backend no longer generates a duplicate title bar. (`#2194 <https://github.com/beeware/toga/issues/2194>`__)
* The web backend is now able to display the About dialog on first page load. (`#2195 <https://github.com/beeware/toga/issues/2195>`__)
* The testbed is now able to run on macOS when the user running the tests has the macOS display setting "Prefer tabs when opening documents" set to "Always". (`#2208 <https://github.com/beeware/toga/issues/2208>`__)
* Compliance with Apple's HIG regarding the naming and shortcuts for the Close and Close All menu items was improved. (`#2214 <https://github.com/beeware/toga/issues/2214>`__)
* Font handling on older versions of iOS has been corrected. (`#2265 <https://github.com/beeware/toga/issues/2265>`__)
* ImageViews with ``flex=1`` will now shrink to fit if the image is larger than the available space. (`#2275 <https://github.com/beeware/toga/issues/2275>`__)

Backward Incompatible Changes
-----------------------------

* The ``toga.Image`` constructor now takes a single argument (``src``); the ``path`` and ``data`` arguments are deprecated. (`#2142 <https://github.com/beeware/toga/issues/2142>`__)
* The use of Caps Lock as a keyboard modifier for commands was removed. (`#2198 <https://github.com/beeware/toga/issues/2198>`__)
* Support for macOS release prior to Big Sur (11) has been dropped. (`#2228 <https://github.com/beeware/toga/issues/2228>`__)
* When inserting or appending a tab to an OptionContainer, the ``enabled`` argument must now be provided as a keyword argument. The name of the first argument has been also been renamed (from ``text`` to ``text_or_item``); it should generally be passed as a positional, rather than keyword argument. (`#2259 <https://github.com/beeware/toga/issues/2259>`__)
* The use of synchronous ``on_result`` callbacks on dialogs and ``Webview.evaluate_javascript()`` calls has been deprecated. These methods should be used in their asynchronous form. (`#2264 <https://github.com/beeware/toga/issues/2264>`__)

Documentation
-------------

* Documentation for ``toga.Key`` was added. (`#2199 <https://github.com/beeware/toga/issues/2199>`__)
* Some limitations on App presentation imposed by Wayland have been documented. (`#2255 <https://github.com/beeware/toga/issues/2255>`__)

Misc
----

* `#2201 <https://github.com/beeware/toga/issues/2201>`__, `#2204 <https://github.com/beeware/toga/issues/2204>`__, `#2215 <https://github.com/beeware/toga/issues/2215>`__, `#2216 <https://github.com/beeware/toga/issues/2216>`__, `#2219 <https://github.com/beeware/toga/issues/2219>`__, `#2222 <https://github.com/beeware/toga/issues/2222>`__, `#2224 <https://github.com/beeware/toga/issues/2224>`__, `#2226 <https://github.com/beeware/toga/issues/2226>`__, `#2230 <https://github.com/beeware/toga/issues/2230>`__, `#2235 <https://github.com/beeware/toga/issues/2235>`__, `#2240 <https://github.com/beeware/toga/issues/2240>`__, `#2246 <https://github.com/beeware/toga/issues/2246>`__, `#2249 <https://github.com/beeware/toga/issues/2249>`__, `#2256 <https://github.com/beeware/toga/issues/2256>`__, `#2257 <https://github.com/beeware/toga/issues/2257>`__, `#2261 <https://github.com/beeware/toga/issues/2261>`__, `#2264 <https://github.com/beeware/toga/issues/2264>`__, `#2267 <https://github.com/beeware/toga/issues/2267>`__, `#2269 <https://github.com/beeware/toga/issues/2269>`__, `#2270 <https://github.com/beeware/toga/issues/2270>`__, `#2271 <https://github.com/beeware/toga/issues/2271>`__, `#2272 <https://github.com/beeware/toga/issues/2272>`__, `#2283 <https://github.com/beeware/toga/issues/2283>`__, `#2284 <https://github.com/beeware/toga/issues/2284>`__, `#2287 <https://github.com/beeware/toga/issues/2287>`__, `#2294 <https://github.com/beeware/toga/issues/2294>`__

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
