=======
Android
=======

The Toga backend for Android is `toga-android
<https://github.com/beeware/toga/tree/main/android>`__.

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

``toga-android`` uses the Android Java APIs to build apps. It uses `Chaquopy
<https://chaquo.com/chaquopy/>`__ to provide a bridge to the native Android Java
libraries and implement Java interfaces from Python.
