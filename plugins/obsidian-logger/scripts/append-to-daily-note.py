#!/usr/bin/env python3

"""
Append Claude Code session summary to Obsidian Daily Note
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def load_config():
    """Load configuration from config.json"""
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / 'config.json'
    example_config_path = script_dir.parent / 'config.example.json'

    if not config_path.exists():
        print(f'Error: config.json not found.', file=sys.stderr)
        print(f'Please copy {example_config_path} to config.json and configure it.', file=sys.stderr)
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Validate required fields
    if not config.get('obsidianVaultPath'):
        print('Error: obsidianVaultPath is required in config.json', file=sys.stderr)
        sys.exit(1)

    return config


def get_current_date(date_format='YYYY-MM-DD'):
    """Get current date in specified format"""
    now = datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)

    return (date_format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day))


def get_timestamp():
    """Get current timestamp"""
    now = datetime.now()
    return now.strftime('%Y/%m/%d %H:%M:%S')


def get_working_directory():
    """Get working directory"""
    try:
        return os.environ.get('PWD', os.getcwd())
    except Exception:
        return 'Unknown'


def get_git_branch():
    """Get current git branch"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def create_session_summary(config, conversation_summary):
    """Create session summary"""
    timestamp = get_timestamp()
    working_dir = get_working_directory()
    git_branch = get_git_branch()

    summary = config['templateHeader'].replace('{{timestamp}}', timestamp)

    if config.get('includeWorkingDirectory', False):
        summary += f"**Working Directory:** `{working_dir}`\n\n"

    if config.get('includeGitBranch', False) and git_branch:
        summary += f"**Git Branch:** `{git_branch}`\n\n"

    summary += conversation_summary or '(No summary provided)'
    summary += '\n\n---\n'

    return summary


def get_daily_note_path(config):
    """Get Daily Note path"""
    date_str = get_current_date(config.get('dateFormat', 'YYYY-MM-DD'))
    daily_notes_dir = Path(config['obsidianVaultPath']) / config.get('dailyNotesPath', 'Daily Notes')

    # Ensure directory exists
    daily_notes_dir.mkdir(parents=True, exist_ok=True)

    return daily_notes_dir / f'{date_str}.md'


def append_to_daily_note(config, summary):
    """Append to Daily Note"""
    daily_note_path = get_daily_note_path(config)

    # Create file if it doesn't exist
    if not daily_note_path.exists():
        date_str = get_current_date(config.get('dateFormat', 'YYYY-MM-DD'))
        initial_content = f'# {date_str}\n\n'
        daily_note_path.write_text(initial_content, encoding='utf-8')

    # Append summary
    with open(daily_note_path, 'a', encoding='utf-8') as f:
        f.write(summary)

    print(f'✓ Session summary appended to: {daily_note_path}')


def main():
    """Main function"""
    try:
        config = load_config()

        # Get conversation summary from stdin or command line arguments
        if len(sys.argv) > 1:
            conversation_summary = ' '.join(sys.argv[1:])
        else:
            # Try to read from stdin
            try:
                if not sys.stdin.isatty():
                    conversation_summary = sys.stdin.read().strip()
                else:
                    conversation_summary = 'Claude Code session completed.'
            except Exception:
                conversation_summary = 'Claude Code session completed.'

        summary = create_session_summary(config, conversation_summary)
        append_to_daily_note(config, summary)

    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
