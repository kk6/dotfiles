# mise 設定

[mise](https://mise.jdx.dev/) は、複数のプログラミング言語のバージョン管理を統一的に行うためのツールです。

## 設定ファイル

- **config.toml**: mise の基本設定
  - Python バージョンファイル（`.python-version`）を使用したツール自動有効化
  - 実験的機能の有効化

## 使用方法

```bash
# Python バージョンを自動的に認識・使用
$ mise use python@3.11

# 現在のバージョンを確認
$ mise current

# インストール済みのバージョンを確認
$ mise list
```

## 参考リンク

- [mise 公式ドキュメント](https://mise.jdx.dev/)
