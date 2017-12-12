========
Examples
========

This directory contains example code demonstrating each widget defined by
Toga:

* button
* detailedlist
* table
* tree

It also contains working copies of the tutorial code:

* tutorial0
* tutorial1
* tutorial2
* tutorial3

Running the examples
--------------------

Each of the examples should run by installing toga, and running the
application as a Python module::

    $ pip install toga
    $ cd <example name>
    $ python -m <example name>

substituting `<example name>` for the example you want to run.

For developers: Creating new examples
-------------------------------------

This directory also contains a `Cookiecutter
<https://github.com/audreyr/cookiecutter>`__ template for new examples. To
create a new example, run the following from this directory::

    $ pip install cookiecutter
    $ cookiecutter .template

and answer the questions.
