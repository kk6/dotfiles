# Claude Code Configuration (`~/.claude/`)

このディレクトリには、すべてのプロジェクトに適用される Claude Code のグローバル設定が含まれます。
chezmoi でソース管理され、`~/.local/share/chezmoi/dot_claude/` からデプロイされます。

## ディレクトリ構成

```bash
~/.claude/
├── CLAUDE.md                              # グローバル指示（ツールチェーン要約 + docs/ へのポインタ）
├── README.md                              # このファイル
├── statusline.py                          # コンテキスト使用量ステータスライン（Python版）
├── hooks/                                 # ツール実行フック
│   ├── block-pip-install.sh               #   PreToolUse: pip install をブロック
│   ├── readme-sync-reminder.sh            #   PostToolUse: README.md 更新リマインド
│   └── ruff-check.sh                      #   Stop: 変更 .py に ruff lint/format チェック
├── rules/                                 # 振る舞いルール（全セッション自動読み込み）
│   ├── response-style.rule.md             #   Claude 固有
│   ├── task-and-session.rule.md           #   Claude 固有
│   ├── session-file-organization.rule.md  #   Claude 固有
│   ├── claude-md-sync.rule.md             #   Claude 固有
│   ├── coding-philosophy.md        → ~/.ai-shared/core/  # 共有
│   ├── git-workflow.md             → ~/.ai-shared/core/  # 共有
│   ├── pytest-best-practices.md    → ~/.ai-shared/core/  # 共有
│   ├── python-development.md       → ~/.ai-shared/core/  # 共有
│   └── python-exception-handling.md → ~/.ai-shared/core/ # 共有
├── docs/                                  # タスク固有ドキュメント（必要時に読み込み）
│   └── idd-workflow.md
├── skills/                                # カスタムスキル
│   ├── 5w1h-review/                       #   Claude 固有
│   ├── ai-review/                         #   Claude 固有
│   ├── debug-python/                      #   Claude 固有
│   ├── intent/              → ~/.ai-shared/skills/  # 共有
│   └── pr-description/      → ~/.ai-shared/skills/  # 共有
└── commands/                              # カスタムスラッシュコマンド（非推奨）
    ├── commit.md
    ├── compress-claude-md.md
    ├── compress-claude-md.py
    ├── gemini-search.md
    ├── security-review.md
    └── sentry-to-github.md
```

> `→ ~/.ai-shared/` と表記されたファイルは symlink。正本は `~/.ai-shared/` にあり、
> Codex (`~/.codex/`) とも共有されている。詳細は [docs/ai-shared.md](../docs/ai-shared.md) を参照。

---

## 設計方針

[Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) の推奨に基づく構成です。

- **`rules/`（自動読み込み）にはユニバーサルなルールのみ** — 全セッションで必要な振る舞い規約に限定
- **タスク固有ガイドは `docs/` に配置** — pytest や例外処理のガイドは必要時にのみ読み込み、命令予算を節約
- **コードスタイルは linter に委譲** — PEP 8、行長、import 順などは ruff の Stop hook で機械的に強制。LLM の命令枠を消費しない
- **CLAUDE.md は簡潔なハブ** — ツールチェーン要約と `docs/` へのポインタのみ。ルール一覧は不要（自動読み込みのため）

---

## Rules

`rules/` 配下のファイルは全セッションで自動読み込みされます。

### Claude 固有

| ファイル | 概要 |
|---------|------|
| `response-style` | 思考は英語、応答は日本語。BLUF（結論先行） |
| `task-and-session` | 要件確認、品質チェック、進捗報告、エスカレーション、セッション管理 |
| `session-file-organization` | セッション中の中間ファイルは `.claude/tmp/` に配置 |
| `claude-md-sync` | rules/hooks 変更時に CLAUDE.md を同期 |

### 共有（`~/.ai-shared/core/` → symlink）

| ファイル | 概要 |
|---------|------|
| `coding-philosophy` | Code=How, Test=What, Commit=Why, Comment=Why not |
| `git-workflow` | Conventional Commits、フィーチャーブランチ、TDD |
| `pytest-best-practices` | テスト命名、AAA パターン、parametrize、fixtures |
| `python-development` | プロジェクト構成（src/tests/docs）、ツールチェーン（uv, ruff, ty, pytest） |
| `python-exception-handling` | 例外処理ガイドライン（silent failure 禁止） |

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

### Claude 固有

| スキル | 概要 |
|--------|------|
| `debug-python` | トレースバック解析 → 再現 → 修正 → テスト検証 |
| `ai-review` | 文章を読者視点でレビューし改善案を提示 |
| `5w1h-review` | 文章の 5W1H 網羅性チェック |

### 共有（`~/.ai-shared/skills/` → symlink）

| スキル | 概要 |
|--------|------|
| `pr-description` | PR テンプレートに基づく説明文の自動生成 |
| `intent` | IDD に基づく ADR（Architecture Decision Record）の生成 |

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
