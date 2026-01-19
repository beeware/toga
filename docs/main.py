# Macros module for MkDocs-Macros
# For more info: https://mkdocs-macros-plugin.readthedocs.io/en/latest/macros/

from collections import defaultdict
from pathlib import Path

import yaml
from tabulate import tabulate


def slugify(string, sep="-"):
    return string.lower().replace(" ", sep)


PLATFORMS_MAPPING = {
    "cocoa": "macOS",
    "gtk": "Linux (GTK)",
    "qt": "Linux (Qt)",
    "winforms": "Windows",
    "iOS": "iOS",
    "android": "Android",
    "web": "Web",
    "textual": "Terminal",
}

with Path("docs/en/reference/data/apis_by_platform.yaml").open() as file:
    api_data = yaml.safe_load(file)

APIS_BY_NAME = {}
APIS_BY_CATEGORY = defaultdict(list)

for category_name, category_contents in api_data.items():
    category_path = Path(category_contents.pop("path", slugify(category_name)))
    for component_name, component in category_contents.items():
        file_name = component.get("file_name", slugify(component_name, sep=""))
        path = category_path / f"{file_name}.md"
        if not (Path("docs/en/reference/api") / path).is_file():
            # It's a directory
            path = category_path / f"{file_name}/index.md"

        unsupported = component.get("unsupported", [])
        beta = component.get("beta", [])
        for backend in unsupported + beta:
            if backend not in PLATFORMS_MAPPING:
                raise ValueError(f"Unrecognized backend {backend}")

        platform_support = {
            platform: "" if backend in unsupported else "○" if backend in beta else "●"
            for backend, platform in PLATFORMS_MAPPING.items()
        }

        api = {
            "link": f"[{component_name}]({path}){{: .component-name }}",
            "description": component["description"],
            "platforms": platform_support,
            "display": component.get("display", "tabs"),
        }

        APIS_BY_NAME[component_name] = api
        APIS_BY_CATEGORY[category_name].append(api)


def component_support(name, width, alt_file):
    """Render component's support by platform, as a table or tabbed view, as needed."""
    component = APIS_BY_NAME[name]

    if component["display"] == "table":
        return (
            "Availability ([Key][api-status-key])\n{: #availability-title }\n\n"
            + tabulate([component["platforms"]], headers="keys", tablefmt="github")
        )
    elif component["display"] == "tabs":
        return component_tab_view(name, component, width, alt_file)
    else:
        return ""


def component_tab_view(name, component, width, alt_file):
    """Render component's support by platform as a tabbed view."""
    slug = alt_file if alt_file else slugify(name, sep="")
    tabs = []
    for (platform, status), backend in zip(
        # Zip in the keys of PLATFORM_MAPPING to have the backend name.
        component["platforms"].items(),
        PLATFORMS_MAPPING,
        strict=True,
    ):
        status_marker = {
            # Full support
            "●": "",
            # Beta support (β)
            "○": "^&beta;^",
            # Not supported (❌)
            "": " ^&#x274C;^",
        }[status]

        if not status:
            content = "Not supported"
        else:
            file_name = f"{slug}-{backend}.png"
            if Path(f"docs/en/reference/images/{file_name}").is_file():
                content = (
                    f"![{name} on {platform}](/reference/images/{file_name})"
                    f'{{ width="{width}" }}\n\n'
                    "/// caption\n\n///\n\n"
                )
            else:
                content = "Screenshot not available"

        tabs.append(f"/// tab | {platform}{status_marker}\n\n{content}\n\n///")

    return "\n\n".join(tabs)


def define_env(env):
    @env.macro
    def api_table(category):
        """Render table of a category of APIs for the reference page."""
        rows = [
            {
                "Component": f"{component['link']}<br>{component['description']}",
                **component["platforms"],
            }
            for component in APIS_BY_CATEGORY[category]
        ]
        return tabulate(rows, headers="keys", tablefmt="github")

    @env.macro
    def component_header(name, width=None, alt_file=None):
        """Render top of component page: title, description, and platform support."""
        component = APIS_BY_NAME[name]
        return "\n\n".join(
            [
                f"# {name}",
                component["description"],
                component_support(name, width=width, alt_file=alt_file),
            ]
        )
