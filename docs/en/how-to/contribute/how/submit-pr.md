# Submitting a pull request

{% extends "contribute/how/submit-pr.md" %}

{% block end_matter %}

{% if config.extra.website %}

Your pull request may require additional content, such as a [change note](change-note.md), before it can be [reviewed](../next/pr-review.md).

{% else %}

As part of submitting a pull request, you'll need to include a [change note](change-note.md) before it can be [reviewed](../next/pr-review.md).

{% endif %}

{% endblock %}
