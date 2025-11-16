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

### 2. Create Configuration File

Create a `config.json` file in the plugin directory:

```bash
cd ~/.claude/plugins/obsidian-logger
cp config.example.json config.json
```

### 3. Edit Configuration File

Edit `config.json` to configure your Obsidian vault path and other settings:

```json
{
  "obsidianVaultPath": "/Users/yourusername/Documents/ObsidianVault",
  "dailyNotesPath": "Daily Notes",
  "dateFormat": "YYYY-MM-DD",
  "templateHeader": "\n\n## Claude Code Session - {{timestamp}}\n\n",
  "includeWorkingDirectory": true,
  "includeGitBranch": true
}
```

#### Configuration Options

- `obsidianVaultPath`: Absolute path to your Obsidian vault (**required**)
- `dailyNotesPath`: Path to Daily Notes folder (relative to vault)
- `dateFormat`: Date format (default: `YYYY-MM-DD`)
- `templateHeader`: Header template for session records
- `includeWorkingDirectory`: Whether to record working directory (default: `true`)
- `includeGitBranch`: Whether to record Git branch (default: `true`)

### 4. Grant Execute Permission to Script

```bash
chmod +x ~/.claude/plugins/obsidian-logger/scripts/append-to-daily-note.py
```

## Requirements

- **Python 3.7+** (pre-installed on macOS 12.3 and later)

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
