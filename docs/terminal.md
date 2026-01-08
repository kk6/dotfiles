# ターミナル設定

tmux と Ghostty の設定を管理しています。

## Ghostty

[Ghostty](https://ghostty.org/) は高速で機能豊富なターミナルエミュレータです。

### 設定ファイル

`~/.config/ghostty/config`

### 主な設定

| 設定 | 値 | 説明 |
|------|-----|------|
| `theme` | `Catppuccin Frappe` | カラースキーム |
| `font-family` | `SFMono Square` | フォント |
| `font-size` | `13` | フォントサイズ |
| `macos-non-native-fullscreen` | `true` | macOS 非ネイティブフルスクリーン |

### Quick Terminal

Ghostty の Quick Terminal 機能を使用して、グローバルショートカットでターミナルを呼び出せます。

| 設定 | 値 |
|------|-----|
| `quick-terminal-position` | `top`（画面上部から表示） |
| `quick-terminal-screen` | `main`（メインディスプレイ） |
| キーバインド | `Ctrl+Option+Space` |

## tmux

[tmux](https://github.com/tmux/tmux) はターミナルマルチプレクサです。

### 設定ファイル

`~/.tmux.conf`

### 主な設定

#### マウスサポート

```bash
set-option -g mouse on
```

マウスでのスクロール、ペイン選択、リサイズが可能です。

### プラグイン

[TPM (Tmux Plugin Manager)](https://github.com/tmux-plugins/tpm) を使用しています。

| プラグイン | 説明 |
|-----------|------|
| `tmux-plugins/tpm` | プラグインマネージャ |
| `tmux-plugins/tmux-sensible` | 標準的な設定セット |
| `nhdaly/tmux-better-mouse-mode` | 改善されたマウスサポート |

### プラグインのインストール

```bash
# TPM をインストール（初回のみ）
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# tmux 内でプラグインをインストール
# prefix + I
```

## 参考リンク

- [Ghostty 公式サイト](https://ghostty.org/)
- [Catppuccin テーマ](https://github.com/catppuccin/catppuccin)
- [tmux GitHub](https://github.com/tmux/tmux)
- [TPM GitHub](https://github.com/tmux-plugins/tpm)
