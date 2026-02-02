from __future__ import annotations


def validate_path(value: str) -> bool:
    """Validate that the value is a valid path."""
    if not value.startswith("/"):
        raise ValueError("Path must start with a /")
    return True


def templated_content(template_path, template_name, **context):
    """Render a template for `template.name` with the provided context."""
    template = (template_path / f"{template_name}.tmpl").read_text(encoding="utf-8")
    return template.format(**context)


def templated_file(template_path, template_name, output_path, **context):
    """Render a template for `template.name` with the provided context, saving the
    result in `output_path`."""
    (output_path / template_name).write_text(
        templated_content(template_path, template_name, **context), encoding="utf-8"
    )
