#!/usr/bin/env python3
"""
統合生成スクリプト

バックエンドとフロントエンド両方の成果物を一括生成します。
"""

import os
import subprocess
import sys
import traceback
from pathlib import Path


def run_command(command: str, description: str, cwd: str = None) -> int:
    """コマンドを実行し、結果を表示"""
    print(f"🚀 {description}...")
    try:
        # PYTHONPYCACHEPREFIX環境変数を設定して__pycache__を統合
        env = os.environ.copy()
        env["PYTHONPYCACHEPREFIX"] = ".cache/pycache"

        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            env=env,
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
    print("🔧 統合生成プロセスを開始...")
    print("=" * 60)

    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent

    steps = [
        (f'"{sys.executable}" scripts/generate_backend.py', "バックエンド生成"),
        (f'"{sys.executable}" scripts/generate_frontend.py', "フロントエンド型生成"),
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
    print("  🔧 Pydanticモデル: app/generated/generated_models.py")
    print("  🔧 FastAPIルーター: app/generated/generated_router.py")
    print("  🔧 TypeScript型定義: scripts/generated/api-types.ts")
    print("  📄 HTMLドキュメント: scripts/generated/docs/redoc.html, swagger.html")
    print()
    print("💡 使用方法:")
    print("  - 新しいエンドポイント追加: source/openapi.yaml を編集")
    print("  - 全体再生成: python3 scripts/generate_all.py")
    print("  - バックエンドのみ: python3 scripts/generate_backend.py")
    print("  - フロントエンドのみ: python3 scripts/generate_frontend.py")
    print("  - 開発サーバー起動: python3 main.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
