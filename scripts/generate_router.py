#!/usr/bin/env python3
"""
APIルーター自動生成スクリプト

endpoint_registry.py に定義されたエンドポイント設定から、
自動でルーターのインクルード文を生成します。
"""

import sys
from pathlib import Path
from typing import List

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.api.endpoint_registry import get_endpoint_list, EndpointConfig


def generate_router_code() -> str:
    """ルーターコードを自動生成"""
    endpoints = get_endpoint_list()
    
    # インポート文を生成
    import_lines = []
    for config in endpoints:
        module_parts = config.module.split('.')
        module_name = module_parts[-1]  # 最後の部分をエイリアスとして使用
        import_lines.append(f"from {config.module} import {config.router_name} as {module_name}_router")
    
    # ルーター登録文を生成
    include_lines = []
    for config in endpoints:
        module_name = config.module.split('.')[-1]
        include_lines.append(
            f'api_router.include_router({module_name}_router, prefix="{config.prefix}", tags={config.tags})'
        )
    
    # 完全なコードを生成
    code = f'''"""Main API router for version 1."""

from fastapi import APIRouter

# 自動生成されたインポート文
{chr(10).join(import_lines)}

# Create main API router
api_router = APIRouter()

# 自動生成されたルーター登録
{chr(10).join(include_lines)}


# =============================================================================
# 🔧 エンドポイント追加方法
# =============================================================================
# 新しいエンドポイントを追加するには:
# 1. app/api/endpoint_registry.py にエンドポイント設定を追加
# 2. app/api/v1/endpoints/ に対応する実装ファイルを作成
# 3. このスクリプトを実行: python scripts/generate_router.py
# =============================================================================

'''
    
    return code


def write_router_file(code: str) -> Path:
    """生成されたコードをファイルに書き込み"""
    router_file = project_root / "app" / "api" / "v1" / "__init__.py"
    
    with open(router_file, "w", encoding="utf-8") as f:
        f.write(code)
    
    return router_file


def validate_endpoints():
    """エンドポイント設定の妥当性をチェック"""
    endpoints = get_endpoint_list()
    errors = []
    
    for config in endpoints:
        # モジュールファイルの存在チェック
        module_path = project_root / config.module.replace('.', '/') / "__init__.py"
        if not module_path.exists():
            # __init__.py がない場合は .py ファイルをチェック
            module_file = project_root / (config.module.replace('.', '/') + '.py')
            if not module_file.exists():
                errors.append(f"モジュールファイルが見つかりません: {module_file}")
    
    return errors


def main():
    """メイン処理"""
    print("🚀 APIルーター自動生成を開始...")
    
    # エンドポイント設定の妥当性チェック
    print("🔍 エンドポイント設定をチェック中...")
    errors = validate_endpoints()
    
    if errors:
        print("❌ エラーが発見されました:")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    print("✅ エンドポイント設定は正常です")
    
    # ルーターコード生成
    print("📝 ルーターコードを生成中...")
    code = generate_router_code()
    
    # ファイルに書き込み
    router_file = write_router_file(code)
    print(f"✅ ルーターファイルを生成: {router_file}")
    
    # エンドポイント一覧を表示
    print("\n📍 生成されたエンドポイント:")
    endpoints = get_endpoint_list()
    for config in endpoints:
        print(f"  - {config.prefix} ({', '.join(config.tags)})")
    
    print("\n🎉 APIルーター自動生成が完了しました！")
    return 0


if __name__ == "__main__":
    sys.exit(main())