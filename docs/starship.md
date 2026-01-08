# Starship 設定

[Starship](https://starship.rs/) は Rust 製の高速でカスタマイズ可能なシェルプロンプトです。

## 設定ファイル

`~/.config/starship.toml`

## 現在の設定

### Python 設定

ローカルの仮想環境から Python バージョンを表示するよう設定しています。

```toml
[python]
python_binary = ['./venv/bin/python', './.venv/bin/python', 'python', 'python3']
```

検索順序：
1. `./venv/bin/python`（プロジェクト内の venv）
2. `./.venv/bin/python`（プロジェクト内の .venv）
3. `python`（システムの python）
4. `python3`（システムの python3）

## カスタマイズ

### プロンプトの要素を変更

```toml
# 例: Node.js のバージョン表示を無効化
[nodejs]
disabled = true

# 例: Git ブランチの表示形式を変更
[git_branch]
format = "[$symbol$branch]($style) "
```

### プリセットを使用

Starship には複数のプリセットが用意されています。

```bash
# プリセット一覧を確認
starship preset --list

# プリセットを適用
starship preset tokyo-night -o ~/.config/starship.toml
```

## 参考リンク

- [Starship 公式ドキュメント](https://starship.rs/)
- [設定オプション一覧](https://starship.rs/config/)
- [プリセット一覧](https://starship.rs/presets/)
