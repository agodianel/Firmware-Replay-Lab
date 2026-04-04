"""UI launcher — starts the Dash app from CLI."""

from __future__ import annotations

import webbrowser
from threading import Timer


def launch_ui(
    bundle_dir: str = "replays/sample-bundles",
    port: int = 8050,
    debug: bool = False,
) -> None:
    """Launch the Dash UI and open the browser."""
    import importlib.util
    import sys
    from pathlib import Path

    # Resolve ui/app.py relative to the repo root
    ui_app_path = Path(__file__).resolve().parents[2].parent / "ui" / "app.py"
    if not ui_app_path.exists():
        # Fallback: try relative to cwd
        ui_app_path = Path("ui/app.py").resolve()

    if not ui_app_path.exists():
        raise FileNotFoundError(f"Cannot find ui/app.py (tried {ui_app_path})")

    spec = importlib.util.spec_from_file_location("ui.app", ui_app_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["ui.app"] = mod
    spec.loader.exec_module(mod)

    app = mod.create_app(bundle_dir=bundle_dir)

    if not debug:
        Timer(1.5, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()

    app.run(debug=debug, port=port)
