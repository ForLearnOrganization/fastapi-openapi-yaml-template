#!/usr/bin/env python3
"""
統合生成スクリプト

APIエンドポイント、型定義、ドキュメントを一括で生成します。
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> int:
    """コマンドを実行し、結果を表示"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ エラーが発生しました: {e}")
        if e.stderr:
            print(f"エラー詳細: {e.stderr}")
        return 1


def main():
    """メイン処理"""
    print("🔧 統合生成プロセスを開始...")
    print("=" * 60)
    
    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent
    
    steps = [
        ("python scripts/generate_router.py", "APIルーター自動生成"),
        ("python scripts/generate_docs.py", "ドキュメント・型定義生成"),
    ]
    
    for command, description in steps:
        full_command = f"cd {project_root} && {command}"
        if run_command(full_command, description) != 0:
            print(f"❌ {description} でエラーが発生しました。処理を中断します。")
            return 1
        print()
    
    print("🎉 すべての生成処理が完了しました！")
    print()
    print("📁 生成されたファイル:")
    print("  🔧 APIルーター: app/api/v1/__init__.py")
    print("  📊 OpenAPIスキーマ: docs/generated/openapi.json, openapi.yaml")
    print("  🔧 TypeScript型定義: generated/api-types.ts")
    print("  📄 HTMLドキュメント: docs/static/redoc.html, swagger.html")
    print()
    print("💡 使用方法:")
    print("  - 新しいエンドポイント追加: app/api/endpoint_registry.py を編集")
    print("  - 再生成: ./scripts/generate_all.sh")
    print("  - 開発サーバー起動: python main.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())