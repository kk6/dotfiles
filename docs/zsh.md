# Zsh 設定

Zsh の設定ファイルを管理しています。

## 設定ファイル

| ファイル | 役割 |
|---------|------|
| `.zshrc` | メインの設定ファイル（対話シェル起動時に読み込み） |
| `.zshenv` | 環境変数の設定（全シェルで読み込み） |
| `.zprofile` | ログインシェル起動時の設定 |

## 主な設定内容

### XDG Base Directory

```bash
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_CACHE_HOME="$HOME/.cache"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_STATE_HOME="$HOME/.local/state"
```

### エイリアス

#### Unix コマンドの置き換え

Rust製のモダンなコマンドに置き換えています。

| エイリアス | 実際のコマンド | 説明 |
|-----------|--------------|------|
| `ls` | `lsd` | モダンなファイル一覧表示 |
| `cat` | `bat` | シンタックスハイライト付きファイル表示 |
| `find` | `fd` | 高速なファイル検索 |
| `vi`, `vim` | `nvim` | Neovim |

#### lsd 関連

| エイリアス | 実行内容 |
|-----------|---------|
| `l`, `ll` | `ls -l` |
| `la` | `ls -a` |
| `lla` | `ls -la` |
| `lt`, `tree` | `ls --tree` |

#### Git コマンド

| エイリアス | 実行内容 |
|-----------|---------|
| `gsw` | `git switch` |
| `gst` | `git status` |
| `ga` | `git add` |
| `gl` | `git pull` |
| `gp` | `git push` |
| `gd` | `git diff` |

#### GitHub Copilot CLI

| エイリアス | 実行内容 |
|-----------|---------|
| `gs` | `gh copilot suggest` |
| `ge` | `gh copilot explain` |

### 便利機能

#### ghq + fzf 連携

`Ctrl+G` で ghq 管理のリポジトリを fzf で検索・移動できます。

```bash
# ghq で管理しているリポジトリに移動
Ctrl+G
```

### 読み込まれるツール

- **zsh-autosuggestions**: コマンド補完サジェスト
- **starship**: カスタマイズ可能なシェルプロンプト
- **zoxide**: スマートなディレクトリ移動（`z` コマンド）
- **mise**: バージョン管理ツール
- **fzf**: ファジーファインダー

## ローカル設定

`.zshrc.local` を作成すると、マシン固有の設定を追加できます。このファイルは `.zshrc` の最後に読み込まれます。

```bash
# 例: ローカル設定の追加
echo 'export MY_LOCAL_VAR="value"' >> ~/.zshrc.local
```

## 参考リンク

- [lsd GitHub](https://github.com/lsd-rs/lsd)
- [bat GitHub](https://github.com/sharkdp/bat)
- [fd GitHub](https://github.com/sharkdp/fd)
- [zoxide GitHub](https://github.com/ajeetdsouza/zoxide)
