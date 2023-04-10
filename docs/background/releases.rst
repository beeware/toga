:tocdepth: 2

===============
Release History
===============

.. towncrier release notes start

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

* Refactored code into multiple repositories, so that users of one backend
  don't have to carry the overhead of other installed platforms

* Corrected a range of bugs, mostly related to problems under Python 3.

0.1.0
=====

Initial public release. Includes:

* A Cocoa (OS X) backend
* A GTK+ backend
* A proof-of-concept Win32 backend
* A proof-of-concept iOS backend
