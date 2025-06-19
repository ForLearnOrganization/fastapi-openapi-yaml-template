# PR検証チェックリスト

このPRで実装された機能を包括的にテストするためのチェックリストです。

## 🏁 事前準備

### 依存関係の確認
```bash
# Poetry環境でのインストール（推奨）
poetry install

# または pip での直接インストール
pip install fastapi uvicorn pydantic pydantic-settings pyyaml httpx
```

### サーバー起動
```bash
# 開発サーバーを起動
poetry run uvicorn main:app --reload
# または
uvicorn main:app --reload

# 成功時の出力例:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [xxxxx] using WatchFiles
# INFO:     Started server process [xxxxx]
```

## 📖 ドキュメント生成機能の検証

### 自動生成ドキュメント
- [ ] **OpenAPI JSON生成**: `python scripts/generate_docs_only.py`
  - [ ] `docs/generated/openapi.json` が生成される
  - [ ] JSONが正しい形式である

- [ ] **OpenAPI YAML生成**: ファイル確認
  - [ ] `docs/generated/openapi.yaml` が生成される
  - [ ] YAMLが正しい形式である

- [ ] **静的HTML生成**: ファイル確認
  - [ ] `docs/static/swagger.html` が生成される
  - [ ] `docs/static/redoc.html` が生成される
  - [ ] HTMLファイルが正常に開ける

### インタラクティブドキュメント
- [ ] **Swagger UI**: http://localhost:8000/docs
  - [ ] 全エンドポイントが表示される
  - [ ] Try it out機能が動作する
  - [ ] 日本語コメントが正しく表示される

- [ ] **ReDoc**: http://localhost:8000/redoc
  - [ ] 全エンドポイントが表示される
  - [ ] 階層構造が適切に表示される
  - [ ] サンプルデータが正しく表示される

## 🚀 API エンドポイントの検証

### ヘルスチェック系
- [ ] **基本ヘルスチェック**
```bash
curl -X GET "http://localhost:8000/api/v1/health/"
# 期待結果: {"status": "healthy", "timestamp": "..."}
```

- [ ] **詳細ヘルスチェック**
```bash
curl -X GET "http://localhost:8000/api/v1/health/detailed"
# 期待結果: システム情報と稼働時間が含まれるJSON
```

### テキスト生成系
- [ ] **テキスト生成（新エンドポイント）**
```bash
curl -X POST "http://localhost:8000/api/v1/text/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "こんにちは", "max_length": 50}'
# 期待結果: 生成されたテキストと metadata を含むJSON
```

- [ ] **後方互換性エンドポイント**
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello world", "max_length": 100}'
# 期待結果: 新エンドポイントと同じ機能が動作
```

- [ ] **テキストエコー**
```bash
curl -X POST "http://localhost:8000/api/v1/text/echo" \
     -H "Content-Type: application/json" \
     -d '{"text": "テストメッセージ"}'
# 期待結果: テキスト分析と統計情報を含むJSON
```

### 外部API連携（モックデータ）
- [ ] **天気情報**
```bash
curl -X POST "http://localhost:8000/api/v1/external/weather" \
     -H "Content-Type: application/json" \
     -d '{"location": "東京", "date": "2024-01-01"}'
