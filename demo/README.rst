Toga Demo
=========

A demonstration of the capabilities of the `Toga widget toolkit`_.

**Toga requires Python 3**

.. _Toga widget toolkit: https://beeware.org/toga

Quickstart
----------

For details of Toga's pre-requisites, see the `Toga project on GitHub`_.

Once those pre-requisites have been met, in your virtualenv, install Toga Demo,
and then run it::

    $ pip install toga-demo
    $ toga-demo

This will pop up a GUI window.

If you have cloned the toga repository, install the dependent packages in your virtualenv::

    $ cd toga
    $ pip install -e ./core

Then install the platform specific code::

    $ pip install -e ./cocoa      # macOS
    $ pip install -e ./gtk        # Linux
    $ pip install -e ./winforms   # Windows

Finally navigate to the demo directory and run the application::

    $ cd demo
    $ python -m toga_demo

.. _Toga project on Github: https://github.com/beeware/toga

Community
---------

Toga Demo is part of the `BeeWare suite`_. You can talk to the community through:

* `@beeware@fosstodon.org on Mastodon`_
* `Discord`_
* The Toga `Github Discussions forum`_

We foster a welcoming and respectful community as described in our
`BeeWare Community Code of Conduct`_.

.. _BeeWare suite: https://beeware.org
.. _@beeware@fosstodon.org on Mastodon: https://fosstodon.org/@beeware
.. _Discord: https://beeware.org/bee/chat/
.. _Github Discussions forum: https://github.com/beeware/toga/discussions
.. _BeeWare Community Code of Conduct: https://beeware.org/community/behavior/

Contributing
------------

If you experience problems with Toga Demo, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls
