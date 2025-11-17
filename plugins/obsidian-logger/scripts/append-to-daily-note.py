#!/usr/bin/env python3

"""Append Claude Code session summary to Obsidian Daily Note."""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import cast


def load_config() -> dict[str, str | bool]:
    """Load configuration from environment variables."""
    # Configuration with prefix CC_PLUGIN_OBSIDIAN_LOGGER_
    vault_path = os.environ.get("CC_PLUGIN_OBSIDIAN_LOGGER_VAULT_PATH")

    # Validate required fields
    if not vault_path:
        print(
            "Error: CC_PLUGIN_OBSIDIAN_LOGGER_VAULT_PATH environment variable is required",
            file=sys.stderr,
        )
        sys.exit(1)

    # vault_path is guaranteed to be str after the check above
    vault_path = cast("str", vault_path)

    # Get other config values with defaults (all are guaranteed to be str)
    daily_notes_path = os.environ.get("CC_PLUGIN_OBSIDIAN_LOGGER_DAILY_NOTES_PATH", "Daily Notes")
    date_format = os.environ.get("CC_PLUGIN_OBSIDIAN_LOGGER_DATE_FORMAT", "YYYY-MM-DD")
    template_header = os.environ.get(
        "CC_PLUGIN_OBSIDIAN_LOGGER_TEMPLATE_HEADER",
        "\n\n## Claude Code Session - {{timestamp}}\n\n",
    )
    include_working_dir = (
        os.environ.get("CC_PLUGIN_OBSIDIAN_LOGGER_INCLUDE_WORKING_DIRECTORY", "true").lower()
        == "true"
    )

    return {
        "obsidianVaultPath": vault_path,
        "dailyNotesPath": daily_notes_path,
        "dateFormat": date_format,
        "templateHeader": template_header,
        "includeWorkingDirectory": include_working_dir,
    }


def get_current_date(date_format: str = "YYYY-MM-DD") -> str:
    """Get current date in specified format."""
    now = datetime.now(tz=timezone.utc).astimezone()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)

    return date_format.replace("YYYY", year).replace("MM", month).replace("DD", day)


def get_timestamp() -> str:
    """Get current timestamp."""
    now = datetime.now(tz=timezone.utc).astimezone()
    return now.strftime("%H:%M:%S")


def get_working_directory() -> str:
    """Get working directory."""
    try:
        return os.environ.get("PWD") or str(Path.cwd())
    except OSError:
        return "Unknown"


def create_session_summary(config: dict[str, str | bool], conversation_summary: str) -> str:
    """Create session summary."""
    timestamp = get_timestamp()
    working_dir = get_working_directory()

    summary = str(config["templateHeader"]).replace("{{timestamp}}", timestamp)

    if config.get("includeWorkingDirectory", False):
        summary += f"**Working Directory:** `{working_dir}`\n\n"

    summary += conversation_summary or "(No summary provided)"
    return summary + "\n\n---\n"


def get_daily_note_path(config: dict[str, str | bool]) -> Path:
    """Get Daily Note path."""
    date_str = get_current_date(str(config.get("dateFormat", "YYYY-MM-DD")))
    daily_notes_dir = Path(str(config["obsidianVaultPath"])) / str(
        config.get("dailyNotesPath", "Daily Notes")
    )

    # Ensure directory exists
    daily_notes_dir.mkdir(parents=True, exist_ok=True)

    return daily_notes_dir / f"{date_str}.md"


def append_to_daily_note(config: dict[str, str | bool], summary: str) -> None:
    """Append summary to Daily Note."""
    daily_note_path = get_daily_note_path(config)

    # Create file if it doesn't exist
    if not daily_note_path.exists():
        date_str = get_current_date(str(config.get("dateFormat", "YYYY-MM-DD")))
        initial_content = f"# {date_str}\n\n"
        daily_note_path.write_text(initial_content, encoding="utf-8")

    # Append summary
    with daily_note_path.open("a", encoding="utf-8") as f:
        f.write(summary)

    print(f"✓ Session summary appended to: {daily_note_path}")


def main() -> None:
    """Run the main script logic."""
    try:
        config = load_config()

        # Get conversation summary from stdin or command line arguments
        if len(sys.argv) > 1:
            conversation_summary = " ".join(sys.argv[1:])
        else:
            # Try to read from stdin
            try:
                if not sys.stdin.isatty():
                    conversation_summary = sys.stdin.read().strip()
                else:
                    conversation_summary = "Claude Code session completed."
            except OSError:
                conversation_summary = "Claude Code session completed."

        summary = create_session_summary(config, conversation_summary)
        append_to_daily_note(config, summary)

    except (OSError, KeyError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
