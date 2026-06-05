from pathlib import Path

from microdriver import app as micropython_app

app = micropython_app(content=Path(__file__).parent / "resources")
