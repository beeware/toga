# Toga APIs by platform

## Key  {: .widgets_by_platform_key id="api-status-key" }

| {{ partly_supported }} | Partly supported: functionality or testing is incomplete |
|------------------------|----|
| {{ fully_supported }}  | **Fully supported** |

## Core Components {: .widgets_by_platform }

<nospell>
{{ pd_read_csv[pd_read_csv("data/widgets_by_platform.csv")[["Type"]("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10])].isin(["Core Component"]).all(axis=1)] | convert_to_md_table }}
</nospell>

## General Widgets {: .widgets_by_platform }

<nospell>
{{ pd_read_csv[pd_read_csv("data/widgets_by_platform.csv")[["Type"]("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10])].isin(["General Widget"]).all(axis=1)] | convert_to_md_table }}
</nospell>

## Layout Widgets {: .widgets_by_platform }

<nospell>
{{ pd_read_csv[pd_read_csv("data/widgets_by_platform.csv")[["Type"]("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10])].isin(["Layout Widget"]).all(axis=1)] | convert_to_md_table }}
</nospell>

## Hardware {: .widgets_by_platform }

<nospell>
{{ pd_read_csv[pd_read_csv("data/widgets_by_platform.csv")[["Type"]("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10])].isin(["Hardware"]).all(axis=1)] | convert_to_md_table }}
</nospell>

## Resources {: .widgets_by_platform }

<nospell>
{{ pd_read_csv[pd_read_csv("data/widgets_by_platform.csv")[["Type"]("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10])].isin(["Resource"]).all(axis=1)] | convert_to_md_table }}
</nospell>
