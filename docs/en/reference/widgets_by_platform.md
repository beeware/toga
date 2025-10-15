# Toga APIs by platform

## Key  {: .widgets_by_platform_key id="api-status-key" }

| {{ partly_supported }} | Partly supported: functionality or testing is incomplete |
|------------------------|----------------------------------------------------------|
| {{ fully_supported }}  | **Fully supported**                                      |

## Core Components {: .widgets_by_platform }

{{ pd_read_csv("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10,11])[pd_read_csv("data/widgets_by_platform.csv")[["Type"]].isin(["Core Component"]).all(axis=1)] | convert_to_md_table }}

## General Widgets {: .widgets_by_platform }

{{ pd_read_csv("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10,11])[pd_read_csv("data/widgets_by_platform.csv")[["Type"]].isin(["General Widget"]).all(axis=1)] | convert_to_md_table }}

## Layout Widgets {: .widgets_by_platform }

{{ pd_read_csv("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10,11])[pd_read_csv("data/widgets_by_platform.csv")[["Type"]].isin(["Layout Widget"]).all(axis=1)] | convert_to_md_table }}

## Hardware {: .widgets_by_platform }

{{ pd_read_csv("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10,11])[pd_read_csv("data/widgets_by_platform.csv")[["Type"]].isin(["Hardware"]).all(axis=1)] | convert_to_md_table }}

## Resources {: .widgets_by_platform }

{{ pd_read_csv("data/widgets_by_platform.csv", na_filter=False, usecols=[2,4,5,6,7,8,9,10,11])[pd_read_csv("data/widgets_by_platform.csv")[["Type"]].isin(["Resource"]).all(axis=1)] | convert_to_md_table }}
