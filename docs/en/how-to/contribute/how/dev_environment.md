# Setting up a development environment

{% extends "contribute/how/dev_environment.md" %}

{% block prerequisites_macos %}

View the [macOS prerequisites][macos-prerequisites].

{% endblock %}

{% block prerequisites_linux %}

View the [GTK prerequisites][gtk-prerequisites] or the [Qt prerequisites][qt-prerequisites].

{% endblock %}

{% block prerequisites_windows %}

View the [Windows prerequisites][windows-prerequisites].

{% endblock %}

{% block install_macos_tool %}

```console
(.venv) $ python -m pip install -e ./core -e ./dummy -e ./cocoa -e ./travertino --group dev
```

{% endblock %}

{% block install_linux_tool %}

```console
(.venv) $ python -m pip install -e ./core -e ./dummy -e ./gtk -e ./travertino --group dev
```

{% endblock %}

{% block install_windows_tool %}

```doscon
(.venv) C:\...>python -m  pip install -e ./core -e ./dummy -e ./winforms -e ./travertino --group dev
```

{% endblock %}
