===
iOS
===

The Toga backend for iOS is `toga-iOS
<https://github.com/beeware/toga/tree/main/iOS>`__.

Prerequisites
-------------

``toga-iOS`` requires iOS 12 or newer.

Installation
------------

``toga-iOS`` must be manually installed into an iOS project; The recommended approach
for deploying ``toga-iOS`` is to use `Briefcase <https://briefcase.readthedocs.org>`__
to package your app.

Implementation details
----------------------

``toga-iOS`` uses the iOS UIKit Objective-C APIs to build apps. It uses `Rubicon
Objective-C <https://rubicon-objc.readthedocs.org>`__ to provide a bridge to the native
UIKit libraries from Python.
