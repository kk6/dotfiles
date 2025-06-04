# dotfiles

個人用のdotfiles設定を [chezmoi](https://github.com/twpayne/chezmoi) で管理しています。

## 管理されているファイル

- **シェル設定**: `.zshrc`, `.zshenv`, `.zprofile`
- **エディタ設定**: `.vimrc`, `.editorconfig`, Neovim設定
- **開発ツール**: Git設定, Starship設定, Flake8設定
- **ターミナル**: `.tmux.conf`, Ghostty設定
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

### プライベートファイルの管理

暗号化が必要なプライベートファイル（APIキーなど）は `private_` プレフィックスを使用して管理できます。

```bash
# プライベートファイルの追加
$ chezmoi add --private ~/.npmrc
```

## 参考リンク

- [chezmoi 公式ドキュメント](https://www.chezmoi.io/)
- [chezmoi GitHub リポジトリ](https://github.com/twpayne/chezmoi)

## ToDo

- [ ] AGE暗号化を使用したプライベートファイルの管理設定
- [ ] テンプレート機能を使用した環境固有の設定管理
- [ ] 不要になったドットファイルの整理と削除
