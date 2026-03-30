# API reference

## Key {: id="api-status-key" }
|                        |                                                          |
|------------------------|----------------------------------------------------------|
| {{ partly_supported }} | Partly supported: functionality or testing is incomplete |
| {{ fully_supported }}  | Fully supported                                          |

<!-- rumdl-disable MD013 -->
{% for category in [
	"Application components",
	"Widgets",
	"Container widgets",
	"Style",
	"Data representation",
	"Resources",
	"Hardware",
] %}
## {{ category }} { .api-reference }

{{ api_table(category) }}

{% endfor %}
