.. _philosophy:

=========
Why Toga?
=========

Toga isn't the world's first widget toolkit - there are dozens of other
options. So why build a new one?

Native widgets - not themes
---------------------------

Toga uses native system widgets, not themes. When you see a Toga app running,
it doesn't just *look* like a native app - it *is* a native app. Applying an
operating system-inspired theme over the top of a generic widget set is an
easy way for a developer to achieve a cross-platform goal, but it leaves the
end user with the mess.

It's easy to spot apps that have been built using themed widget sets - they're
the ones that don't behave quite like any other app. Widgets don't look
*quite* right, or there's a menu bar on a window in an OS X app. Themes can
get quite close - but there are always tell-tale signs.

On top of that, native widgets are always faster than a themed generic widget.
After all, you're using native system capability that has been tuned and
optimized, not a drawing engine that's been layered on top of a generic widget.

Abstract the broad concepts
---------------------------

It's not enough to just look like a native app, though - you need to *feel*
like a native app as well.

A "Quit" option under a "File" menu makes sense if you're writing a Windows
app - but it's completely out of place if you're on OS X - the Quit option
should be under the application menu.

And besides - why did the developer have to code the location of a Quit option
anyway? Every app in the world has to have a quit option, so why doesn't the
widget toolkit provide a quit option pre-installed, out of the box?

Although Toga uses 100% native system widgets, that doesn't mean Toga is just
a wrapper around system widgets. Wherever possible, Toga attempts to abstract
the broader concepts underpinning the construction of GUI apps, and build an
API for *that*. So - every Toga app has the basic set of menu options you'd
expect of every app - Quit, About, and so on - all in the places you'd expect
to see them in a native app.

When it comes to widgets, sometimes the abstraction is simple - after all, a
button is a button, no matter what platform you're on. But other widgets may
not be exposed so literally. What the Toga API aims to expose is a set of
mechanisms for achieving UI goals, not a literal widget set.

Python native
-------------

Most widget toolkits start their life as a C or C++ layer, which is then
wrapped by other languages. As a result, you end up with APIs that taste
like C or C++.

Toga has been designed from the ground up to be a Python native widget
toolkit. This means the API is able to exploit language level features like
generators and context managers in a way that a wrapper around a C library
wouldn't be able to (at least, not easily).

This also means supporting Python 3, and 3 only because that's where the
future of Python is at.

`pip install` and nothing more
------------------------------

Toga aims to be no more than a `pip install` away from use. It doesn't require
the compilation of C extensions. There's no need to install a binary support
library. There's no need to change system paths and environment variables.
Just install it, import it, and start writing (or running) code.

Embrace mobile
--------------

10 years ago, being a cross-platform widget toolkit meant being available
for Windows, OS X and Linux. These days, mobile computing is much more
important. But despite this, there aren't many good options for Python
programming on mobile platforms, and cross-platform mobile coding is still
elusive. Toga aims to correct this.
