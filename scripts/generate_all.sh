#!/bin/bash

# 統合生成シェルスクリプト
# APIエンドポイント、型定義、ドキュメントを一括生成

set -e

echo "🔧 統合生成プロセスを開始..."

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# Python統合生成スクリプトを実行
python scripts/generate_all.py

echo ""
echo "✅ 統合生成が完了しました！"