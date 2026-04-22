"""
Minimal reproduction case demonstrating non-interactive desktop sessions.

Requires:
    - .NET Desktop Runtime 10
    - pythonnet (pip install pythonnet) in a Python 3.13 virtual environment.
"""

import sys
from pathlib import Path

import clr_loader
from pythonnet import set_runtime

runtime_json = Path(__file__).parent / "runtime.json"
runtime_json.write_text("""
{
  "runtimeOptions": {
    "tfm": "net10.0-windows",
    "frameworks": [
      {
        "name": "Microsoft.NETCore.App",
        "version": "10.0.0"
      },
      {
        "name": "Microsoft.WindowsDesktop.App",
        "version": "10.0.0"
      }
    ]
  }
}
""")
set_runtime(clr_loader.get_coreclr(runtime_config=runtime_json))

import clr  # noqa: E402

clr.AddReference("System.Windows.Forms")

import System.Windows.Forms as WinForms  # noqa: E402


def main():
    # Create and show a form
    form = WinForms.Form()
    form.Text = "Interactive Desktop Test"
    form.Show()

    # Process pending Windows messages so the form is fully realized
    WinForms.Application.DoEvents()

    # Try to activate the form
    form.Activate()
    WinForms.Application.DoEvents()

    # Check if the window manager recognizes an active form
    active = WinForms.Form.ActiveForm
    print(f"Form.Visible:         {form.Visible}")
    print(f"Form.IsHandleCreated: {form.IsHandleCreated}")
    print(f"Form.ActiveForm:      {active}")
    print()

    if active is not None:
        print("RESULT: Interactive desktop session detected.")
        print("        Form.ActiveForm returned the active form.")
        rc = 0
    else:
        print("RESULT: Non-interactive session detected.")
        print("        Form.ActiveForm returned null despite a visible form.")
        print("        Window activation is not functional in this environment.")
        rc = 1

    form.Close()
    form.Dispose()
    return rc


if __name__ == "__main__":
    sys.exit(main())
