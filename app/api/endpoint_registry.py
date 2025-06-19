"""
APIエンドポイント自動生成システム

このファイルはすべてのAPIエンドポイントを一覧できるレジストリです。
ここでエンドポイントを定義すると、自動でルーターが生成されます。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class EndpointConfig:
    """エンドポイント設定"""
    
    prefix: str  # URLプレフィックス（例: "/health"）
    tags: List[str]  # OpenAPIタグ
    module: str  # インポートするモジュール名（例: "app.api.v1.endpoints.health"）
    router_name: str = "router"  # モジュール内のルーター変数名
    description: str = ""  # エンドポイントの説明


# =============================================================================
# 🔧 エンドポイント設定レジストリ
# =============================================================================
# 新しいエンドポイントを追加する場合は、下記のリストに追加してください。
# 対応する実装ファイルも app/api/v1/endpoints/ に作成してください。

ENDPOINT_REGISTRY: List[EndpointConfig] = [
    # ヘルスチェック系エンドポイント
    EndpointConfig(
        prefix="/health",
        tags=["health"],
        module="app.api.v1.endpoints.health",
        description="アプリケーションの状態監視エンドポイント",
    ),
    
    # テキスト生成系エンドポイント
    EndpointConfig(
        prefix="/text",
        tags=["text"],
        module="app.api.v1.endpoints.text",
        description="テキスト生成・処理エンドポイント",
    ),
    
    # 外部API連携エンドポイント
    EndpointConfig(
        prefix="/external",
        tags=["external"],
        module="app.api.v1.endpoints.external",
        description="外部サービス連携エンドポイント（モックデータ）",
    ),
]


def get_endpoint_list() -> List[EndpointConfig]:
    """登録されている全エンドポイント設定を取得"""
    return ENDPOINT_REGISTRY


def print_endpoint_summary():
    """エンドポイント一覧をコンソールに表示（デバッグ用）"""
    print("🔧 登録済みAPIエンドポイント:")
    print("=" * 60)
    
    for config in ENDPOINT_REGISTRY:
        print(f"📍 {config.prefix}")
        print(f"   タグ: {', '.join(config.tags)}")
        print(f"   モジュール: {config.module}")
        print(f"   説明: {config.description}")
        print()


if __name__ == "__main__":
    # このファイルを直接実行すると、エンドポイント一覧が表示されます
    print_endpoint_summary()