# cc-marketplace

kadoppeのClaude Codeプラグインマーケットプレイス

## 概要

このリポジトリは、Claude Code用のカスタムプラグインを提供するマーケットプレイスです。

## 利用可能なプラグイン

### obsidian-logger

Claude Codeの作業内容をObsidianのDaily Noteに自動記録するプラグインです。セッション終了時に、Stop hookを使って作業内容を自動的にObsidian vaultのDaily Noteに追記します。

- **バージョン**: 0.1.0
- **機能**: Stop hook による自動ログ記録
- **詳細**: [obsidian-logger/README.md](./obsidian-logger/README.md)

## インストール

### 1. マーケットプレイスを追加

Claude Codeで以下のコマンドを実行してこのマーケットプレイスを追加します:

```bash
/plugin marketplace add /Users/kadoppe/Sources/github.com/kadoppe/cc-marketplace
```

または、GitHubからクローンした場合:

```bash
/plugin marketplace add ./cc-marketplace
```

### 2. プラグインをインストール

```bash
/plugin install obsidian-logger@cc-marketplace
```

### 3. インストール済みプラグインの確認

```bash
/plugin list
```

## 開発

### 新しいプラグインの追加

1. `plugins/`ディレクトリ内に新しいプラグインディレクトリを作成:

```bash
mkdir -p plugins/my-new-plugin/.claude-plugin
cd plugins/my-new-plugin
```

2. `.claude-plugin/plugin.json`を作成してプラグインマニフェストを定義

3. 必要なコンポーネント（commands、agents、skills、scripts等）をプラグインルートに追加

4. `.claude-plugin/marketplace.json`にプラグイン情報を追加

### プラグインの更新

プラグインを更新した場合:

1. プラグインをアンインストール:
   ```bash
   /plugin uninstall plugin-name@cc-marketplace
   ```

2. 再インストール:
   ```bash
   /plugin install plugin-name@cc-marketplace
   ```

## マーケットプレイス構造

```
cc-marketplace/
├── .claude-plugin/
│   └── marketplace.json      # マーケットプレイスのメタデータ
├── README.md                 # このファイル
├── .gitignore                # Git除外設定
└── plugins/
    └── obsidian-logger/      # プラグイン
        ├── .claude-plugin/
        │   └── plugin.json   # プラグインマニフェスト
        ├── hooks/
        │   └── hooks.json    # Hook設定
        ├── scripts/          # スクリプト
        │   └── append-to-daily-note.js  # メイン処理
        ├── config.example.json  # 設定ファイルのサンプル
        ├── package.json      # npm設定
        └── README.md         # プラグインのドキュメント
```

## ライセンス

MIT

## 作者

kadoppe
