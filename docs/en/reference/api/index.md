# API Reference

## Key  {: id="api-status-key" }
|                        |                                                          |
|------------------------|----------------------------------------------------------|
| {{ partly_supported }} | Partly supported: functionality or testing is incomplete |
| {{ fully_supported }}  | **Fully supported**                                      |

{% for category in [
	"Application components",
	"Widgets",
	"Container widgets",
	"Style",
	"Resources",
	"Data sources",
	"Constants and types",
	"Hardware",
] %}
## {{ category }} { .api-reference }

{{ api_table(category) }}

{% endfor %}
