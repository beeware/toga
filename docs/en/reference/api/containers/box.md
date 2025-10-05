# Box

A generic container for other widgets. Used to construct layouts.

Availability ([Key][api-status-key])  <!-- rumdl-disable-line MD013 -->
{: .availability-title }

{{ pd_read_csv("../../data/widgets_by_platform.csv", na_filter=False, usecols=[4,5,6,7,8,9,10])[pd_read_csv("../../data/widgets_by_platform.csv")[["ComponentName"]].isin(["Box"]).all(axis=1)] | convert_to_md_table }}

## Usage

An empty Box can be constructed without any children, with children added to the box after construction:

```python
import toga

box = toga.Box()

label1 = toga.Label('Hello')
label2 = toga.Label('World')

box.add(label1)
box.add(label2)
```

Alternatively, children can be specified at the time the box is constructed:

```python
import toga

label1 = toga.Label('Hello')
label2 = toga.Label('World')

box = toga.Box(children=[label1, label2])
```

In most apps, a layout is constructed by building a tree of boxes inside boxes, with concrete widgets (such as [`Label`][toga.Label] or [`Button`][toga.Button]) forming the leaf nodes of the tree. Style directives can be applied to enforce a margin around the outside of the box, direction of child stacking inside the box, and background color of the box.

## Reference

::: toga.Box

::: toga.Row

::: toga.Column
