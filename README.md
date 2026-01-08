# dotfiles

個人用のdotfiles設定を [chezmoi](https://github.com/twpayne/chezmoi) で管理しています。

## 管理されているファイル

- **シェル設定**: `.zshrc`, `.zshenv`, `.zprofile`
- **エディタ設定**: `.vimrc`, `.editorconfig`, Neovim設定
- **開発ツール**: Git設定, Starship設定, Flake8設定, mise設定
- **ターミナル**: `.tmux.conf`, Ghostty設定
- **Claude Code設定**: `.claude/CLAUDE.md`, カスタムコマンド
- **その他**: `.fzf.bash`, `.fzf.zsh`, `.stylelintrc`, npm設定など

## セットアップ

### 新環境での初期設定

```bash
# chezmoi のインストール
$ brew install chezmoi

# dotfilesリポジトリからの初期化
$ chezmoi init git@github.com:kk6/dotfiles.git

# 設定内容の確認（適用前のプレビュー）
$ chezmoi diff

# 設定ファイルの適用
$ chezmoi apply
```

### その他のプラットフォーム

chezmoi は Windows や Linux でも使用できます。詳細は[公式ドキュメント](https://www.chezmoi.io/install/)を参照してください。

## 使い方

### ファイルの編集

```bash
# ファイルを編集（例：.zshrc）
$ chezmoi edit ~/.zshrc

# 編集内容を適用
$ chezmoi apply
```

### よく使用するコマンド

```bash
# 変更内容の確認
$ chezmoi diff

# 設定ファイルの状態確認
$ chezmoi status

# リポジトリから最新の変更を取得して適用
$ chezmoi update

# 変更をリポジトリに追加・コミット・プッシュ
$ chezmoi add ~/.zshrc
$ chezmoi cd
$ git commit -m "Update zshrc"
$ git push
$ exit
```

### .zshrc.local の使用

`.zshrc.local` ファイルを使用して、個別の環境設定を上書きできます。このファイルは `.zshrc` の後に読み込まれます。

現状、`.zshrc.local` はリポジトリに含まれていません。必要に応じて自分で作成してください。

```bash
# .zshrc.local の作成
$ touch ~/.zshrc.local
# .zshrc.local に個別の設定を追加
$ echo "export PATH=\$PATH:/my/custom/path" >> ~/.zshrc.local
```

## 注意事項

- このリポジトリは個人用の設定を管理するためのものであり、他のユーザーが使用することを意図していません。
- 変更を加える際は、事前にバックアップを取ることをおすすめします。

## mise 設定

[mise](https://mise.jdx.dev/) は、複数のプログラミング言語のバージョン管理を統一的に行うためのツールです。

### 設定ファイル

- **config.toml**: mise の基本設定
  - Python バージョンファイル（`.python-version`）を使用したツール自動有効化
  - 実験的機能の有効化

### 使用方法

```bash
# Python バージョンを自動的に認識・使用
$ mise use python@3.11

# 現在のバージョンを確認
$ mise current

# インストール済みのバージョンを確認
$ mise list
```

詳細は[mise の公式ドキュメント](https://mise.jdx.dev/)を参照してください。

## Claude Code 設定

このリポジトリには Claude Code の設定とカスタムコマンドが含まれています：

- **CLAUDE.md**: Claude Code の開発設定（Python、Git、TDD など）
- **カスタムコマンド**:
  - CLAUDE.md 圧縮ツール（コンテキスト削減）
  - セキュリティレビューコマンド
  - Conventional Commits 準拠の Git コミットコマンド

詳細は `dot_claude/README.md` を参照してください。

## Neovim / Vim

`vim` は `nvim` のエイリアスとして設定されています。

### 設定ファイルの構成

| ファイル | 役割 |
|---------|------|
| `~/.vimrc` | 空（LazyVimに委譲） |
| `~/.config/nvim/` | メインの設定ディレクトリ |

Neovimの設定は [LazyVim](https://www.lazyvim.org/) をベースにしています。

### ディレクトリ構成

~/.config/nvim/
├── init.lua                    # エントリポイント
├── lua/
│   ├── config/
│   │   ├── autocmds.lua        # 自動コマンド
│   │   ├── keymaps.lua         # キーマップ
│   │   ├── lazy.lua            # プラグインマネージャ設定
│   │   └── options.lua         # エディタオプション
│   └── plugins/
│       └── colorscheme.lua     # カラースキーム設定
└── lazy-lock.json              # プラグインのロックファイル

### カスタマイズ方法

#### カラースキームを変更する

`lua/plugins/colorscheme.lua` を編集：

```lua
return {
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    opts = {
      flavour = "frappe",  -- latte, frappe, macchiato, mocha
    },
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "catppuccin",
    },
  },
}

プラグインを追加する

lua/plugins/ 以下に新しいluaファイルを作成：

-- lua/plugins/example.lua
return {
  { "github-user/plugin-name" },
}

エディタオプションを変更する

lua/config/options.lua を編集：

vim.opt.cursorcolumn = true
vim.opt.tabstop = 2

参考リンク

- https://www.lazyvim.org/
- https://github.com/folke/lazy.nvim

## 参考リンク

- [chezmoi 公式ドキュメント](https://www.chezmoi.io/)
- [chezmoi GitHub リポジトリ](https://github.com/twpayne/chezmoi)
