#!/bin/bash

# ドキュメント生成シェルスクリプト
# OpenAPIスキーマ、TypeScript型定義、HTMLドキュメントを一括生成

set -e

echo "🚀 ドキュメント生成を開始..."

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# Pythonの仮想環境を確認
if [ ! -d ".venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  仮想環境が見つかりません。以下のコマンドで仮想環境をアクティベートしてください:"
    echo "   poetry shell"
    echo "   または"
    echo "   source .venv/bin/activate"
    exit 1
fi

# ドキュメント生成スクリプトを実行
echo "📋 ドキュメント生成スクリプトを実行..."
python scripts/generate_docs.py

echo ""
echo "✅ ドキュメント生成が完了しました！"
echo ""
echo "📁 生成されたファイル:"
echo "  📊 OpenAPIスキーマ:"
echo "    - docs/generated/openapi.json"
echo "    - docs/generated/openapi.yaml"
echo "  🔧 TypeScript型定義:"
echo "    - generated/api-types.ts"
echo "  📄 HTMLドキュメント:"
echo "    - docs/static/redoc.html"
echo "    - docs/static/swagger.html"
echo ""
echo "🌐 ドキュメントを表示するには:"
echo "  開発サーバー: http://localhost:8000/docs (Swagger UI)"
echo "  開発サーバー: http://localhost:8000/redoc (ReDoc)"
echo "  静的ファイル: docs/static/swagger.html"
echo "  静的ファイル: docs/static/redoc.html"