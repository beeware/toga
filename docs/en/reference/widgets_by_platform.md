# Toga APIs by platform

## Key  {: .widgets_by_platform_key id="api-status-key" }

| {{ partly_supported }} | Partly supported: functionality or testing is incomplete |
|------------------------|----------------------------------------------------------|
| {{ fully_supported }}  | **Fully supported**                                      |

{% for category in [
	"Core application components",
	"General widgets",
	"Layout widgets",
	"Resources",
	"Hardware",
] %}
## {{ category }} { .widgets_by_platform }

{{ api_table(category, platforms=True) }}

{% endfor %}
