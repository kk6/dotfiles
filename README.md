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

## ドキュメント

各ツールの詳細な設定については以下を参照してください：

| ドキュメント | 内容 |
|-------------|------|
| [docs/neovim.md](docs/neovim.md) | Neovim / Vim 設定 |
| [docs/mise.md](docs/mise.md) | mise によるバージョン管理 |
| [dot_claude/README.md](dot_claude/README.md) | Claude Code カスタムコマンド |

## 注意事項

- このリポジトリは個人用の設定を管理するためのものであり、他のユーザーが使用することを意図していません。
- 変更を加える際は、事前にバックアップを取ることをおすすめします。

## 参考リンク

- [chezmoi 公式ドキュメント](https://www.chezmoi.io/)
- [chezmoi GitHub リポジトリ](https://github.com/twpayne/chezmoi)
