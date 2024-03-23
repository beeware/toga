==============================
Backend implementation details
==============================

Although Toga is a cross-platform toolkit, it is sometimes necessary to invoke
platform-specific logic. These guides provide information on how platform-specific
features map onto the Toga backend API.

Accessing these APIs will result in an application that is no longer cross-platform
(unless you gate the usage of these APIs with ``sys.platform`` or
``toga.platform.current_platform`` checks); however, accessing a backend API may be the
only way to implement a feature that Toga doesn't provide.

For details on how to access the the backend implementations, see the documentation on
:ref:`Toga's three-layer architecture <architecture>`.

.. toctree::
   :maxdepth: 1
   :glob:

   android
   gtk
   iOS
   cocoa
   textual
   web
   winforms
