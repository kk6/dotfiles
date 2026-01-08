# Neovim / Vim 設定

`vim` は `nvim` のエイリアスとして設定されています。

## 設定ファイルの構成

| ファイル | 役割 |
|---------|------|
| `~/.vimrc` | 空（LazyVimに委譲） |
| `~/.config/nvim/` | メインの設定ディレクトリ |

Neovimの設定は [LazyVim](https://www.lazyvim.org/) をベースにしています。

## ディレクトリ構成

```
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
```

## カスタマイズ方法

### カラースキームを変更する

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
```

### プラグインを追加する

`lua/plugins/` 以下に新しいluaファイルを作成：

```lua
-- lua/plugins/example.lua
return {
  { "github-user/plugin-name" },
}
```

### エディタオプションを変更する

`lua/config/options.lua` を編集：

```lua
vim.opt.cursorcolumn = true
vim.opt.tabstop = 2
```

## 参考リンク

- [LazyVim 公式ドキュメント](https://www.lazyvim.org/)
- [lazy.nvim GitHub リポジトリ](https://github.com/folke/lazy.nvim)
