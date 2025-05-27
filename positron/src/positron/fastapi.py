from __future__ import annotations

from pathlib import Path
from typing import Any

from briefcase.bootstraps import TogaGuiBootstrap


def validate_path(value: str) -> bool:
    if not value.startswith("/"):
        raise ValueError("Path must start with a /")
    return True


def templated_content(template_name: str, **context) -> str:
    template = (
        Path(__file__).parent / f"fastapi_template/{template_name}.tmpl"
    ).read_text(encoding="utf-8")
    return template.format(**context)


def templated_file(template_name: str, output_path: Path, **context) -> None:
    (output_path / template_name).write_text(
        templated_content(template_name, **context), encoding="utf-8"
    )


class FastAPIPositronBootstrap(TogaGuiBootstrap):
    display_name_annotation = "runs a FastAPI backend (local web server)"

    def app_source(self) -> str:
        return templated_content("app.py")

    def pyproject_table_briefcase_app_extra_content(self) -> str:
        return """
requires = [
    "fastapi~=0.110.0",
    "asgiref~=3.7.2",
]
"""

    def extra_context(self, project_overrides: dict[str, str]) -> dict[str, Any] | None:
        return {}

    def post_generate(self, base_path: Path):
        app_path = base_path / "src" / self.context["module_name"]

        self.console.debug("Writing server.py")
        templated_file(
            "server.py",
            app_path,
            module_name=self.context["module_name"],
        )
