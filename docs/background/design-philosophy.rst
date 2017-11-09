.. _design-philosophy:

=================
Design Philosophy
=================

.. note::
    These docs are still very much a WIP, and are mostly cobbled together from
    conversations with the Core Team members and Project Founder. They are not 
    complete and you should feel free to edit or add to them.

Data-Driven Widgets
-------------------

The "grand vision", such that it is, is that the public interface for the Tree
and Table widgets don't have any data manipulation APIs natively. Instead, a
Tree/Table visualizes a data source, and the data source can be manipulated.
We've (internally) got a :code:`ListDataSource` to wrap lists/tuples; and a
:code:`DictDataSource` to wrap dictionaries. But that's really just defining a
general "manipulation of data" interface; any object that provides the same
basic interface should be usable by a Tree/Table. So far, we've been focussing
on the "must have" methods - i.e., you have to have an :code:`insert(n, data)`
method to be able to add new data to a list/dict. But once you've got that, you
should be able to build any other list-like or dict-like method using those
primitives.

So - append, prepend, push, pop all become possible.

The end goal - yes, :code:`ListDataSource` should be a superset of the List API;
:code:`DictDataSource` should be a superset of Dict. As for the widgets
themselves - there are three layers to consider. There's the interface (the
public API), the implementation (the internal platform API) and the native (the
actual native widget(s) on the screen. The interface layer shouldn't have any
data manipulation methods - no add/remove/insert - because at the interface
layer, you're visualizing a data source. The implementation layer needs to
implement the primitives - like insert and remove - so that the underlying
native widgets can be created and displayed. But that collection of primitives
is only exposed so that the implementation, as a listener on the data source,
can reflect changes to the data source.
