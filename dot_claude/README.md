# Claude Code Configuration (`~/.claude/`)

このディレクトリには、すべてのプロジェクトに適用される Claude Code のグローバル設定が含まれます。
chezmoi でソース管理され、`~/.local/share/chezmoi/dot_claude/` からデプロイされます。

## ディレクトリ構成

```bash
~/.claude/
├── CLAUDE.md                              # グローバル指示（設定アーキテクチャ概要 + hooks/docs/ へのポインタ）
├── README.md                              # このファイル
├── statusline.py                          # コンテキスト使用量ステータスライン（Python版）
├── hooks/                                 # ツール実行フック
│   ├── block-pip-install.sh               #   PreToolUse: pip install をブロック
│   ├── readme-sync-reminder.sh            #   PostToolUse: README.md 更新リマインド
│   └── ruff-check.sh                      #   Stop: 変更 .py に ruff lint/format チェック
├── rules/                                 # 振る舞いルール（自動読み込み。一部は paths: で条件付き）
│   ├── response-style.rule.md             #   常時
│   ├── task-and-session.rule.md           #   常時
│   ├── session-file-organization.rule.md  #   常時
│   ├── claude-md-sync.rule.md             #   paths: 一致時（rules/hooks/skills/settings/CLAUDE.md/README.md）
│   ├── coding-philosophy.rule.md          #   常時
│   ├── git-workflow.rule.md               #   常時
│   ├── pytest-best-practices.rule.md      #   paths: 一致時（test_*.py, tests/**, conftest.py）
│   ├── python-development.rule.md         #   paths: 一致時（*.py, pyproject.toml）
│   └── python-exception-handling.rule.md  #   paths: 一致時（*.py）
├── rule-library/                          # 自動読み込み対象外。必要なリポジトリの .claude/rules/ へ手動コピー
│   └── django-development.rule.md         #   Django プロジェクトでのみ有効化
├── docs/                                  # タスク固有ドキュメント（必要時に読み込み）
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

- **`rules/`（自動読み込み）は「常時必要な振る舞い規約」または「`paths:` で確実にスコープできる技術ルール」に限定** — `paths:` はファイル種別（`*.py` など）で条件付けできるが、フレームワーク単位（Django か等）までは判定できない
- **フレームワーク単位でしか判定できないルールは `rule-library/`** — 自動読み込みせず、該当リポジトリの `.claude/rules/` へ手動コピーして使う
- **タスク固有ガイドは `docs/` に配置** — 必要時にのみ読み込み、命令予算を節約
- **コードスタイルは linter に委譲** — PEP 8、行長、import 順などは ruff の Stop hook で機械的に強制。LLM の命令枠を消費しない
- **CLAUDE.md は簡潔なハブ** — 設定アーキテクチャの概要と `docs/` へのポインタのみ

---

## Rules

`rules/` 配下のファイルは自動読み込みされます。`paths:` frontmatter を持つファイルはマッチするファイルに触れたときだけ注入され、持たないファイルは常時注入されます。

| ファイル | 適用範囲 | 概要 |
|---------|---------|------|
| `response-style` | 常時 | 思考は英語、応答は日本語。BLUF（結論先行） |
| `task-and-session` | 常時 | 要件確認、品質チェック、進捗報告、エスカレーション、セッション管理 |
| `session-file-organization` | 常時 | セッション中の中間ファイルは `.claude/tmp/` に配置 |
| `coding-philosophy` | 常時 | Code=How, Test=What, Commit=Why, Comment=Why not |
| `git-workflow` | 常時 | Conventional Commits、フィーチャーブランチ、TDD |
| `claude-md-sync` | `paths:` | rules/hooks/skills/settings/CLAUDE.md/README.md 変更時に同期を促す |
| `pytest-best-practices` | `paths:` | テスト命名、AAA パターン、parametrize、fixtures |
| `python-development` | `paths:` | プロジェクト構成（src/tests/docs）、ツールチェーン（uv, ruff, ty, pytest） |
| `python-exception-handling` | `paths:` | 例外処理ガイドライン（silent failure 禁止） |

## Rule Library

`rule-library/` 配下は自動読み込み**されません**。フレームワーク単位でしか判定できない（`*.py` のような glob では絞り込めない）ルールの置き場で、該当するリポジトリでのみ `.claude/rules/` へ手動コピーして使います。

| ファイル | 概要 | 使い方 |
|---------|------|--------|
| `django-development` | Django プロジェクトの開発規約 | `cp ~/.claude/rule-library/django-development.rule.md ./.claude/rules/` |

---

## Docs

`docs/*.md` はタスク固有のガイドです。必要時に Claude が読み込みます。

| ファイル | 概要 |
|---------|------|
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
| `ai-review` | 文章を読者視点でレビューし改善案を提示 |
| `5w1h-review` | 文章の 5W1H 網羅性チェック |
| `pr-description` | PR テンプレートに基づく説明文の自動生成 |
| `intent` | IDD に基づく ADR（Architecture Decision Record）の生成 |

> Codex (`~/.codex/skills/`) にも同名スキルがあるが、モデルごとにプロンプトをチューニングできるよう実体を分離している（symlink 共有はしない）。

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

## statusline.py

Claude Code セッションのコンテキスト使用状況をリアルタイム表示するステータスラインスクリプトです。

使用履歴は `~/.claude/.sl_usage_log.csv` に蓄積されます。
