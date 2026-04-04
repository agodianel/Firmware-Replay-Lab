"""Dash application — multi-page app for replay bundle inspection."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dash import Dash, html, dcc, callback, Input, Output, dash_table
import plotly.graph_objects as go

from firmware_replay_lab.bundle import ReplayBundle
from firmware_replay_lab.replay import evaluate_bundle
from firmware_replay_lab.validator import validate_bundle


def _load_bundles(bundle_dir: str) -> dict[str, ReplayBundle]:
    """Load all JSON bundles from a directory."""
    bundles: dict[str, ReplayBundle] = {}
    dirpath = Path(bundle_dir)
    if not dirpath.exists():
        return bundles
    for f in sorted(dirpath.glob("*.json")):
        try:
            bundles[f.name] = ReplayBundle.load_json(f)
        except Exception:
            pass
    return bundles


def create_app(bundle_dir: str = "replays/sample-bundles") -> Dash:
    """Create and configure the Dash application."""
    bundles = _load_bundles(bundle_dir)
    bundle_names = list(bundles.keys())

    app = Dash(
        __name__,
        title="Firmware Replay Lab",
        suppress_callback_exceptions=True,
    )

    app.layout = html.Div([
        html.H1("Firmware Replay Lab", style={"textAlign": "center", "padding": "20px"}),
        html.Div([
            html.Label("Select Bundle:"),
            dcc.Dropdown(
                id="bundle-selector",
                options=[{"label": name, "value": name} for name in bundle_names],
                value=bundle_names[0] if bundle_names else None,
                style={"width": "400px"},
            ),
        ], style={"padding": "10px 20px"}),
        dcc.Tabs(id="tabs", value="overview", children=[
            dcc.Tab(label="Overview", value="overview"),
            dcc.Tab(label="Serial Log", value="logs"),
            dcc.Tab(label="Timeline", value="timeline"),
            dcc.Tab(label="Assertions", value="assertions"),
        ]),
        html.Div(id="tab-content", style={"padding": "20px"}),
    ])

    @callback(
        Output("tab-content", "children"),
        Input("bundle-selector", "value"),
        Input("tabs", "value"),
    )
    def render_tab(bundle_name: str | None, tab: str) -> Any:
        if not bundle_name or bundle_name not in bundles:
            return html.P("No bundle selected.")

        bundle = bundles[bundle_name]

        if tab == "overview":
            return _render_overview(bundle, bundle_name)
        elif tab == "logs":
            return _render_logs(bundle)
        elif tab == "timeline":
            return _render_timeline(bundle)
        elif tab == "assertions":
            return _render_assertions(bundle)
        return html.P("Unknown tab.")

    return app


def _render_overview(bundle: ReplayBundle, name: str) -> Any:
    meta = bundle.metadata
    result = evaluate_bundle(bundle)
    errors = validate_bundle(bundle)
    hard_errors = [e for e in errors if not e.startswith("warning:")]
    warnings = [e for e in errors if e.startswith("warning:")]

    status_color = "#2ecc71" if result.passed else "#e74c3c"
    status_text = "PASS" if result.passed else "FAIL"
    valid_text = "VALID" if not hard_errors else "INVALID"

    return html.Div([
        html.H2(f"Bundle: {name}"),
        html.Div([
            html.Span(
                status_text,
                style={
                    "background": status_color, "color": "white",
                    "padding": "4px 12px", "borderRadius": "4px",
                    "fontWeight": "bold", "marginRight": "10px",
                },
            ),
            html.Span(
                valid_text,
                style={
                    "background": "#3498db" if not hard_errors else "#e67e22",
                    "color": "white", "padding": "4px 12px", "borderRadius": "4px",
                },
            ),
        ], style={"marginBottom": "15px"}),
        html.Table([
            html.Tr([html.Td("Target", style={"fontWeight": "bold"}), html.Td(meta.target)]),
            html.Tr([html.Td("Board", style={"fontWeight": "bold"}), html.Td(meta.board)]),
            html.Tr([html.Td("Firmware", style={"fontWeight": "bold"}), html.Td(meta.firmware_version)]),
            html.Tr([html.Td("Commit", style={"fontWeight": "bold"}), html.Td(meta.commit)]),
            html.Tr([html.Td("Captured", style={"fontWeight": "bold"}), html.Td(meta.captured_at)]),
            html.Tr([html.Td("Log Lines", style={"fontWeight": "bold"}), html.Td(str(len(bundle.serial_log)))]),
            html.Tr([html.Td("Events", style={"fontWeight": "bold"}), html.Td(str(len(bundle.events)))]),
            html.Tr([html.Td("Assertions", style={"fontWeight": "bold"}), html.Td(str(len(bundle.assertions)))]),
        ], style={"borderCollapse": "collapse", "marginBottom": "15px"}),
        html.H3("Notes"),
        html.Ul([html.Li(note) for note in bundle.notes]) if bundle.notes else html.P("No notes."),
        html.H3("Validation"),
        html.Ul([html.Li(e, style={"color": "#e74c3c"}) for e in hard_errors]) if hard_errors else html.P("No errors."),
        html.Ul([html.Li(w, style={"color": "#f39c12"}) for w in warnings]) if warnings else None,
    ])


def _render_logs(bundle: ReplayBundle) -> Any:
    if not bundle.serial_log:
        return html.P("No serial log entries.")

    data = [
        {
            "timestamp_ms": line.timestamp_ms,
            "direction": line.direction,
            "message": line.message,
        }
        for line in bundle.serial_log
    ]

    return html.Div([
        html.H2(f"Serial Log ({len(data)} lines)"),
        dash_table.DataTable(
            data=data,
            columns=[
                {"name": "Timestamp (ms)", "id": "timestamp_ms"},
                {"name": "Direction", "id": "direction"},
                {"name": "Message", "id": "message"},
            ],
            style_cell={"textAlign": "left", "fontFamily": "monospace", "padding": "5px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#f8f9fa"},
            style_data_conditional=[
                {
                    "if": {"filter_query": '{message} contains "ERROR" || {message} contains "PANIC" || {message} contains "fault"'},
                    "backgroundColor": "#fde8e8",
                },
            ],
            page_size=50,
            filter_action="native",
            sort_action="native",
        ),
    ])


def _render_timeline(bundle: ReplayBundle) -> Any:
    if not bundle.events and not bundle.serial_log:
        return html.P("No data for timeline.")

    fig = go.Figure()

    # Plot serial log density
    if bundle.serial_log:
        timestamps = [line.timestamp_ms for line in bundle.serial_log]
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=[1] * len(timestamps),
            mode="markers",
            name="Log Lines",
            marker={"size": 4, "color": "#3498db"},
        ))

    # Plot events
    if bundle.events:
        event_types = sorted(set(e.get("type", "") for e in bundle.events))
        colors = ["#e74c3c", "#f39c12", "#2ecc71", "#9b59b6", "#1abc9c"]
        for i, etype in enumerate(event_types):
            evts = [e for e in bundle.events if e.get("type") == etype]
            fig.add_trace(go.Scatter(
                x=[e.get("timestamp_ms", 0) for e in evts],
                y=[2 + i * 0.3] * len(evts),
                mode="markers+text",
                name=etype,
                marker={"size": 10, "color": colors[i % len(colors)], "symbol": "diamond"},
                text=[e.get("detail", "")[:40] for e in evts],
                textposition="top center",
            ))

    fig.update_layout(
        title="Event Timeline",
        xaxis_title="Time (ms)",
        yaxis_visible=False,
        height=400,
        showlegend=True,
    )

    return html.Div([
        html.H2("Timeline"),
        dcc.Graph(figure=fig),
    ])


def _render_assertions(bundle: ReplayBundle) -> Any:
    if not bundle.assertions:
        return html.P("No assertions defined.")

    result = evaluate_bundle(bundle)
    failure_set = set(result.failures)

    from firmware_replay_lab.replay import _ASSERTION_HANDLERS

    rows = []
    for idx, assertion in enumerate(bundle.assertions):
        kind = assertion.get("kind", "unknown")
        handler = _ASSERTION_HANDLERS.get(kind)
        if handler:
            failure = handler(bundle, assertion)
            status = "FAIL" if failure else "PASS"
            detail = failure or "OK"
        else:
            status = "ERROR"
            detail = f"Unknown kind: {kind}"

        rows.append({
            "index": idx,
            "kind": kind,
            "status": status,
            "detail": detail,
            "config": json.dumps({k: v for k, v in assertion.items() if k != "kind"}),
        })

    return html.Div([
        html.H2(f"Assertions ({len(rows)})"),
        html.Div([
            html.Span(
                f"{sum(1 for r in rows if r['status'] == 'PASS')} passed",
                style={"color": "#2ecc71", "marginRight": "15px", "fontWeight": "bold"},
            ),
            html.Span(
                f"{sum(1 for r in rows if r['status'] != 'PASS')} failed",
                style={"color": "#e74c3c", "fontWeight": "bold"},
            ),
        ], style={"marginBottom": "10px"}),
        dash_table.DataTable(
            data=rows,
            columns=[
                {"name": "#", "id": "index"},
                {"name": "Kind", "id": "kind"},
                {"name": "Status", "id": "status"},
                {"name": "Detail", "id": "detail"},
                {"name": "Config", "id": "config"},
            ],
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#f8f9fa"},
            style_data_conditional=[
                {"if": {"filter_query": '{status} = "PASS"'}, "backgroundColor": "#eafaf1"},
                {"if": {"filter_query": '{status} = "FAIL"'}, "backgroundColor": "#fde8e8"},
                {"if": {"filter_query": '{status} = "ERROR"'}, "backgroundColor": "#fef3e2"},
            ],
        ),
    ])


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
