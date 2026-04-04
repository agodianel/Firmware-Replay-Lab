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
    # Import here so dash is only required when actually using the UI
    from ui.app import create_app

    app = create_app(bundle_dir=bundle_dir)

    if not debug:
        Timer(1.5, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()

    app.run(debug=debug, port=port)
