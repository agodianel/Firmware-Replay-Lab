"""AI summarization — optional LLM-powered analysis of replay bundles.

Usage requires one of:
    - OPENAI_API_KEY env var (for OpenAI)
    - ANTHROPIC_API_KEY env var (for Anthropic)
    - OLLAMA_HOST env var (for local Ollama)

This module never decides pass/fail. It provides advisory summaries only.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

from ..bundle import ReplayBundle


@dataclass
class AISummary:
    provider: str
    model: str
    summary: str
    suggested_assertions: list[str]
    confidence_note: str


def _bundle_to_prompt(bundle: ReplayBundle) -> str:
    """Convert bundle to a prompt for LLM analysis."""
    meta = bundle.metadata
    lines = [
        "Analyze this firmware replay bundle:",
        f"Target: {meta.target}, Board: {meta.board}",
        f"Firmware: {meta.firmware_version}, Commit: {meta.commit}",
        "",
        f"Serial log ({len(bundle.serial_log)} lines):",
    ]
    # Include up to 50 lines for context
    for entry in bundle.serial_log[:50]:
        lines.append(f"  [{entry.timestamp_ms}ms] {entry.message}")
    if len(bundle.serial_log) > 50:
        lines.append(f"  ... ({len(bundle.serial_log) - 50} more lines)")

    if bundle.events:
        lines.append(f"\nEvents ({len(bundle.events)}):")
        for event in bundle.events[:20]:
            lines.append(f"  - {event.get('type', '?')}: {event.get('detail', '')[:80]}")

    if bundle.notes:
        lines.append("\nEngineer notes:")
        for note in bundle.notes:
            lines.append(f"  - {note}")

    lines.append("\nProvide: 1) A short summary of the failure, "
                 "2) Likely root cause, "
                 "3) Suggested replay assertions to add.")
    return "\n".join(lines)


def _get_provider() -> tuple[str, str]:
    """Detect available AI provider. Returns (provider, model)."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic", "claude-sonnet-4-20250514"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai", "gpt-4o-mini"
    if os.environ.get("OLLAMA_HOST"):
        return "ollama", "llama3"
    raise RuntimeError(
        "No AI provider configured. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or OLLAMA_HOST."
    )


def summarize_bundle(bundle: ReplayBundle) -> AISummary:
    """Generate an AI summary of a replay bundle.

    Requires an AI provider to be configured via environment variables.
    This is advisory only — never use this for pass/fail decisions.
    """
    provider, model = _get_provider()
    prompt = _bundle_to_prompt(bundle)

    if provider == "openai":
        return _call_openai(prompt, model)
    elif provider == "anthropic":
        return _call_anthropic(prompt, model)
    elif provider == "ollama":
        return _call_ollama(prompt, model)
    raise RuntimeError(f"Unknown provider: {provider}")


def _call_openai(prompt: str, model: str) -> AISummary:
    """Call OpenAI API via urllib (no third-party dependency)."""
    import urllib.request

    api_key = os.environ["OPENAI_API_KEY"]
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
    }).encode()

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    text = data["choices"][0]["message"]["content"]
    return AISummary(
        provider="openai", model=model, summary=text,
        suggested_assertions=[], confidence_note="Advisory only — not deterministic.",
    )


def _call_anthropic(prompt: str, model: str) -> AISummary:
    """Call Anthropic API via urllib."""
    import urllib.request

    api_key = os.environ["ANTHROPIC_API_KEY"]
    payload = json.dumps({
        "model": model,
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    text = data["content"][0]["text"]
    return AISummary(
        provider="anthropic", model=model, summary=text,
        suggested_assertions=[], confidence_note="Advisory only — not deterministic.",
    )


def _call_ollama(prompt: str, model: str) -> AISummary:
    """Call local Ollama API."""
    import urllib.request

    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
    }).encode()

    req = urllib.request.Request(
        f"{host}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())

    text = data.get("response", "")
    return AISummary(
        provider="ollama", model=model, summary=text,
        suggested_assertions=[], confidence_note="Advisory only — not deterministic.",
    )
