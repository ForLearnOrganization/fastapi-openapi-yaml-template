# 📘 OpenAPI YAML-first 開発ガイド

## 概要

このプロジェクトは **OpenAPI YAML-first** アプローチを採用しています。手書きの `source/openapi.yaml` ファイルを起点として、バックエンドのPydanticモデル・FastAPIエンドポイント、フロントエンドのTypeScript型定義を自動生成します。

## 🔄 開発フロー

### 1. API仕様の策定
```bash
# source/openapi.yaml を編集
vim source/openapi.yaml
```

**バックエンド担当者**が以下を定義：
- API エンドポイント（パス、メソッド、パラメータ）
- リクエスト・レスポンススキーマ
- エラーレスポンス
- API ドキュメント

### 2. フロントエンドとの仕様合意
**フロントエンド担当者**が仕様を確認：
- エンドポイント設計の妥当性
- データ構造の確認
- エラーハンドリング戦略

### 3. コード・型生成
仕様合意後、一括生成：
```bash
./scripts/generate_yaml_first.sh
```

または個別実行：
```bash
# TypeScript型定義生成
python scripts/generate_frontend_code.py

# Pythonコード生成
python scripts/generate_backend_code.py

# HTMLドキュメント生成
python scripts/generate_docs.py
```

### 4. 実装フェーズ
**バックエンド**: 生成されたスタブに実装追加
```python
# app/generated/generated_router.py
async def generate_text(request: GenerateTextRequest) -> GenerateTextResponse:
    # TODO: 実装が必要 → 実際の処理に置き換え
    result = your_llm_service.generate(request.prompt, request.max_length)
    return GenerateTextResponse(
        generated_text=result.text,
        input_prompt=request.prompt,
        metadata={"method": "llm", "model": result.model}
    )
```

**フロントエンド**: 生成された型定義を使用
```typescript
import { GenerateTextRequest, apiMethods } from './generated/api-types';

const handleGenerate = async () => {
  try {
    const response = await apiMethods.generateText({
      prompt: userInput,
      max_length: 100,
      temperature: 0.7
    });
    setGeneratedText(response.generated_text);
  } catch (error) {
    console.error('API Error:', error);
  }
};
```

## 🗂️ ファイル管理

### ソース管理（手動編集）
```
source/
├── openapi.yaml     # API仕様定義（ソース・オブ・トゥルース）
└── config.yaml     # アプリケーション設定
```

### 自動生成（編集禁止）
```
app/generated/
├── generated_models.py      # Pydanticモデル
└── generated_router.py      # FastAPIルータースタブ

generated/
└── api-types.ts            # TypeScript型定義

docs/generated/
├── openapi.json            # OpenAPI JSON仕様
└── openapi.yaml            # OpenAPI YAML仕様（整形済み）

docs/static/
├── swagger.html            # Swagger UI
└── redoc.html             # ReDoc
```

## 📝 OpenAPI YAML 編集ガイド

### 基本構造
```yaml
openapi: 3.1.0
info:
  title: API名
  description: API説明
  version: 1.0.0

paths:
  /api/v1/example:
    post:
      tags: [example]
      summary: サマリー
      description: 詳細説明
      operationId: example_operation
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExampleRequest'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ExampleResponse'

components:
  schemas:
    ExampleRequest:
      type: object
      properties:
        field1:
          type: string
          description: フィールド説明
      required:
        - field1
```

### スキーマ設計のベストプラクティス

1. **明確な命名**: `UserCreateRequest`, `UserResponse` など目的を明示
2. **適切な型制約**: `minimum`, `maximum`, `minLength`, `maxLength` を設定
3. **詳細な説明**: 各フィールドに `description` を記述
4. **必須フィールド**: `required` で明示的に指定
5. **エラーレスポンス**: 統一されたエラー形式を定義

### 型生成における注意点

- `operationId` は関数名になるため、有効なPython/TypeScript識別子にする
- `$ref` はモデル名になるため、PascalCase を推奨
- `enum` 値は文字列リテラル型として生成される
- `anyOf` での null を含む場合は Optional 型として処理

## 🛠️ 運用コマンド

### 開発時
```bash
# YAML編集後の再生成
./scripts/generate_yaml_first.sh

# 開発サーバー起動
python main.py

# 型チェック（TypeScript）
npx tsc --noEmit generated/api-types.ts
```

### ドキュメント確認
```bash
# 静的ドキュメント生成
python scripts/generate_docs.py

# ブラウザで確認
open docs/static/swagger.html
open docs/static/redoc.html
```

### デバッグ
```bash
# 生成された内容の確認
cat app/generated/generated_models.py
cat app/generated/generated_router.py
cat generated/api-types.ts
```

## 🚀 CI/CD 統合例

```yaml
# .github/workflows/api-validation.yml
name: API Validation
on: [push, pull_request]

jobs:
  validate-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate OpenAPI
        run: |
          pip install pyyaml
          python -c "import yaml; yaml.safe_load(open('source/openapi.yaml'))"

      - name: Generate and Test
        run: |
          ./scripts/generate_yaml_first.sh
          python -m pytest tests/
          npx tsc --noEmit generated/api-types.ts
```

## 📋 チェックリスト

### API仕様策定時
- [ ] エンドポイントのパス設計が RESTful
- [ ] 適切な HTTP メソッドの選択
- [ ] リクエスト・レスポンススキーマの定義
- [ ] エラーレスポンスの統一
- [ ] 認証・認可方式の明確化
- [ ] バリデーションルールの設定

### 実装時
- [ ] 生成されたスタブに実装を追加
- [ ] エラーハンドリングの実装
- [ ] テストケースの作成
- [ ] パフォーマンステスト
- [ ] セキュリティ検証

### リリース前
- [ ] API ドキュメント生成確認
- [ ] TypeScript 型定義の動作確認
- [ ] フロントエンド・バックエンドの結合テスト
- [ ] 本番環境での動作確認

このアプローチにより、API仕様を中心とした一貫性のある開発フローを実現できます。
