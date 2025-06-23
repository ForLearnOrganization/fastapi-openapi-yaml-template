#!/usr/bin/env python3
"""
OpenAPI YAML-first 統合生成スクリプト

手書きのopenapi.yamlからコード、型定義、ドキュメントを一括生成します。
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
    print("🔧 OpenAPI YAML-first 統合生成プロセスを開始...")
    print("=" * 60)

    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent

    # source/openapi.yaml の存在確認
    yaml_path = project_root / "source" / "openapi.yaml"
    if not yaml_path.exists():
        print(f"❌ 必要なファイルが見つかりません: {yaml_path}")
        print("手書きのOpenAPI YAML仕様ファイルを作成してください。")
        return 1

    print(f"📖 OpenAPI YAML仕様を確認: {yaml_path}")
    print()

    steps = [
        (
            f'"{sys.executable}" scripts/generate_types_from_yaml.py',
            "TypeScript型定義・OpenAPIファイル生成",
        ),
        (
            f'"{sys.executable}" scripts/generate_from_yaml.py',
            "Pydanticモデル・FastAPIルーター生成",
        ),
        (f'"{sys.executable}" scripts/generate_docs.py', "HTMLドキュメント生成"),
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
    print("  📊 ソース仕様: source/openapi.yaml")
    print("  🔧 TypeScript型定義: scripts/generated/api-types.ts")
    print("  📄 OpenAPIドキュメント: docs/generated/openapi.{json,yaml}")
    print("  🏗️ Pydanticモデル: app/generated/generated_models.py")
    print("  🌐 FastAPIルーター: app/generated/generated_router.py")
    print("  📖 HTMLドキュメント: scripts/generated/docs/{swagger,redoc}.html")
    print()
    print("🔄 開発フロー:")
    print("  1. 📝 source/openapi.yaml を編集（API仕様の更新）")
    print("  2. 🚀 python3 scripts/generate_all.py を実行（全自動生成）")
    print("  3. 🛠️ 必要に応じて生成されたスタブに実装を追加")
    print("  4. 🧪 開発サーバーでテスト: python3 main.py")
    print("  5. 📦 Next.jsで scripts/generated/api-types.ts を使用")
    print()
    print("💡 チーム開発での使用:")
    print("  - バックエンド担当者: source/openapi.yaml の仕様策定")
    print("  - フロントエンド担当者: 仕様確認・合意")
    print("  - 合意後: 型生成してそれぞれ開発進行")
    print("  - フロント側: fetchベースAPIクライアント使用")

    return 0


if __name__ == "__main__":
    sys.exit(main())
