# Claude Code カスタムコマンド

このディレクトリには、Claude Code での開発効率を向上させるためのカスタムコマンドが含まれています。

## 利用可能なコマンド

### 1. CLAUDE.md圧縮ツール (`compress-claude-md.py`)

CLAUDE.mdファイルのコンテキスト使用量を25-30%削減する圧縮ツールです。

#### 機能
- **自動バックアップ**: 元ファイルを`.backup`として保存
- **段階的圧縮**: 4段階の圧縮処理を適用
- **情報保全**: 重要な開発情報は保持
- **復元機能**: 問題があれば元に戻すことが可能
- **詳細レポート**: 圧縮効果の数値化

#### 使用方法

```bash
# プロジェクトのCLAUDE.mdを圧縮
python ~/.claude/commands/compress-claude-md.py

# グローバルCLAUDE.mdを圧縮
python ~/.claude/commands/compress-claude-md.py --global

# 指定したファイルを圧縮
python ~/.claude/commands/compress-claude-md.py /path/to/CLAUDE.md

# バックアップから復元（プロジェクト）
python ~/.claude/commands/compress-claude-md.py --restore

# バックアップから復元（グローバル）
python ~/.claude/commands/compress-claude-md.py --restore --global
```

#### 圧縮対象
- **Build/Test/Lint Commands**: 重複するコマンドを統合形式に変換
- **コード例**: 長いコード例を要点に絞って簡潔化
- **重複セクション**: 重複的なセクションを統合
- **参照セクション**: 詳細情報を外部ドキュメントへの参照に変換

#### 期待される効果
- 文字数削減: 25-30%
- コンテキスト使用量の削減
- Claude Code の応答速度向上
- 重要な開発情報の保持

#### 安全性
- 実行前に自動バックアップを作成
- 元ファイルは`.backup`拡張子で保存
- 復元機能により簡単に元に戻すことが可能
- 圧縮結果の詳細レポートを表示

#### 使用例

```bash
# 圧縮実行
$ python ~/.claude/commands/compress-claude-md.py
CLAUDE.md圧縮開始: /Users/kk6/project/CLAUDE.md
==================================================
✓ バックアップ作成: /Users/kk6/project/CLAUDE.md.backup
圧縮処理中...

✓ 圧縮完了!
元のサイズ: 33,587 文字 (812 行)
圧縮後サイズ: 25,190 文字 (601 行)
削減量: 8,397 文字 (25.0%)
バックアップ: /Users/kk6/project/CLAUDE.md.backup

復元する場合: python compress-claude-md.py --restore
```

### 2. セキュリティレビュー (`security-review.md`)

コードのセキュリティ脆弱性をレビューするためのコマンドです。

### 3. Gemini Web検索 (`gemini-search.md`)

Google Gemini CLIを使用してWeb検索を行うためのコマンドです。

#### 機能
- **優先使用**: Web検索が必要な場合、組み込みの`WebSearch`ツールではなく、このコマンドを使用
- **Task Tool統合**: Task Toolを通じてgeminiコマンドを実行
- **シンプルな構文**: `gemini --prompt`形式でWeb検索を実行

#### 使用方法

Claude Codeでは、Web検索が必要な場合に自動的にこのコマンドが使用されます。

```bash
gemini --prompt "WebSearch: <検索クエリ>"
```

#### 注意事項
- **必須使用**: Web検索時は必ずこのコマンドを使用すること
- **Task Tool経由**: 直接実行ではなく、Task Toolを通じて実行すること

### 4. Git コミット (`commit.md`)

Conventional Commits v1.0.0仕様に従ったGitコミットを作成するためのコマンドです。

#### 機能
- **事前分析**: git status、diff、logを並列実行して現在の状態を確認
- **Conventional Commits準拠**: セマンティックバージョニングに対応した形式
- **pre-commitフック対応**: フックによるファイル変更を自動処理
- **Claude Codeフッター**: 自動的にClaude Code署名を追加

#### 使用方法

Claudeに `/commit` コマンドで使用可能です。

#### コミットタイプ
- `feat:` - 新機能 (MINOR バージョンアップ)
- `fix:` - バグ修正 (PATCH バージョンアップ)
- `docs:` - ドキュメント変更
- `style:` - コードフォーマット (機能変更なし)
- `refactor:` - リファクタリング
- `test:` - テスト追加・修正
- `chore:` - メンテナンス作業
- `ci:` - CI設定変更
- `perf:` - パフォーマンス改善
- `build:` - ビルドシステム変更

#### 破壊的変更の記載
- タイプの後に `!` を追加: `feat(api)!: エンドポイント構造変更`
- またはフッターに記載: `BREAKING CHANGE: 破壊的変更の説明`

## コマンドの追加方法

新しいカスタムコマンドを追加する場合：

1. `~/.claude/commands/` ディレクトリに新しいファイルを作成
2. スクリプトファイルの場合は実行権限を付与: `chmod +x filename`
3. このREADMEに使用方法を追記

## 注意事項

- コマンドは自己責任で使用してください
- 重要なファイルを操作する前は必ずバックアップを作成してください
- 問題が発生した場合は、バックアップから復元してください

## トラブルシューティング

### CLAUDE.md圧縮ツールのトラブルシューティング

**問題**: 圧縮後にClaude Codeが正常に動作しない
**解決**: バックアップから復元してください
```bash
python ~/.claude/commands/compress-claude-md.py --restore
```

**問題**: 特定のセクションが過度に圧縮されている
**解決**: 圧縮スクリプトの該当関数を調整するか、手動で必要な情報を追加してください

**問題**: バックアップファイルが見つからない
**解決**: 圧縮実行前にバックアップが作成されているか確認してください。`.backup`拡張子のファイルを探してください。

## ファイル作成ルール

Claude Codeセッション中の中間ファイルは `./claude/tmp/` ディレクトリに配置してください。
- セッション中の中間出力も `.claude/tmp/` に作成されます
- 必要に応じて `.claude/tmp/` の外への移動を提案します

## フィードバック

コマンドの改善提案やバグ報告は、プロジェクトのイシューとして報告してください。