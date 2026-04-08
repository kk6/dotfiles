# AI Shared Configuration (`~/.ai-shared/`)

Claude Code と OpenAI Codex で共通の開発ルール・スキルを一元管理するための共有レイヤー。

## 設計方針: shared-first, tool-specific-thin

```
~/.ai-shared/          ← 共通資産の正本（chezmoi 管理）
~/.claude/             ← Claude 固有の薄いレイヤー（共有ファイルは symlink で参照）
~/.codex/              ← Codex 固有の薄いレイヤー（同上）
```

ツールに依存しない「開発の知識」は `~/.ai-shared/` に集約し、各ツールからは symlink で参照する。
ツール固有の設定（応答スタイル、フック、サブエージェント等）は各ツールのディレクトリに残す。

## ディレクトリ構成

```bash
~/.ai-shared/
├── core/                              # 共有ルール（正本）
│   ├── coding-philosophy.md           #   Code=How, Test=What, Commit=Why, Comment=Why not
│   ├── git-workflow.md                #   Conventional Commits, TDD, フィーチャーブランチ
│   ├── pytest-best-practices.md       #   テスト命名, AAA, parametrize, fixtures
│   ├── python-development.md          #   プロジェクト構成, ツールチェーン（uv, ruff, ty）
│   └── python-exception-handling.md   #   例外処理ガイドライン（silent failure 禁止）
└── skills/                            # 共有スキル（正本）
    ├── intent/SKILL.md                #   ADR（Architecture Decision Record）生成
    └── pr-description/SKILL.md        #   PR テンプレートに基づく説明文生成
```

## 共有と分離の基準

| 分類 | 内容 | 理由 |
|------|------|------|
| **共有する** | コーディング哲学、Git 運用、テスト方針、言語規約 | ツールに依存しない「チームの知識」 |
| **分ける** | 応答スタイル、対話フロー、フック、サブエージェント、MCP 設定 | ツール固有の機能・性格に依存 |
| **スキルは選択的に共有** | `pr-description`, `intent` は共有。レビュー系は分離 | 手順的なスキルは共有可、判断スタイルに関わるものは分離 |

### Claude 固有（`~/.claude/` に残すもの）

| ファイル | 理由 |
|---------|------|
| `rules/response-style.rule.md` | 応答言語・BLUF 形式 |
| `rules/task-and-session.rule.md` | 対話フロー・確認頻度 |
| `rules/session-file-organization.rule.md` | `.claude/tmp/` の中間ファイル管理 |
| `rules/claude-md-sync.rule.md` | Claude Code の CLAUDE.md 同期機能 |
| `skills/5w1h-review/` | 出力形式が Claude 向け |
| `skills/ai-review/` | 同上 |
| `skills/debug-python/` | デバッグの進め方が Claude 向け |

### Codex 固有（`~/.codex/` に残すもの）

| ファイル | 理由 |
|---------|------|
| `config.toml` | モデル設定、trust_level、プラグイン（chezmoi テンプレート管理） |
| `AGENTS.md` | Codex グローバル指示書 |
| `rules/default.rules` | コマンド許可リスト（ランタイム生成、chezmoi 管理外） |

## chezmoi でのソース管理

### symlink の仕組み

chezmoi ソース内で `symlink_<name>.tmpl` ファイルを作り、中身にリンク先パスを記述する。
`chezmoi apply` 時にテンプレートが展開され、デプロイ先に symlink が作成される。

```
# chezmoi ソース側
dot_claude/rules/symlink_coding-philosophy.md.tmpl
  → 中身: {{ .chezmoi.homeDir }}/.ai-shared/core/coding-philosophy.md

# デプロイ結果
~/.claude/rules/coding-philosophy.md → ~/.ai-shared/core/coding-philosophy.md
```

### ソースディレクトリの対応

| chezmoi ソース | デプロイ先 |
|---------------|-----------|
| `dot_ai-shared/` | `~/.ai-shared/` |
| `dot_claude/` | `~/.claude/` |
| `dot_codex/` | `~/.codex/` |

## 運用

### ルールの追加・変更

共有ルールを編集する場合は正本（`dot_ai-shared/core/`）を編集する。
symlink 経由で Claude・Codex の両方に自動反映される。

```bash
# 共有ルールの編集
chezmoi edit ~/.ai-shared/core/coding-philosophy.md

# Claude 固有ルールの編集
chezmoi edit ~/.claude/rules/response-style.rule.md
```

### 新しいルールの追加

1. ツール非依存か判断する（上記の基準を参照）
2. 共有なら `dot_ai-shared/core/` に追加し、`dot_claude/rules/` と `dot_codex/rules/` に `symlink_*.tmpl` を作成
3. ツール固有なら該当ツールのディレクトリに直接配置

### 新しいスキルの追加

1. 手順的で判断余地が少ないスキルは `dot_ai-shared/skills/` に追加
2. `dot_claude/skills/` と `dot_codex/skills/` に `symlink_*.tmpl` を作成
3. 判断スタイルに依存するスキルは該当ツールのディレクトリに直接配置

### 新環境でのセットアップ

```bash
chezmoi init git@github.com:kk6/dotfiles.git
chezmoi apply
```

`chezmoi apply` で `~/.ai-shared/`、`~/.claude/`、`~/.codex/` のすべてがデプロイされる。
symlink もテンプレート展開により自動的に作成される。
