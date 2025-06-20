#!/usr/bin/env python3
"""
バックエンド開発者向け統合生成スクリプト

APIエンドポイント、Pydanticモデル、ドキュメントを生成します。
フロントエンド用の型定義は含まれません。
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str, cwd: str = None) -> int:
    """コマンドを実行し、結果を表示"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd,
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
    print("🔧 バックエンド開発者向け統合生成プロセスを開始...")
    print("=" * 60)
    
    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent
    
    steps = [
        ("python3 scripts/generate_router.py", "APIルーター自動生成"),
        ("python3 scripts/generate_docs.py", "HTMLドキュメント生成"),
    ]
    
    for command, description in steps:
        full_command = f"cd {project_root} && {command}"
        if run_command(full_command, description) != 0:
            print(f"❌ {description} でエラーが発生しました。処理を中断します。")
            return 1
        print()
    
    print("🎉 バックエンド開発処理が完了しました！")
    print()
    print("📁 生成されたファイル:")
    print("  🔧 APIルーター: app/api/v1/__init__.py")
    print("  📄 HTMLドキュメント: docs/static/redoc.html, swagger.html")
    print("  📊 OpenAPIスキーマ: docs/generated/openapi.json, openapi.yaml")
    print()
    print("💡 使用方法:")
    print("  - 新しいエンドポイント追加: app/api/endpoint_registry.py を編集")
    print("  - バックエンド再生成: python3 scripts/generate_backend.py")
    print("  - 開発サーバー起動: python3 main.py")
    print()
    print("👥 チーム開発:")
    print("  - フロントエンド型生成は: python3 scripts/generate_frontend.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())