# 期待結果: モック天気データを含むJSON
```

- [ ] **ランダム名言**
```bash
curl -X GET "http://localhost:8000/api/v1/external/quote"
# 期待結果: {"quote": "...", "author": "...", "category": "..."}
```

- [ ] **ランダム雑学**
```bash
curl -X GET "http://localhost:8000/api/v1/external/fact"
# 期待結果: {"fact": "...", "category": "...", "source": "..."}
```

- [ ] **プログラミングジョーク**
```bash
curl -X GET "http://localhost:8000/api/v1/external/joke"
# 期待結果: {"joke": "...", "type": "programming", "rating": "..."}
```

## ⚙️ 型生成システムの検証

### TypeScript型生成
- [ ] **型生成の実行**
```bash
python scripts/generate_code_only.py
# または
./scripts/generate_code_only.sh
```

- [ ] **生成ファイルの確認**
  - [ ] `generated/api-types.ts` が生成される
  - [ ] 全てのリクエスト・レスポンス型が含まれる
  - [ ] API_ENDPOINTS定数が正しく生成される

### APIルーター自動生成
- [ ] **ルーター生成の実行**
```bash
python scripts/generate_router.py
```

- [ ] **生成ファイルの確認**
  - [ ] `app/api/v1/__init__.py` が更新される
  - [ ] 全エンドポイントのインポートが含まれる
  - [ ] ルーター登録が正しく生成される

## 🛠️ 開発ツールの検証

### コード品質ツール
- [ ] **Ruff フォーマット**
```bash
ruff format .
# 期待結果: コードが適切にフォーマットされる
```

- [ ] **Ruff リント**
```bash
ruff check .
# 期待結果: エラーなしまたは修正可能な警告のみ
```

### 包括的生成スクリプト
- [ ] **全生成実行**
```bash
./scripts/generate_all.sh
# 期待結果: ドキュメント、型、ルーターが全て更新される
```

- [ ] **ドキュメント専用生成**
```bash
./scripts/generate_docs_only.sh
# 期待結果: HTMLドキュメントのみ生成される
```

- [ ] **コード専用生成**
```bash
./scripts/generate_code_only.sh
# 期待結果: TypeScript型とルーターのみ生成される
```

## 🌐 CORS設定の検証

### ブラウザからのアクセス
- [ ] **CORSヘッダーの確認**
```bash
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS "http://localhost:8000/api/v1/text/generate"
# 期待結果: Access-Control-Allow-Origin ヘッダーが返される
```

## 🎯 設定ファイルの検証

### YAML設定
- [ ] **config.yaml の読み込み**
  - [ ] アプリ起動時にエラーが出ない
  - [ ] 設定値が正しく反映される

### VSCode設定
- [ ] **.vscode/settings.json の確認**
  - [ ] 保存時の自動フォーマットが動作する
  - [ ] Ruffが正しく設定されている

## 📊 パフォーマンス確認

### レスポンス時間
- [ ] **基本エンドポイントの速度**
```bash
time curl -X GET "http://localhost:8000/api/v1/health/"
# 期待結果: 数百ミリ秒以内での応答
```

### 同時接続テスト
- [ ] **複数リクエストの処理**
```bash
# 複数のターミナルで同時実行
curl -X POST "http://localhost:8000/api/v1/text/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "テスト", "max_length": 30}' &
curl -X GET "http://localhost:8000/api/v1/health/" &
curl -X GET "http://localhost:8000/api/v1/external/quote" &
wait
# 期待結果: 全てのリクエストが正常に処理される
```

## 🧪 エラーハンドリングの検証

### 不正なリクエスト
- [ ] **必須パラメータ不足**
```bash
curl -X POST "http://localhost:8000/api/v1/text/generate" \
     -H "Content-Type: application/json" \
     -d '{}'
# 期待結果: 422 Validation Error
```

- [ ] **存在しないエンドポイント**
```bash
curl -X GET "http://localhost:8000/api/v1/nonexistent"
# 期待結果: 404 Not Found
```

### データ型エラー
- [ ] **不正な型のデータ**
```bash
curl -X POST "http://localhost:8000/api/v1/text/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": 123, "max_length": "abc"}'
# 期待結果: 422 Validation Error
```

## 📝 ドキュメント確認

### README.md
- [ ] セットアップ手順が正確である
- [ ] 使用例が動作する
- [ ] 運用フローが明確に記載されている

### API仕様書
- [ ] 全エンドポイントが文書化されている
- [ ] リクエスト・レスポンス例が正確である
- [ ] エラーレスポンスが記載されている

## 🔧 開発フロー確認

### エンドポイント追加フロー
- [ ] `app/api/endpoint_registry.py` への追加が簡単
- [ ] 自動生成で正しくルーターに反映される
- [ ] TypeScript型も自動で生成される

### チーム開発フロー
- [ ] バックエンド：Pydanticモデル定義 → スキーマ自動生成
- [ ] フロントエンド：型ファイル取得 → 型安全な実装
- [ ] 両チーム：APIドキュメントでの仕様確認

## ✅ 最終確認項目

- [ ] 全APIエンドポイントが正常に動作
- [ ] ドキュメント生成が完全に機能
- [ ] 型生成システムが正常に動作  
- [ ] 後方互換性が保たれている
- [ ] エラーハンドリングが適切
- [ ] CORS設定が正しく動作
- [ ] 開発ツールチェーンが完動
- [ ] プロジェクト構造が整理されている

---

## 🚨 問題が発生した場合

### よくある問題と解決方法

1. **モジュールインポートエラー**
   ```bash
   # プロジェクトルートでPythonパスを確認
   export PYTHONPATH="."
   python scripts/generate_docs.py
   ```

2. **ポート競合エラー**
   ```bash
   # 別のポートで起動
   uvicorn main:app --reload --port 8001
   ```

3. **依存関係エラー**
   ```bash
   # 依存関係を再インストール
   pip install --upgrade -r requirements.txt
   # または
   poetry install --sync
   ```

各項目をチェックして、全て✅になることを確認してください。