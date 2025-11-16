# cc-marketplace

kadoppe's Claude Code Plugin Marketplace

## Overview

This repository is a marketplace that provides custom plugins for Claude Code.

## Available Plugins

### obsidian-logger

A plugin that automatically logs Claude Code work sessions to Obsidian Daily Notes. When a session ends, it uses a Stop hook to automatically append the work summary to the Daily Note in your Obsidian vault.

- **Version**: 0.1.0
- **Features**: Automatic logging via Stop hook
- **Details**: [obsidian-logger/README.md](./obsidian-logger/README.md)

## Installation

### 1. Add the Marketplace

Run the following command in Claude Code to add this marketplace:

```bash
/plugin marketplace add /Users/kadoppe/Sources/github.com/kadoppe/cc-marketplace
```

Or, if cloned from GitHub:

```bash
/plugin marketplace add ./cc-marketplace
```

### 2. Install a Plugin

```bash
/plugin install obsidian-logger@cc-marketplace
```

### 3. Verify Installed Plugins

```bash
/plugin list
```

## Development

### Adding a New Plugin

1. Create a new plugin directory inside the `plugins/` directory:

```bash
mkdir -p plugins/my-new-plugin/.claude-plugin
cd plugins/my-new-plugin
```

2. Create `.claude-plugin/plugin.json` to define the plugin manifest

3. Add necessary components (commands, agents, skills, scripts, etc.) to the plugin root

4. Add plugin information to `.claude-plugin/marketplace.json`

### Updating a Plugin

When you update a plugin:

1. Uninstall the plugin:
   ```bash
   /plugin uninstall plugin-name@cc-marketplace
   ```

2. Reinstall:
   ```bash
   /plugin install plugin-name@cc-marketplace
   ```

## Marketplace Structure

```
cc-marketplace/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace metadata
├── README.md                 # This file
├── .gitignore                # Git exclusion settings
└── plugins/
    └── obsidian-logger/      # Plugin
        ├── .claude-plugin/
        │   └── plugin.json   # Plugin manifest
        ├── hooks/
        │   └── hooks.json    # Hook configuration
        ├── scripts/          # Scripts
        │   └── append-to-daily-note.py  # Main processing
        ├── config.example.json  # Sample configuration file
        └── README.md         # Plugin documentation
```

## License

MIT

## Author

kadoppe
