#!/bin/bash
# OpenAPI YAML-first 開発フロー用の統合生成スクリプト

set -e

echo "🚀 OpenAPI YAML-first 開発フロー開始"
echo "=========================================="
echo ""

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# OpenAPI YAML の存在確認
if [ ! -f "source/openapi.yaml" ]; then
    echo "❌ エラー: source/openapi.yaml が見つかりません"
    echo "手書きのOpenAPI YAML仕様ファイルを作成してください。"
    exit 1
fi

echo "📖 OpenAPI YAML 仕様ファイルを確認: source/openapi.yaml"
echo ""

# Python生成スクリプトを実行
python scripts/generate_yaml_first.py

echo ""
echo "✅ OpenAPI YAML-first 開発フロー完了！"
echo ""
echo "🔧 生成されたファイルの確認:"
echo "   ls -la generated/api-types.ts"
echo "   ls -la app/generated/"
echo "   ls -la docs/generated/"
echo "   ls -la docs/static/"
echo ""
echo "🚀 開発サーバー起動:"
echo "   python main.py"