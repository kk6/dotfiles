# Git 設定

Git のグローバル設定を管理しています。

## 設定ファイル

| ファイル | 役割 |
|---------|------|
| `~/.config/git/config` | Git の設定 |
| `~/.config/git/ignore` | グローバル gitignore |

## 主な設定

### エイリアス

| エイリアス | 説明 |
|-----------|------|
| `plog` | 整形されたログ表示（ハッシュ、日付、メッセージ、ブランチ、著者） |
| `push-f` | `--force-with-lease` 付きのプッシュ（安全な強制プッシュ） |

```bash
# 使用例
git plog
git push-f
```

### コア設定

| 設定 | 値 | 説明 |
|------|-----|------|
| `core.editor` | `vim` | コミットメッセージ編集に使用 |
| `core.pager` | `delta` | 差分表示に delta を使用 |

### delta 設定

[delta](https://github.com/dandavison/delta) を使用して差分表示を改善しています。

- `navigate = true`: n/N で差分間を移動
- `dark = true`: ダークモード

### ブランチとマージ

| 設定 | 値 | 説明 |
|------|-----|------|
| `init.defaultBranch` | `main` | 新規リポジトリのデフォルトブランチ |
| `merge.ff` | `false` | マージコミットを常に作成 |
| `merge.conflictstyle` | `zdiff3` | コンフリクト表示形式 |
| `pull.ff` | `only` | fast-forward できない場合はエラー |

### マージツール

VS Code をマージツールとして設定しています。

```bash
# コンフリクト解消時
git mergetool
```

### Git LFS

大容量ファイル管理のため Git LFS が有効化されています。

## グローバル gitignore

以下のファイルタイプがグローバルで無視されます：

- **macOS**: `.DS_Store`, `._*` など
- **エディタ**: Vim スワップファイル、JetBrains IDE 設定
- **言語**: Python (`__pycache__/`, `.pyc`)、Node.js (`node_modules/`)、Ruby (`*.gem`)
- **ビルド成果物**: `build/`, `dist/`, `coverage/`
- **環境ファイル**: `.env`, `.venv/`

## 参考リンク

- [delta GitHub](https://github.com/dandavison/delta)
- [Git LFS](https://git-lfs.github.com/)
