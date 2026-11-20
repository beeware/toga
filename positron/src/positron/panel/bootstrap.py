from __future__ import annotations

from pathlib import Path

from ..base import BasePositronBootstrap

TEMPLATE_PATH = Path(__file__).parent / "templates"


class PanelPositronBootstrap(BasePositronBootstrap):
    def app_source(self) -> str:
        return self.templated_content(TEMPLATE_PATH / "app.py")

    def pyproject_table_briefcase_app_extra_content(self):
        return """
requires = [
    "panel>=1.9.0,<2",
]
test_requires = [
{% if cookiecutter.test_framework == "pytest" %}
    "pytest",
{% endif %}
]
"""

    def post_generate(self, base_path: Path):
        app_path = base_path / "src" / self.context["module_name"]

        # App files
        for template_name in ["panel.py"]:
            self.templated_file(
                TEMPLATE_PATH / template_name,
                app_path,
                module_name=self.context["module_name"],
            )
