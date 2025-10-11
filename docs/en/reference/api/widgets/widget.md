# Widget

The abstract base class of all widgets. This class should not be instantiated directly.

Availability ([Key][api-status-key])  <!-- rumdl-disable-line MD013 -->
{: .availability-title }

{{ pd_read_csv("reference/data/widgets_by_platform.csv", na_filter=False, usecols=[4,5,6,7,8,9,10])[pd_read_csv("reference/data/widgets_by_platform.csv")[["ComponentName"]].isin(["Widget"]).all(axis=1)] | convert_to_md_table }}

## Reference

::: toga.Widget
    options:
        show_if_no_docstring: true

::: toga.widgets.base.StyleT
