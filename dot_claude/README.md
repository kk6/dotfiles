# Claude Code Configuration (`~/.claude/`)

このディレクトリには、すべてのプロジェクトに適用される Claude Code のグローバル設定が含まれます。
chezmoi でソース管理され、`~/.local/share/chezmoi/dot_claude/` からデプロイされます。

## ディレクトリ構成

```
~/.claude/
├── CLAUDE.md                              # 全セッションに適用されるグローバル指示
├── README.md                              # このファイル
├── statusline.sh                          # コンテキスト使用量ステータスライン
├── rules/                                 # 振る舞いルール集
│   ├── git-workflow.rule.md
│   ├── python-development.rule.md
│   ├── python-exception-handling.rule.md
│   └── session-management.rule.md
├── skills/                                # カスタムスキル（現行の拡張機能）
│   ├── debug-python/
│   └── pr-description/
└── commands/                              # カスタムスラッシュコマンド（非推奨）
    ├── commit.md
    ├── compress-claude-md.md
    ├── compress-claude-md.py
    ├── gemini-search.md
    └── security-review.md
```

---

## CLAUDE.md

すべての Claude Code セッションで自動的に読み込まれるグローバル指示ファイルです。

| 設定項目 | 内容 |
|---|---|
| 思考言語 | 英語のみ |
| 応答言語 | 日本語 |
| Python 例外処理 | `except: pass` 禁止、最小スコープのキャッチのみ許可 |

詳細ルールへの参照を含む軽量な設定で、具体的なルールは `rules/` に分離しています。

---

## Rules

Claude Code の振る舞いを制御するルールファイル群です。
`CLAUDE.md` から参照され、セッション開始時に自動で読み込まれます。

### `git-workflow.rule.md`

Git の操作規約を定義します。

- Conventional Commits v1.0.0 形式のコミットメッセージ
- フィーチャーブランチの推奨
- TDD（t-wada 方式）の採用
- セッション中の中間ファイルは `.claude/tmp/` に配置

### `python-development.rule.md`

Python プロジェクトの標準的な構成とツール選定を定義します。

- `uv` によるパッケージ管理、`pytest` によるテスト（AAA パターン）
- `ruff`（lint/format）、`ty`（型検査）、`pre-commit` の使用
- ログに f-string 禁止、Google スタイル docstring
- 外部依存がある単独スクリプトは PEP 723 準拠

### `python-exception-handling.rule.md`

Python の例外処理に関する厳格なルールを定義します（違反は容認されません）。

- **`except: pass` は完全禁止**（最も重要なルール）
- `except Exception:` / `except BaseException:` の使用禁止 — 最も具体的な例外クラスを指定
- `try-except` の乱用禁止 — システム境界（I/O・ネットワーク・ユーザー入力）にのみ使用
- 想定外のエラーは伝播させる（クラッシュさせてトレースバックを見る）
- やむを得ず広くキャッチする場合は必ずログに記録し再 raise する

### `session-management.rule.md`

セッション開始時の初期化と進捗保全の規約を定義します。

- セッション開始時に `~/.zshrc` を読み込み、エイリアス設定を把握してからコマンドを提案
- セッション途中で終了する場合は `WIP:` プレフィックスのコミットか TODO コメントで進捗を保存
- PR 関連タスクは途中で止めず完結させる

---

## Skills

`/skill-name` の形式で呼び出せるカスタム拡張機能です。
`~/.claude/skills/` に配置したスキルはすべてのプロジェクトで使用できます。

### `debug-python` — Python デバッグ支援

Python コードのデバッグを体系的に進めるスキルです。

- トレースバック解析 → 再現 → 修正 → テスト検証の一連フローを実行
- 重複キー/ID エラーなど典型的バグパターンへの対処を含む

```
/debug-python   # エラーメッセージかトレースバックを貼り付けて実行
```

### `pr-description` — PR 説明文の自動生成

`.github/PULL_REQUEST_TEMPLATE.md` を読み取り、`git diff` と `git log` をもとに PR 説明文を生成します。

- テンプレートの全セクションを埋める
- 出力はコピーしやすいよう Markdown コードブロックで返す

```
/pr-description
```

### スキルの追加方法

```bash
mkdir -p ~/.claude/skills/my-skill
# ~/.claude/skills/my-skill/SKILL.md を作成
```

SKILL.md の最小構成:

```markdown
---
name: my-skill
description: What this skill does.
---

## Instructions
...

$ARGUMENTS
```

---

## statusline.sh

Claude Code のステータスライン表示スクリプトです。
セッションのコンテキスト使用状況をリアルタイムで表示します。

**表示内容（2行）:**

```
🤖 モデル名 │ 📊 使用量/最大値 ████░░░░░░ XX% 🟢 Good │ ⬇入力 ⬆出力 │ 💡残量 │ ⏳~ETA │ 🔄圧縮回数
🔥 バーンレート │ 🕐 Daily:XX  🗓 Weekly:XX  📊 Monthly:XX
```

| 表示項目 | 説明 |
|---|---|
| モデル名 | 使用中の Claude モデル |
| 使用量バー | コンテキストウィンドウの消費率 |
| バーンレート | トークン消費速度（/min） |
| ETA | コンテキスト枯渇までの推定残り時間 |
| 圧縮回数 | セッション内の自動圧縮発生回数 |
| D/W/M 集計 | 日次・週次・月次のトークン使用量 |

使用履歴は `~/.claude/.sl_usage_log.csv` に蓄積されます。

---

## Custom Commands（非推奨）

> **⚠️ Deprecated — 今後整理予定**
>
> `~/.claude/commands/` のカスタムスラッシュコマンドは、Skills 機能が導入される以前の拡張手段です。
> 現在は Skills が主要な拡張機能であり、`commands/` は段階的に整理・Skills へ移行する予定です。
> 新しい機能は Skills として追加してください。

### `compress-claude-md` — CLAUDE.md 圧縮

CLAUDE.md のコンテキスト使用量を 25–30% 削減する Python スクリプトです。
重複コマンドの統合・コード例の簡潔化・参照形式への変換などの圧縮処理を行います。

```bash
python ~/.claude/commands/compress-claude-md.py          # プロジェクトの CLAUDE.md を圧縮
python ~/.claude/commands/compress-claude-md.py --global # グローバル CLAUDE.md を圧縮
python ~/.claude/commands/compress-claude-md.py --restore # バックアップから復元
```

### `security-review` — セキュリティレビュー

コードのセキュリティ脆弱性をレビューするコマンドです。

### `gemini-search` — Gemini Web 検索

Google Gemini CLI を使った Web 検索コマンドです。
呼び出されると、組み込みの `WebSearch` ツールの代わりに `gemini --prompt` を Task Tool 経由で実行します。

### `commit` — Git コミット

Conventional Commits v1.0.0 仕様に従ったコミットを作成するコマンドです。
pre-commit フックによるファイル変更への対処と Claude Code 署名フッターの付与を含みます。
