# Claude Code Configuration (`~/.claude/`)

このディレクトリには、すべてのプロジェクトに適用される Claude Code のグローバル設定が含まれます。
chezmoi でソース管理され、`~/.local/share/chezmoi/dot_claude/` からデプロイされます。

## ディレクトリ構成

```bash
~/.claude/
├── CLAUDE.md                              # グローバル指示（ツールチェーン要約 + docs/ へのポインタ）
├── README.md                              # このファイル
├── statusline.sh                          # コンテキスト使用量ステータスライン（Bash版）
├── statusline.py                          # コンテキスト使用量ステータスライン（Python版）
├── hooks/                                 # ツール実行フック
│   ├── block-pip-install.sh               #   PreToolUse: pip install をブロック
│   └── ruff-check.sh                      #   Stop: 変更 .py に ruff lint/format チェック
├── rules/                                 # 振る舞いルール（全セッション自動読み込み）
│   ├── response-style.rule.md
│   ├── coding-philosophy.rule.md
│   ├── task-and-session.rule.md
│   ├── python-development.rule.md
│   ├── git-workflow.rule.md
│   └── claude-md-sync.rule.md
├── docs/                                  # タスク固有ドキュメント（必要時に読み込み）
│   ├── pytest-best-practices.md
│   ├── python-exception-handling.md
│   └── idd-workflow.md
├── skills/                                # カスタムスキル
│   ├── 5w1h-review/
│   ├── ai-review/
│   ├── debug-python/
│   ├── intent/
│   └── pr-description/
└── commands/                              # カスタムスラッシュコマンド（非推奨）
    ├── commit.md
    ├── compress-claude-md.md
    ├── compress-claude-md.py
    ├── gemini-search.md
    ├── security-review.md
    └── sentry-to-github.md
```

---

## 設計方針

[Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) の推奨に基づく構成です。

- **`rules/`（自動読み込み）にはユニバーサルなルールのみ** — 全セッションで必要な振る舞い規約に限定
- **タスク固有ガイドは `docs/` に配置** — pytest や例外処理のガイドは必要時にのみ読み込み、命令予算を節約
- **コードスタイルは linter に委譲** — PEP 8、行長、import 順などは ruff の Stop hook で機械的に強制。LLM の命令枠を消費しない
- **CLAUDE.md は簡潔なハブ** — ツールチェーン要約と `docs/` へのポインタのみ。ルール一覧は不要（自動読み込みのため）

---

## Rules

`rules/*.rule.md` は全セッションで自動読み込みされます。

| ファイル | 概要 |
|---------|------|
| `response-style` | 思考は英語、応答は日本語。BLUF（結論先行） |
| `coding-philosophy` | Code=How, Test=What, Commit=Why, Comment=Why not |
| `task-and-session` | 要件確認、品質チェック、進捗報告、エスカレーション、セッション管理 |
| `python-development` | プロジェクト構成（src/tests/docs）、ツールチェーン（uv, ruff, ty, pytest） |
| `git-workflow` | Conventional Commits、フィーチャーブランチ、TDD |
| `claude-md-sync` | rules/hooks 変更時に CLAUDE.md を同期 |

---

## Docs

`docs/*.md` はタスク固有のガイドです。必要時に Claude が読み込みます。

| ファイル | 概要 |
|---------|------|
| `pytest-best-practices` | テスト命名、AAA パターン、parametrize、fixtures |
| `python-exception-handling` | 例外処理ガイドライン（silent failure 禁止） |
| `idd-workflow` | Intent-Driven Development、ADR テンプレート・ライフサイクル |

---

## Hooks

| フック | トリガー | 概要 |
|--------|---------|------|
| `block-pip-install.sh` | PreToolUse (Bash) | `pip install` をブロックし `uv add` / `uvx` を促す |
| `ruff-check.sh` | Stop | 変更された `.py` ファイルに `ruff check` + `ruff format --check` を実行 |

---

## Skills

`/skill-name` で呼び出せるカスタム拡張機能です。

| スキル | 概要 |
|--------|------|
| `debug-python` | トレースバック解析 → 再現 → 修正 → テスト検証 |
| `pr-description` | PR テンプレートに基づく説明文の自動生成 |
| `ai-review` | 文章を読者視点でレビューし改善案を提示 |
| `intent` | IDD に基づく ADR（Architecture Decision Record）の生成 |
| `5w1h-review` | 文章の 5W1H 網羅性チェック |

---

## Commands（非推奨）

> **今後 Skills へ移行予定。** 新しい機能は Skills として追加してください。

| コマンド | 概要 |
|---------|------|
| `commit` | Conventional Commits 準拠のコミット作成 |
| `compress-claude-md` | CLAUDE.md のコンテキスト使用量を圧縮 |
| `gemini-search` | Gemini CLI 経由の Web 検索 |
| `security-review` | コードのセキュリティ脆弱性レビュー |
| `sentry-to-github` | Sentry issue から GitHub issue の検索・作成 |

---

## statusline.sh / statusline.py

Claude Code セッションのコンテキスト使用状況をリアルタイム表示するステータスラインスクリプトです（Bash 版と Python 版の 2 実装）。

使用履歴は `~/.claude/.sl_usage_log.csv` に蓄積されます。
