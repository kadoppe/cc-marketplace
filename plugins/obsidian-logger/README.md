# Obsidian Logger Plugin

Claude Codeの作業内容をObsidianのDaily Noteに自動記録するプラグインです。

## 概要

このプラグインは、Claude Codeのセッションが終了したときに、Stop hookを使って作業内容を自動的にObsidianのDaily Noteに追記します。

## 機能

- **Stop Hook**: Claude Code終了時に自動実行
- **Daily Note連携**: Obsidian vaultのDaily Noteに作業内容を追記
- **柔軟な設定**: Vault パス、Daily Notes フォルダ、日付フォーマットなどをカスタマイズ可能
- **Git情報の記録**: 作業ディレクトリとGitブランチを自動記録（オプション）

## インストール

### 1. マーケットプレイスからインストール

```bash
# マーケットプレイスを追加（初回のみ）
/plugin marketplace add /Users/kadoppe/Sources/github.com/kadoppe/cc-marketplace

# プラグインをインストール
/plugin install obsidian-logger@cc-marketplace
```

### 2. 設定ファイルの作成

プラグインディレクトリに`config.json`を作成します：

```bash
cd ~/.claude/plugins/obsidian-logger
cp config.example.json config.json
```

### 3. 設定ファイルの編集

`config.json`を編集して、Obsidian vaultのパスなどを設定します：

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

#### 設定項目

- `obsidianVaultPath`: Obsidian vaultの絶対パス（**必須**）
- `dailyNotesPath`: Daily Notesフォルダのパス（vaultからの相対パス）
- `dateFormat`: 日付フォーマット（デフォルト: `YYYY-MM-DD`）
- `templateHeader`: セッション記録のヘッダーテンプレート
- `includeWorkingDirectory`: 作業ディレクトリを記録するか（デフォルト: `true`）
- `includeGitBranch`: Gitブランチを記録するか（デフォルト: `true`）

### 4. スクリプトに実行権限を付与

```bash
chmod +x ~/.claude/plugins/obsidian-logger/scripts/append-to-daily-note.js
```

## 使用方法

プラグインをインストールして設定が完了すると、Claude Codeのセッションを終了するたびに、自動的にObsidianのDaily Noteに作業内容が記録されます。

### 記録される情報

- セッションのタイムスタンプ
- 作業ディレクトリ（設定により有効な場合）
- Gitブランチ（設定により有効な場合）
- 作業内容のサマリー

### 記録例

```markdown
## Claude Code Session - 2025/11/16 14:30:15

**Working Directory:** `/Users/kadoppe/projects/my-app`

**Git Branch:** `feature/new-feature`

プラグインの雛形を作成しました。

---
```

## スクリプト

基本的な機能は`scripts/`ディレクトリに切り出されています：

- `append-to-daily-note.js`: Daily Noteへの追記処理を行うメインスクリプト

### 手動実行

スクリプトは手動でも実行できます：

```bash
# 引数でサマリーを指定
node scripts/append-to-daily-note.js "作業内容のサマリー"

# 標準入力からサマリーを読み込み
echo "作業内容のサマリー" | node scripts/append-to-daily-note.js
```

## トラブルシューティング

### Daily Noteが作成されない

- `config.json`の`obsidianVaultPath`が正しいか確認してください
- ファイルシステムの書き込み権限があるか確認してください

### Gitブランチが記録されない

- 作業ディレクトリがGitリポジトリかどうか確認してください
- `config.json`で`includeGitBranch`が`true`になっているか確認してください

## 開発

### プラグインの更新

```bash
# アンインストール
/plugin uninstall obsidian-logger@cc-marketplace

# 再インストール
/plugin install obsidian-logger@cc-marketplace
```

### ディレクトリ構造

```
obsidian-logger/
├── .claude-plugin/
│   └── plugin.json          # プラグインマニフェスト
├── hooks/
│   └── hooks.json           # Hook設定
├── scripts/                 # スクリプト
│   └── append-to-daily-note.js  # メイン処理
├── config.example.json      # 設定ファイルのサンプル
├── package.json             # npm設定
└── README.md                # このファイル
```

### Hook設定について

このプラグインは`hooks/hooks.json`で以下のようにStop hookを定義しています：

```json
{
  "Stop": [
    {
      "matcher": ".*",
      "hooks": [
        {
          "type": "command",
          "command": "node ${CLAUDE_PLUGIN_ROOT}/scripts/append-to-daily-note.js"
        }
      ]
    }
  ]
}
```

`.claude-plugin/plugin.json`では、このhooks.jsonファイルを参照しています：

```json
{
  "hooks": "./hooks/hooks.json"
}
```

- **Stop**: Claude Codeのセッション終了時に実行されるイベント
- **matcher**: `.*` で全ての停止イベントにマッチ
- **command**: スクリプトを実行（`${CLAUDE_PLUGIN_ROOT}`は自動的にプラグインのルートディレクトリに展開されます）

## ライセンス

MIT

## 作者

kadoppe
