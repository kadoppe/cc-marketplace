#!/usr/bin/env node

/**
 * Append Claude Code session summary to Obsidian Daily Note
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Load configuration
function loadConfig() {
  const configPath = path.join(__dirname, '..', 'config.json');
  const exampleConfigPath = path.join(__dirname, '..', 'config.example.json');

  if (!fs.existsSync(configPath)) {
    console.error('Error: config.json not found.');
    console.error(`Please copy ${exampleConfigPath} to config.json and configure it.`);
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

  // Validate required fields
  if (!config.obsidianVaultPath) {
    console.error('Error: obsidianVaultPath is required in config.json');
    process.exit(1);
  }

  return config;
}

// Get current date in specified format
function getCurrentDate(format = 'YYYY-MM-DD') {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day);
}

// Get current timestamp
function getTimestamp() {
  const now = new Date();
  return now.toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
}

// Get working directory
function getWorkingDirectory() {
  try {
    return process.env.PWD || process.cwd();
  } catch (error) {
    return 'Unknown';
  }
}

// Get current git branch
function getGitBranch() {
  try {
    const branch = execSync('git rev-parse --abbrev-ref HEAD', {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'ignore']
    }).trim();
    return branch;
  } catch (error) {
    return null;
  }
}

// Create session summary
function createSessionSummary(config, conversationSummary) {
  const timestamp = getTimestamp();
  const workingDir = getWorkingDirectory();
  const gitBranch = getGitBranch();

  let summary = config.templateHeader
    .replace('{{timestamp}}', timestamp);

  if (config.includeWorkingDirectory) {
    summary += `**Working Directory:** \`${workingDir}\`\n\n`;
  }

  if (config.includeGitBranch && gitBranch) {
    summary += `**Git Branch:** \`${gitBranch}\`\n\n`;
  }

  summary += conversationSummary || '(No summary provided)';
  summary += '\n\n---\n';

  return summary;
}

// Get Daily Note path
function getDailyNotePath(config) {
  const dateStr = getCurrentDate(config.dateFormat || 'YYYY-MM-DD');
  const dailyNotesDir = path.join(
    config.obsidianVaultPath,
    config.dailyNotesPath || 'Daily Notes'
  );

  // Ensure directory exists
  if (!fs.existsSync(dailyNotesDir)) {
    fs.mkdirSync(dailyNotesDir, { recursive: true });
  }

  return path.join(dailyNotesDir, `${dateStr}.md`);
}

// Append to Daily Note
function appendToDailyNote(config, summary) {
  const dailyNotePath = getDailyNotePath(config);

  // Create file if it doesn't exist
  if (!fs.existsSync(dailyNotePath)) {
    const dateStr = getCurrentDate(config.dateFormat || 'YYYY-MM-DD');
    const initialContent = `# ${dateStr}\n\n`;
    fs.writeFileSync(dailyNotePath, initialContent, 'utf-8');
  }

  // Append summary
  fs.appendFileSync(dailyNotePath, summary, 'utf-8');

  console.log(`✓ Session summary appended to: ${dailyNotePath}`);
}

// Main function
function main() {
  try {
    const config = loadConfig();

    // Get conversation summary from stdin or command line arguments
    let conversationSummary = '';

    if (process.argv.length > 2) {
      conversationSummary = process.argv.slice(2).join(' ');
    } else {
      // Try to read from stdin
      try {
        conversationSummary = fs.readFileSync(0, 'utf-8').trim();
      } catch (error) {
        conversationSummary = 'Claude Code session completed.';
      }
    }

    const summary = createSessionSummary(config, conversationSummary);
    appendToDailyNote(config, summary);

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  loadConfig,
  createSessionSummary,
  appendToDailyNote
};
