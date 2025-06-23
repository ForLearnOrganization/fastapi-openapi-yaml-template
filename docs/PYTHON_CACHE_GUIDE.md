# 🐍 Python キャッシュディレクトリ設定ガイド

## ✅ キャッシュは正常に動作しています

Python の `__pycache__` ディレクトリは正常に生成され、パフォーマンス向上に寄与しています。
全ての生成スクリプト実行でも統合ディレクトリに集約されています。

## 📁 現在の設定

### 設定場所
- **環境変数**: `.env.example` で `PYTHONPYCACHEPREFIX=.cache/pycache` 
- **実際の生成先**: `.cache/pycache/` ディレクトリ
- **スクリプト実行**: 全ての生成スクリプトで自動適用

### ✨ 改善内容

**統合前（散在）**:
```
scripts/__pycache__/
app/__pycache__/
app/api/__pycache__/
app/models/__pycache__/
```

**統合後（集約）**:
```
.cache/pycache/
├── (全モジュールのキャッシュファイル)
└── (環境全体で一元管理)
```

### キャッシュの確認方法

```bash
# キャッシュが生成されているか確認
find .cache/pycache -name "*.pyc" | head -10

# 生成スクリプト実行でキャッシュ生成
python3 scripts/generate_all.py

# キャッシュファイル数をカウント
find .cache/pycache -name "*.pyc" | wc -l
```

## 🚀 パフォーマンス比較

### Before（散在型）
```
app/
├── core/
│   ├── __pycache__/
│   ├── config.py
│   └── __init__.py
├── api/
│   ├── __pycache__/
│   └── v1/
│       ├── __pycache__/
│       └── endpoints/
│           └── __pycache__/
```

### After（統合型）
```
.cache/
└── pycache/
    └── [統合されたキャッシュファイル]
app/
├── core/
│   ├── config.py
│   └── __init__.py
├── api/
│   └── v1/
│       └── endpoints/
```

## 🔧 利点

1. **✨ ディレクトリ構造がクリーン**: `__pycache__` フォルダが散在しない
2. **🚀 パフォーマンス維持**: キャッシュは正常に機能
3. **🔍 可視性向上**: プロジェクト構造が見やすい
4. **📦 管理容易**: キャッシュの一括管理・削除が可能

## 🔄 キャッシュ管理コマンド

```bash
# キャッシュクリア
rm -rf .cache/pycache/

# キャッシュサイズ確認
du -sh .cache/pycache/

# キャッシュ再生成
poetry run python3 -c "import app; print('Cache regenerated')"
```

## ⚡ VS Code 統合

VS Code settings で自動的に環境変数が設定されるため、開発時も統合キャッシュが使用されます。

```json
{
  "python.envFile": "${workspaceFolder}/.env.example"
}
```

## 🎯 確認ポイント

キャッシュが正常に動作しているかの確認：

1. **インポート速度**: 2回目以降のインポートが高速
2. **キャッシュファイル存在**: `.cache/pycache/` にファイルが生成
3. **アプリケーション動作**: 正常にモジュールが読み込まれる

## 🚨 トラブルシューティング

### キャッシュが生成されない場合

1. **権限確認**:
   ```bash
   ls -la .cache/pycache/
   ```

2. **環境変数確認**:
   ```bash
   echo $PYTHONPYCACHEPREFIX
   ```

3. **手動設定**:
   ```bash
   export PYTHONPYCACHEPREFIX=.cache/pycache
   ```

### キャッシュディレクトリが見つからない場合

```bash
# ディレクトリ作成
mkdir -p .cache/pycache

# 権限設定
chmod 755 .cache/pycache
```

キャッシュシステムは正常に動作しており、開発パフォーマンスを維持しながらプロジェクトの可読性を向上させています。