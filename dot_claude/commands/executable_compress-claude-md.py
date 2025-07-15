#!/usr/bin/env python3
"""
CLAUDE.md圧縮スクリプト
コンテキスト使用量を削減するためのCLAUDE.mdファイル圧縮ツール
"""
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class ClaudeMDCompressor:
    """CLAUDE.mdファイルを圧縮するクラス"""

    def __init__(self, claude_md_path: str):
        self.claude_md_path = Path(claude_md_path)
        self.backup_path = self.claude_md_path.with_suffix('.md.backup')
        self.original_content = ""
        self.compressed_content = ""

    def create_backup(self) -> None:
        """元のファイルのバックアップを作成"""
        if not self.claude_md_path.exists():
            raise FileNotFoundError(f"CLAUDE.md not found: {self.claude_md_path}")

        shutil.copy2(self.claude_md_path, self.backup_path)
        print(f"✓ バックアップ作成: {self.backup_path}")

    def load_content(self) -> None:
        """ファイル内容を読み込み"""
        with open(self.claude_md_path, 'r', encoding='utf-8') as f:
            self.original_content = f.read()

    def compress_build_commands(self, content: str) -> str:
        """Build/Test/Lint Commands セクションの圧縮"""
        # セクションの開始と終了を検出
        section_pattern = r'(## Build/Test/Lint Commands.*?)(## \w+|$)'
        match = re.search(section_pattern, content, re.DOTALL)

        if not match:
            return content

        section_content = match.group(1)

        # 重複するコマンドを統合形式に変換
        compressed_section = """## Build/Test/Lint Commands

### Quick Reference
| Task | Make | uv Direct |
|------|------|-----------|
| Install (basic) | `make install` | `uv pip install -e .` |
| Install (vector) | `make install-vector` | `uv pip install -e ".[vector]"` |
| Test (all) | `make test` | `uv run pytest` |
| Test (fast) | `make test-fast` | `uv run pytest -m "not slow"` |
| Test (core) | `make test-core` | `uv run pytest -m "not vector"` |
| Test (coverage) | `make test-cov` | `uv run pytest --cov=minerva` |
| Lint | `make lint` | `uv run ruff check` |
| Format | `make format` | `uv run ruff format` |
| Type check | `make type-check` | `uv run mypy src tests` |
| Dev server | `make dev` | `uv run mcp dev src/minerva/server.py:mcp` |

### Notes
- **Fast tests**: 85% speed improvement, excludes slow integration tests
- **Core tests**: Excludes vector dependency tests
- **Vector tests**: Requires vector dependencies installed
- **Property tests**: Use `uv run pytest tests/*_properties.py`
- **Coverage reports**: Add `--cov-report=html` for HTML reports

"""

        return content.replace(match.group(0), compressed_section + match.group(0)[len(match.group(1)):])

    def compress_code_examples(self, content: str) -> str:
        """長いコード例を簡潔化"""
        # sed コマンドの例を短縮
        sed_pattern = r'(### sed Command Pitfalls.*?)(### \w+|## \w+|$)'
        match = re.search(sed_pattern, content, re.DOTALL)

        if match:
            compressed_sed = """### sed Command Pitfalls ⚠️
**CRITICAL**: `sed` with `[ \\t]` patterns can corrupt files by deleting characters.

**Safe alternatives**:
- `uv run ruff format src/ tests/` (RECOMMENDED)
- `sed -i '' 's/[[:space:]]*$//' file.py` (explicit pattern)
- Verify with `git diff` after using sed

"""
            content = content.replace(match.group(0), compressed_sed + match.group(0)[len(match.group(1)):])

        return content

    def compress_repetitive_sections(self, content: str) -> str:
        """重複的なセクションを統合"""
        # MCP Server Integration の長いコード例を短縮
        mcp_pattern = r'(### MCP Server Integration.*?```python.*?```)'
        matches = re.findall(mcp_pattern, content, re.DOTALL)

        for match in matches:
            if len(match) > 1000:  # 1000文字を超える場合は短縮
                compressed_mcp = """### MCP Server Integration
Server uses `@mcp.tool()` decorators for direct service integration:

```python
@mcp.tool()
def create_note(text: str, filename: str) -> Path:
    return service.create_note(text, filename)

@mcp.tool()
def merge_notes(source_files: list[str], target_filename: str) -> dict:
    result = service.merge_notes(source_files, target_filename)
    return result.to_dict()
```

Key benefits: Direct service calls, no wrapper functions, FastMCP integration."""
                content = content.replace(match, compressed_mcp)

        return content

    def compress_reference_sections(self, content: str) -> str:
        """参照セクションを階層化"""
        # Vector Search の詳細を外部参照に変換
        vector_pattern = r'(#### Essential Vector Search Tools.*?)(#### \w+|### \w+|## \w+|$)'
        match = re.search(vector_pattern, content, re.DOTALL)

        if match:
            compressed_vector = """#### Essential Vector Search Tools
Core tools: `semantic_search()`, `find_similar_notes()`, `build_vector_index()`, `get_vector_index_status()`

**Complete API reference**: See `docs/vector_search_api.md`

**Quick workflow**:
1. `build_vector_index()` - Initial setup
2. `semantic_search("query", limit=5)` - Find content
3. `get_vector_index_status()` - Check status

"""
            content = content.replace(match.group(0), compressed_vector + match.group(0)[len(match.group(1)):])

        return content

    def compress_content(self) -> None:
        """コンテンツの圧縮を実行"""
        content = self.original_content

        # 段階的な圧縮の適用
        content = self.compress_build_commands(content)
        content = self.compress_code_examples(content)
        content = self.compress_repetitive_sections(content)
        content = self.compress_reference_sections(content)

        # 空行の重複を削除
        content = re.sub(r'\n\n\n+', '\n\n', content)

        self.compressed_content = content

    def save_compressed_content(self) -> None:
        """圧縮されたコンテンツを保存"""
        with open(self.claude_md_path, 'w', encoding='utf-8') as f:
            f.write(self.compressed_content)

    def generate_report(self) -> Dict[str, any]:
        """圧縮レポートを生成"""
        original_size = len(self.original_content)
        compressed_size = len(self.compressed_content)
        reduction = original_size - compressed_size
        reduction_percent = (reduction / original_size) * 100

        original_lines = self.original_content.count('\n')
        compressed_lines = self.compressed_content.count('\n')

        return {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'reduction': reduction,
            'reduction_percent': reduction_percent,
            'original_lines': original_lines,
            'compressed_lines': compressed_lines,
            'backup_path': str(self.backup_path)
        }

    def restore_backup(self) -> None:
        """バックアップから復元"""
        if not self.backup_path.exists():
            raise FileNotFoundError(f"バックアップファイルが見つかりません: {self.backup_path}")

        shutil.copy2(self.backup_path, self.claude_md_path)
        print(f"✓ バックアップから復元: {self.claude_md_path}")


