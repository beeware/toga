=======
Android
=======

The Toga backend for Android is `toga-android
<https://github.com/beeware/toga/tree/main/android>`__.

Platform details
================

Prerequisites
-------------

``toga-android`` requires Android SDK 24 (Android 7 / Nougat) or newer.

Installation
------------

``toga-android`` must be manually installed into an Android project; The recommended
approach for deploying ``toga-android`` is to use `Briefcase
<https://briefcase.readthedocs.org>`__ to package your app.

Implementation details
----------------------

The ``toga-android`` backend uses the `Android Java API
<https://developer.android.com/reference>`__, with `Material3 widgets
<https://m3.material.io>`__. It uses `Chaquopy <https://chaquo.com/chaquopy/>`__ to
provide a bridge to the native Android Java libraries and implement Java interfaces from
Python.

Platform-specific APIs
======================

Activities and Intents
----------------------

On Android, some interactions are managed using Activities, which are started using
Intents.

Android's implementation of the :any:`toga.App` class includes the method
:meth:`~toga_android.App.start_activity()`, which can be used to start an activity.

.. py:method:: toga_android.App.start_activity(self, activity, *options, on_complete=None)

   Start a native Android activity.

   :param activity: The ``android.content.Intent`` instance to start
   :param options: Any additional arguments to pass to the native
       ``android.app.Activity.startActivityForResult()`` call.
   :param on_complete: A callback to invoke when the activity completes. The callback
       will be invoked with 2 arguments: the result code, and the result data.

To use this method, instantiate an instance of ``android.content.Intent``; optionally,
provide additional arguments, and a callback that will be invoked when the activity
completes. For example, to dial a phone number with the ``Intent.ACTION_DIAL`` intent::

    from android.content import Intent
    from android.net import Uri

    intent = new Intent(Intent.ACTION_DIAL)
    intent.setData(Uri.parse("tel:0123456789"))

    def number_dialed(result, data):
        # result is the status code (e.g., Activity.RESULT_OK)
        # data is the value returned by the activity.
        ...

    # Assuming your toga.App app instance is called `app`
    app._impl.start_activity(intent, on_complete=number_dialed)
