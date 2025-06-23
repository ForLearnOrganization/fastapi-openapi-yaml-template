#!/usr/bin/env python3
"""
フロントエンド開発者向け型生成スクリプト

TypeScript型定義とAPIクライアントコードを生成します。
OpenAPI仕様から型安全なNext.js開発用ファイルを生成します。
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
    print("🔧 フロントエンド開発者向け型生成プロセスを開始...")
    print("=" * 60)

    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent

    # source/openapi.yaml の存在確認
    yaml_path = project_root / "source" / "openapi.yaml"
    if yaml_path.exists():
        print("📖 手書きOpenAPI仕様から生成します")
        steps = [
            (
                f'"{sys.executable}" scripts/generate_frontend_code.py',
                "YAML仕様からTypeScript型生成",
            ),
        ]
    else:
        print("📖 FastAPIアプリから動的生成します")
        steps = [
            (
                f'"{sys.executable}" scripts/generate_client_types.py',
                "FastAPIからTypeScript型生成",
            ),
        ]

    for command, description in steps:
        full_command = f"cd {project_root} && {command}"
        if run_command(full_command, description) != 0:
            print(f"❌ {description} でエラーが発生しました。処理を中断します。")
            return 1
        print()

    print("🎉 フロントエンド型生成が完了しました！")
    print()
    print("📁 生成されたファイル:")
    print("  🔧 TypeScript型定義: scripts/generated/api-types.ts")
    print("  📊 APIエンドポイント定数: scripts/generated/api-types.ts 内")
    print()
    print("💡 Next.js での使用例:")
    print("  ```typescript")
    print(
        "  import { GenerateTextRequest, apiMethods } from './scripts/generated/api-types';"
    )
    print("  ")
    print("  const response = await apiMethods.generateText({")
    print("    prompt: 'Hello world',")
    print("    max_length: 100")
    print("  });")
    print("  ```")
    print()
    print("🌐 fetchベースAPIクライアント:")
    print("  - APIClientクラスが自動生成されます")
    print("  - 型安全なAPI呼び出しが可能")
    print("  - エラーハンドリング内蔵")
    print()
    print("👥 チーム開発:")
    print("  - バックエンド再生成は: python3 scripts/generate_backend.py")
    print("  - プロジェクト全体: python3 scripts/generate_all.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
