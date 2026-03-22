# Claude Code Configuration (`~/.claude/`)

このディレクトリには、すべてのプロジェクトに適用される Claude Code のグローバル設定が含まれます。
chezmoi でソース管理され、`~/.local/share/chezmoi/dot_claude/` からデプロイされます。

## ディレクトリ構成

```bash
~/.claude/
├── CLAUDE.md                              # 全セッションに適用されるグローバル指示
├── README.md                              # このファイル
├── statusline.sh                          # コンテキスト使用量ステータスライン（Bash版）
├── statusline.py                          # コンテキスト使用量ステータスライン（Python版）
├── hooks/                                 # ツール実行フック
│   └── block-pip-install.sh
├── rules/                                 # 振る舞いルール集
│   ├── claude-md-sync.rule.md
│   ├── coding-philosophy.rule.md
│   ├── git-workflow.rule.md
│   ├── idd-workflow.rule.md
│   ├── python-development.rule.md
│   ├── python-exception-handling.rule.md
│   ├── pytest-best-practices.rule.md
│   ├── response-style.rule.md
│   ├── session-management.rule.md
│   └── task-completion.rule.md
├── skills/                                # カスタムスキル（現行の拡張機能）
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
    └── security-review.md
```

---

## CLAUDE.md

すべての Claude Code セッションで自動的に読み込まれるグローバル指示ファイルです。
ルールの概要と `rules/` への参照を含む軽量なハブファイルで、具体的なルールは `rules/` に分離しています。

---

## Rules

Claude Code の振る舞いを制御するルールファイル群です。
`CLAUDE.md` から参照され、セッション開始時に自動で読み込まれます。

### `response-style.rule.md`

応答の言語とスタイルを定義します。

- 思考は英語、応答は日本語
- BLUF（結論先行）で回答

### `coding-philosophy.rule.md`

コード・テスト・コミット・コメントの役割分担を定義します。

- Code = How、Test = What、Commit = Why、Comment = Why not

### `task-completion.rule.md`

タスク完了前のチェックリストとエスカレーション規約を定義します。

- 要件カバレッジ・制約準拠・品質ゲートの 3 段階チェック
- 中間報告と早期エスカレーションの義務

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

### `pytest-best-practices.rule.md`

pytest のベストプラクティスを定義します。

- テストメソッド命名規約（`test_<subject>_<behavior>_when_<condition>`）
- AAA パターン（Arrange-Act-Assert）
- `parametrize` では必ず `ids` を指定
- エッジケース（空入力、境界値、無効入力）の網羅

### `idd-workflow.rule.md`

Intent-Driven Development（IDD）のワークフローとADRテンプレートを定義します。

- Intent = Why（動機）+ What（成果）。How（実装詳細）は含めない
- ADR は `docs/adr/NNNN-kebab-case-slug.md` に保存
- ライフサイクル: proposed → accepted → superseded by ADR-NNNN
- How-Leak Check: 実装詳細がIntentに混入していないか検証

### `claude-md-sync.rule.md`

`rules/` や `hooks/` の追加・削除・改名時に `CLAUDE.md` の該当セクションを同期する規約です。

- ファイル変更後、`CLAUDE.md` の記載と実ファイルの整合性を確認
- 差異がある場合はユーザーに提案してから更新

### `session-management.rule.md`

セッション開始時の初期化と進捗保全の規約を定義します。

- セッション開始時に `~/.zshrc` を読み込み、エイリアス設定を把握してからコマンドを提案
- セッション途中で終了する場合は `WIP:` プレフィックスのコミットか TODO コメントで進捗を保存
- PR 関連タスクは途中で止めず完結させる

---

## Hooks

ツール実行時に自動で呼び出されるフックスクリプトです。

### `block-pip-install.sh`（PreToolUse）

`pip install` / `pip3 install` コマンドの実行をブロックします。
代わりに `uv add`（プロジェクト依存）または `uvx`（CLI ツール）の使用を促します。

---

## Skills

`/skill-name` の形式で呼び出せるカスタム拡張機能です。
`~/.claude/skills/` に配置したスキルはすべてのプロジェクトで使用できます。

### `debug-python` — Python デバッグ支援

Python コードのデバッグを体系的に進めるスキルです。

- トレースバック解析 → 再現 → 修正 → テスト検証の一連フローを実行
- 重複キー/ID エラーなど典型的バグパターンへの対処を含む

```bash
/debug-python   # エラーメッセージかトレースバックを貼り付けて実行
```

### `pr-description` — PR 説明文の自動生成

`.github/PULL_REQUEST_TEMPLATE.md` を読み取り、`git diff` と `git log` をもとに PR 説明文を生成します。

- テンプレートの全セクションを埋める
- 出力はコピーしやすいよう Markdown コードブロックで返す

```bash
/pr-description
```

### `ai-review` — 文章レビュー

下書きテキスト（メッセージ、報告書、PR 説明文、コミットメッセージなど）を読者の視点でレビューし、改善案を提示します。

- 明瞭さ・完全性・構造・トーン・アクションアイテムの 5 軸で評価
- 問題点リスト + 修正版ドラフトを出力

```bash
/ai-review   # レビュー対象のテキストを貼り付けて実行
```

### `intent` — Intent-Driven Development（ADR 生成）

Intent-Driven Development（IDD）に基づき、ADR（Architecture Decision Record）を生成するスキルです。

- ユーザーの意図から Why（動機）と What（成果）を抽出し、How（実装詳細）の混入を検出・分離
- `docs/adr/` の既存ファイルから自動採番
- Supersede ワークフロー対応（旧 ADR の Status 直接編集を含む）

```bash
/intent   # 作りたい機能や設計判断を伝えて実行
```

### `5w1h-review` — 文章の5W1Hチェック

文章の5W1H（Who, What, When, Where, Why, How）の網羅性をチェックし、不足要素と具体的な改善案を提示するスキル

- 対象: 進捗報告、議事録、メール、Slackメッセージ、PR説明文、障害報告、引き継ぎ資料など
- 「レビューして」「5W1Hチェックして」「これで大丈夫か見て」「情報足りてるか」などで起動
- 出力: 各要素のステータス表（✅/⚠️/❌）＋ 不足要素の具体的な追記例 ＋ 総合評価

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

## statusline.sh / statusline.py

Claude Code のステータスライン表示スクリプトです（Bash 版と Python 版の 2 実装）。
セッションのコンテキスト使用状況をリアルタイムで表示します。

**表示内容（2行）:**

```bash
🤖 モデル名 │ 📊 使用量/最大値 ████░░░░░░ XX% 🟢 Good │ ⬇入力 ⬆出力 │ 💡残量 │ ⏳~ETA │ 🔄圧縮回数
🔥 バーンレート │ 🕐 Daily:XX  🗓 Weekly:XX  📊 Monthly:XX
```

| 表示項目 | 説明 |
| --- | --- |
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
