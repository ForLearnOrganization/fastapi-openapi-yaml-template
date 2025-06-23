#!/usr/bin/env python3
"""
バックエンド開発者向け統合生成スクリプト

APIエンドポイント、Pydanticモデル、ドキュメントを生成します。
フロントエンド用の型定義は含まれません。
"""

import subprocess
import sys
import traceback
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
        # デバッグ用のトレースバック表示
        print("🔍 詳細トレースバック:")
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}")
        print("🔍 詳細トレースバック:")
        traceback.print_exc()
        return 1


def main():
    """メイン処理"""
    print("🔧 バックエンド開発者向け統合生成プロセスを開始...")
    print("=" * 60)

    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent

    steps = [
        (f'"{sys.executable}" scripts/generate_from_yaml.py', "YAML-firstコード生成"),
        (f'"{sys.executable}" scripts/generate_docs.py', "HTMLドキュメント生成"),
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
    print("  🔧 Pydanticモデル: app/generated/generated_models.py")
    print("  🔧 FastAPIルーター: app/generated/generated_router.py")
    print("  📄 HTMLドキュメント: scripts/generated/docs/redoc.html, swagger.html")
    print()
    print("💡 使用方法:")
    print("  - 新しいエンドポイント追加: source/openapi.yaml を編集")
    print("  - バックエンド再生成: python3 scripts/generate_backend.py")
    print("  - 完全再生成: python3 scripts/generate_yaml_first.py")
    print("  - 開発サーバー起動: python3 main.py")
    print()
    print("👥 チーム開発:")
    print("  - フロントエンド型生成は: python3 scripts/generate_frontend.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
