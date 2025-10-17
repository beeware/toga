# Macros module for MkDocs-Macros
# For more info: https://mkdocs-macros-plugin.readthedocs.io/en/latest/macros/

from pathlib import Path

import pandas as pd

ALL_APIS = pd.read_csv(
    "docs/en/reference/data/apis_by_platform.csv",
    quotechar='"',
    comment="#",
    na_filter=False,  # Leave blank cells as empty strings instead of NaN
)
ALL_APIS["Component"] = "[" + ALL_APIS["Name"] + "](" + ALL_APIS["Link"] + ")"
# The "by platform" page is one level higher, so the paths need api/ prepended.
ALL_APIS["Component_from_platforms"] = (
    "[" + ALL_APIS["Name"] + "](api/" + ALL_APIS["Link"] + ")"
)

BACKENDS_MAPPING = {
    "macOS": "cocoa",
    "GTK": "gtk",
    "Windows": "winforms",
    "iOS": "iOS",
    "Android": "android",
    "Web": "web",
    "Terminal": "textual",
}
PLATFORMS = list(BACKENDS_MAPPING)


def component_support(name, width, alt_file):
    """Render component's support by platform, as a table or tabbed view, as needed."""
    selection = ALL_APIS[ALL_APIS["Name"] == name]

    if (display := selection["Display"].item()) == "table":
        return (
            "Availability ([Key][api-status-key])\n{: .availability-title }\n\n"
            + selection[PLATFORMS].to_markdown(index=False, stralign=None)
        )
    elif display == "tabs":
        return component_tab_view(selection, width, alt_file)
    else:
        return ""


def component_tab_view(row, width, alt_file):
    """Render component's support by platform as a tabbed view."""
    name = row["Name"].item()
    slug = alt_file if alt_file else name.lower().replace(" ", "")
    tabs = []
    for platform in PLATFORMS:
        status = row[platform].item()
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
            file_name = f"{slug}-{BACKENDS_MAPPING[platform]}.png"
            if Path(f"docs/en/reference/images/{file_name}").is_file():
                content = (
                    f"![{name} on {platform}](/reference/images/{file_name})"
                    f'{{ width="{width}" }}\n'
                    "/// caption\n///\n"
                )
            else:
                content = "Screenshot not available"

        tabs.append(f"/// tab | {platform}{status_marker}\n{content}\n///")

    return "\n".join(tabs)


def define_env(env):
    @env.macro
    def api_table(category, platforms=False):
        """Render table of a category of APIs for the two reference pages."""
        selection = ALL_APIS[ALL_APIS["Category"] == category]
        if platforms:
            return selection[["Component_from_platforms", *PLATFORMS]].to_markdown(
                index=False, headers=["Component", *PLATFORMS], stralign=None
            )
        else:
            return selection[["Component", "Description"]].to_markdown(
                index=False, stralign=None
            )

    @env.macro
    def component_header(name, width=None, alt_file=None):
        """Render top of component page: title, description, and platform support."""
        selection = ALL_APIS[ALL_APIS["Name"] == name]
        description = selection["Description"].item()
        return "\n\n".join(
            [
                f"# {name}",
                description,
                component_support(name, width=width, alt_file=alt_file),
            ]
        )
