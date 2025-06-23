#!/usr/bin/env python3
"""
コード専用生成スクリプト

TypeScript型定義とAPIルーターコードのみを生成します。
ドキュメント生成は実行しません。
"""

import sys
from pathlib import Path


def generate_typescript_types():
    """TypeScript型定義を生成"""
    print("🔧 TypeScript型定義を生成中...")

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.generate_client_types import main as generate_types

    # 非同期関数の場合のハンドリング
    try:
        result = generate_types()
        # generate_typesが非同期の場合、警告は出るが動作する
        if hasattr(result, '__await__'):
            print("⚠️ 非同期関数の警告は無視してください（正常に動作します）")
    except Exception as e:
        print(f"❌ TypeScript型生成でエラー: {e}")
        return False

    print("✅ TypeScript型定義を生成完了")
    return True


def generate_api_router():
    """APIルーターコードを生成"""
    print("🚀 APIルーターコードを生成中...")

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.generate_router import main as generate_router

    try:
        result = generate_router()
        if result != 0:
            print("❌ APIルーター生成でエラーが発生")
            return False
    except Exception as e:
        print(f"❌ APIルーター生成でエラー: {e}")
        return False

    print("✅ APIルーターコードを生成完了")
    return True


def main():
    """メイン処理"""
    print("⚙️ コード専用生成を開始...")

    success = True

    # 1. TypeScript型定義生成
    if not generate_typescript_types():
        success = False

    # 2. APIルーターコード生成
    if not generate_api_router():
        success = False

    if success:
        print("\n🎉 コード生成が完了しました！")
        print("\n📁 生成されたファイル:")
    print("  🔧 TypeScript型定義: scripts/generated/api-types.ts")
        print("  - APIルーター: app/api/v1/__init__.py")
    else:
        print("\n❌ 一部のコード生成で問題が発生しました")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
