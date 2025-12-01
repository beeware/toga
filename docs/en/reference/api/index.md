# API Reference

{% for category in [
	"Core application components",
	"General widgets",
	"Layout widgets",
	"Resources",
	"Hardware",
] %}
## {{ category }} { .api-reference }

{{ api_table(category) }}

{% endfor %}
