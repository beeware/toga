:tocdepth: 2

===============
Release History
===============

.. towncrier release notes start

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
