# dotfiles

[chezmoi](https://github.com/twpayne/chezmoi) で管理。

## 使い方

### 初期設定

```bash
$ brew install chezmoi
$ chezmoi init git@github.com:kk6/dotfiles.git
$ chezmoi apply
```

chezmoi は Win でも Linux でも使えるので Mac 以外は公式の使い方参照。

### ファイルを編集する

```bash
$ chezmoi edit ~/.zshrc
(ファイルを編集して保存)
$ chezmoi apply
```
上記の例だと `edit` コマンドで `dotfiles/dot_zshrc` が編集される。そして `apply` コマンドを実行すると、`dot_zshrc` の内容が `~/.zshrc` に反映される。

## ToDo

とりあえず旧 dotfiles で必要なものはこのリポジトリに移動済み。.hg\*関連はもう要らないので削除した。

- プライベートなファイルも暗号化してリポジトリ管理できるっぽいので使い方覚える
- いつの間にか知らないドットファイルたくさん増えてたのでリポジトリ管理したほうが良さそうなものとそうでないものを整理する