def main():
    """メイン実行関数"""
    # プロジェクトのCLAUDE.mdパスを取得
    project_claude_md = Path.cwd() / "CLAUDE.md"

    # グローバルCLAUDE.mdパスを取得
    global_claude_md = Path.home() / ".claude" / "CLAUDE.md"

    # 引数によってファイルを選択
    if len(sys.argv) > 1:
        if sys.argv[1] == "--global":
            claude_md_path = global_claude_md
        elif sys.argv[1] == "--restore":
            # 復元モード
            target_path = global_claude_md if len(sys.argv) > 2 and sys.argv[2] == "--global" else project_claude_md
            compressor = ClaudeMDCompressor(target_path)
            compressor.restore_backup()
            return
        else:
            claude_md_path = Path(sys.argv[1])
    else:
        # デフォルトはプロジェクトのCLAUDE.md
        claude_md_path = project_claude_md

    try:
        # 圧縮処理の実行
        compressor = ClaudeMDCompressor(claude_md_path)

        print(f"CLAUDE.md圧縮開始: {claude_md_path}")
        print("=" * 50)

        # バックアップ作成
        compressor.create_backup()

        # コンテンツ読み込み
        compressor.load_content()

        # 圧縮実行
        print("圧縮処理中...")
        compressor.compress_content()

        # 圧縮結果の保存
        compressor.save_compressed_content()

        # レポート生成
        report = compressor.generate_report()

        # 結果表示
        print("\n✓ 圧縮完了!")
        print(f"元のサイズ: {report['original_size']:,} 文字 ({report['original_lines']} 行)")
        print(f"圧縮後サイズ: {report['compressed_size']:,} 文字 ({report['compressed_lines']} 行)")
        print(f"削減量: {report['reduction']:,} 文字 ({report['reduction_percent']:.1f}%)")
        print(f"バックアップ: {report['backup_path']}")
        print("\n復元する場合: python compress-claude-md.py --restore")

    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
