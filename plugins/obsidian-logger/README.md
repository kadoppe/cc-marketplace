# Obsidian Logger Plugin

A plugin that automatically logs Claude Code work sessions to Obsidian Daily Notes.

## Overview

This plugin automatically appends work summaries to Obsidian Daily Notes using a Stop hook when Claude Code sessions end.

## Features

- **Stop Hook**: Automatically executes when Claude Code ends
- **Daily Note Integration**: Appends work summaries to Daily Notes in your Obsidian vault
- **Flexible Configuration**: Customize vault path, Daily Notes folder, date format, and more
- **Git Information Recording**: Automatically records working directory and Git branch (optional)

## Installation

### 1. Install from Marketplace

```bash
# Add the marketplace (first time only)
/plugin marketplace add /Users/kadoppe/Sources/github.com/kadoppe/cc-marketplace

# Install the plugin
/plugin install obsidian-logger@cc-marketplace
```

## Requirements

- **Python 3.7+** (pre-installed on macOS 12.3 and later)

## Environment Variables

The plugin uses the following environment variables (automatically set from `config.json`):

### Required

- `CC_PLUGIN_OBSIDIAN_LOGGER_VAULT_PATH`: Absolute path to your Obsidian vault

### Optional

- `CC_PLUGIN_OBSIDIAN_LOGGER_DAILY_NOTES_PATH`: Path to Daily Notes folder (relative to vault)
  - Default: `"Daily Notes"`
- `CC_PLUGIN_OBSIDIAN_LOGGER_DATE_FORMAT`: Date format for Daily Note filenames
  - Default: `"YYYY-MM-DD"`
- `CC_PLUGIN_OBSIDIAN_LOGGER_TEMPLATE_HEADER`: Header template for session records
  - Default: `"\n\n## Claude Code Session - {{timestamp}}\n\n"`
  - Use `{{timestamp}}` as a placeholder for the current time
- `CC_PLUGIN_OBSIDIAN_LOGGER_INCLUDE_WORKING_DIRECTORY`: Whether to record working directory
  - Default: `"true"`
  - Accepts: `"true"` or `"false"`

> **Note**: You typically don't need to set these environment variables manually. The plugin automatically reads settings from `config.json` and converts them to environment variables.

## Usage

Once the plugin is installed and configured, work summaries are automatically recorded to Obsidian Daily Notes whenever you end a Claude Code session.

### Recorded Information

- Session timestamp
- Working directory (if enabled in configuration)
- Git branch (if enabled in configuration)
- Work summary

### Example Record

```markdown
## Claude Code Session - 2025/11/16 14:30:15

**Working Directory:** `/Users/kadoppe/projects/my-app`

**Git Branch:** `feature/new-feature`

Created plugin template.

---
```

## Scripts

Core functionality is extracted to the `scripts/` directory:

- `append-to-daily-note.py`: Main script that handles appending to Daily Notes

### Manual Execution

Scripts can also be executed manually:

```bash
# Specify summary as an argument
python3 scripts/append-to-daily-note.py "Work summary"

# Read summary from standard input
echo "Work summary" | python3 scripts/append-to-daily-note.py
```

## Troubleshooting

### Daily Note Not Created

- Check that `obsidianVaultPath` in `config.json` is correct
- Verify you have filesystem write permissions

### Git Branch Not Recorded

- Verify the working directory is a Git repository
- Check that `includeGitBranch` is set to `true` in `config.json`

## Development

### Updating the Plugin

```bash
# Uninstall
/plugin uninstall obsidian-logger@cc-marketplace

# Reinstall
/plugin install obsidian-logger@cc-marketplace
```

### Directory Structure

```
obsidian-logger/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── hooks/
│   └── hooks.json           # Hook configuration
├── scripts/                 # Scripts
│   └── append-to-daily-note.py  # Main processing
├── config.example.json      # Sample configuration file
└── README.md                # This file
```

### About Hook Configuration

This plugin defines a Stop hook in `hooks/hooks.json` as follows:

```json
{
  "Stop": [
    {
      "matcher": ".*",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/append-to-daily-note.py"
        }
      ]
    }
  ]
}
```

`.claude-plugin/plugin.json` references this hooks.json file:

```json
{
  "hooks": "./hooks/hooks.json"
}
```

- **Stop**: Event that executes when Claude Code session ends
- **matcher**: `.*` matches all stop events
- **command**: Executes the script (`${CLAUDE_PLUGIN_ROOT}` is automatically expanded to the plugin's root directory)

## License

MIT

## Author

kadoppe
