# fzf 設定

[fzf](https://github.com/junegunn/fzf) はコマンドラインのファジーファインダーです。

## 設定ファイル

| ファイル | 役割 |
|---------|------|
| `~/.fzf.zsh` | Zsh 用の設定（PATH、補完、キーバインド） |
| `~/.fzf.bash` | Bash 用の設定 |

## デフォルト設定

`.zshrc` で以下の環境変数を設定しています。

```bash
# ripgrep をデフォルトコマンドとして使用（.git を除外）
export FZF_DEFAULT_COMMAND='rg --files --hidden --glob "!.git"'

# 表示オプション
export FZF_DEFAULT_OPTS='--height 40% --reverse --border'
```

| オプション | 説明 |
|-----------|------|
| `--height 40%` | 画面の 40% の高さで表示 |
| `--reverse` | 結果を上から表示 |
| `--border` | ボーダーを表示 |

## キーバインド

Zsh で以下のキーバインドが有効になっています。

| キー | 機能 |
|------|------|
| `Ctrl+T` | ファイル検索（カレントディレクトリ以下） |
| `Ctrl+R` | コマンド履歴検索 |
| `Alt+C` | ディレクトリ移動 |

## ghq 連携

`Ctrl+G` で ghq 管理のリポジトリを検索・移動できます（`.zshrc` で設定）。

```bash
# Ctrl+G を押すと、ghq 管理のリポジトリ一覧が表示される
# 選択すると、そのディレクトリに移動
```

## 使用例

```bash
# ファイルを検索して vim で開く
vim $(fzf)

# プロセスを検索して kill
kill -9 $(ps aux | fzf | awk '{print $2}')

# Git ブランチを切り替え
git switch $(git branch | fzf)
```

## 参考リンク

- [fzf GitHub](https://github.com/junegunn/fzf)
- [fzf Wiki](https://github.com/junegunn/fzf/wiki)
