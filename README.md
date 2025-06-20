# 🚀 localLLM-FastAPI

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![Poetry](https://img.shields.io/badge/dependency-poetry-blue.svg?style=flat&logo=poetry&logoColor=white)](https://python-poetry.org)

## 概要

FastAPI経由で、localLLMを動かします。本格的なプロダクション環境で使用可能なスケーラブルなFastAPIアプリケーションです。自動生成ドキュメント、型安全なAPIエンドポイント、Next.jsプロジェクト向けのクライアントサイド型生成機能を提供します。

## ✨ 機能

- 🏗️ **YAML-Firstアーキテクチャ**: OpenAPI YAML仕様からコード自動生成
- 📖 **自動生成ドキュメント**: カスタムOpenAPIスキーマを使ったSwagger UIとReDoc
- 🔄 **型生成**: クライアントサイド開発用の自動TypeScript型生成
- 🌐 **外部API統合**: 天気、名言、豆知識、ジョークのモックエンドポイント
- 🧪 **テキスト生成**: ルールベースのテキスト生成サービス（実際のLLMに拡張可能）
- ❤️ **ヘルスチェック**: 包括的なヘルス監視エンドポイント
- 🔧 **YAML設定**: 設定駆動開発
- 🌍 **CORS対応**: Next.js開発用の事前設定
- ⚡ **コード自動生成**: YAML仕様からPydanticモデル・FastAPIルーター自動生成
- 📄 **HTMLドキュメント生成**: 静的なSwagger UIとReDocファイルの自動生成

## 🚀 簡単スタート

### 1. セットアップ

```bash
# リポジトリクローン
git clone https://github.com/ForLearnOrganization/localllm-fastapi.git
cd localllm-fastapi

# 依存関係インストール
poetry install

# 開発サーバー起動
poetry run uvicorn main:app --reload
```

### 2. アクセス

- **APIドキュメント**: http://localhost:8000/docs
- **代替ドキュメント**: http://localhost:8000/redoc
- **ルートページ**: http://localhost:8000/

## 👥 開発者向けコマンド

### バックエンド開発者

```bash
# YAML-First: バックエンド成果物の生成（Pydanticモデル、FastAPIルーター、ドキュメント）
python3 scripts/generate_backend.py

# YAML-First: 完全な統合生成（推奨）
python3 scripts/generate_yaml_first.py

# 新しいエンドポイント追加フロー:
# 1. source/openapi.yaml を編集
# 2. python3 scripts/generate_backend.py を実行
# 3. app/generated/generated_router.py の TODO部分を実装
```

### フロントエンド開発者

```bash
# TypeScript型定義とAPIクライアントの生成
python3 scripts/generate_frontend.py

# Next.jsプロジェクトで型安全なAPI呼び出しが可能
```

### プロジェクト全体

```bash
# すべてを一括生成（バックエンド + フロントエンド）
python3 scripts/generate_all.py

# 完全なYAML-firstワークフロー
python3 scripts/generate_yaml_first.py
```

### インストール

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/ForLearnOrganization/localllm-fastapi.git
   cd localllm-fastapi
   ```

2. **Poetry の依存パッケージをインストール**
   ```bash
   poetry install
   ```

3. **開発環境の設定**
   ```bash
   poetry shell  # 仮想環境をアクティベート
   ```

4. **APIサーバの起動**
   ```bash
   poetry run uvicorn main:app --reload
   ```

5. **アプリケーションへのアクセス**
   - **APIドキュメント**: http://localhost:8000/docs
   - **代替ドキュメント**: http://localhost:8000/redoc
   - **ルートページ**: http://localhost:8000/

## 📁 プロジェクト構造

```
localllm-fastapi/
├── .vscode/                    # VSCode設定
│   ├── settings.json          # エディタ設定（Ruff自動フォーマット）
│   └── extensions.json        # 推奨拡張機能
├── app/                       # アプリケーションソース
│   ├── generated/             # 🤖 YAML自動生成: Pydanticモデル・FastAPIルーター
│   ├── core/                  # 設定とコア機能
│   ├── models/               # Pydanticスキーマ（手動定義用）
│   ├── services/             # ビジネスロジック
│   └── utils/                # ユーティリティ関数
├── scripts/                   # 型生成・ドキュメント生成スクリプト
│   ├── generate_backend.py    # バックエンド開発者向け生成
│   ├── generate_frontend.py   # フロントエンド開発者向け生成
│   ├── generate_yaml_first.py # YAML-first統合生成
│   ├── generate_from_yaml.py  # YAMLからPython生成
│   └── generate_docs.py       # 📄 HTML ドキュメント生成
├── docs/                      # 📁 ドキュメント管理
│   ├── generated/            # 🤖 自動生成: OpenAPIスキーマ
│   └── static/               # 🤖 自動生成: 静的HTMLドキュメント
├── generated/                 # 🤖 自動生成: TypeScript型定義
├── source/                    # 📁 手動管理: ソース用YAML等
│   └── openapi.yaml          # 🔧 API仕様定義（編集対象）
├── config.yaml               # アプリケーション設定
└── main.py                   # アプリケーションエントリーポイント
```

## 🔄 YAML-First開発運用フロー

### バックエンド開発者の作業フロー

1. **OpenAPI YAML仕様の編集**
   ```yaml
   # source/openapi.yaml でAPI仕様を定義
   paths:
     /api/v1/new-feature/create:
       post:
         tags: [features]
         summary: 新機能作成
         requestBody:
           content:
             application/json:
               schema:
                 $ref: '#/components/schemas/NewFeatureRequest'
         responses:
           '200':
             content:
               application/json:
                 schema:
                   $ref: '#/components/schemas/NewFeatureResponse'
   
   components:
     schemas:
       NewFeatureRequest:
         type: object
         properties:
           name:
             type: string
             description: 機能名
           description:
             type: string
             description: 機能説明
   ```

2. **コードとモデルの自動生成**
   ```bash
   # Pydanticモデル・FastAPIルーターを自動生成
   python3 scripts/generate_backend.py
   ```

3. **生成されたスタブの実装**
   ```python
   # app/generated/generated_router.py に生成された関数を実装
   async def create_new_feature(request: NewFeatureRequest) -> NewFeatureResponse:
       # TODO: 実装が必要 ← この部分のみ編集
       # ビジネスロジックの実装
       return NewFeatureResponse(id=1, name=request.name, status="created")
   ```

### フロントエンド開発者の作業フロー

1. **型定義の取得**
   ```bash
   # TypeScript型定義とAPIクライアントを生成
   python3 scripts/generate_frontend.py
   ```

2. **Next.jsでの型安全なAPI呼び出し**
   ```typescript
   // generated/api-types.ts からインポート
   import { GenerateTextRequest, apiMethods } from './generated/api-types';
   
   const MyComponent = () => {
     const handleGenerateText = async () => {
       try {
         const response = await apiMethods.generateText({
           prompt: 'Hello world',
           max_length: 100
         });
         console.log(response.generated_text);
       } catch (error) {
         console.error('API呼び出しエラー:', error);
       }
     };
   
     return <button onClick={handleGenerateText}>テキスト生成</button>;
   };
   ```

3. **fetchベースAPIクライアントの使用**
   ```typescript
   import { createApiClient, API_ENDPOINTS } from './generated/api-types';
   
   const apiClient = createApiClient(process.env.NEXT_PUBLIC_API_URL);
   
   // 型安全なAPI呼び出し
   const healthData = await apiClient.get(API_ENDPOINTS.HEALTH_CHECK);
   ```

### チーム開発での役割分担

| 担当者 | 実行コマンド | 生成物 | 目的 |
|--------|-------------|--------|------|
| バックエンド | `python3 scripts/generate_backend.py` | APIルーター、HTMLドキュメント | API開発・ドキュメント化 |
| フロントエンド | `python3 scripts/generate_frontend.py` | TypeScript型定義、APIクライアント | 型安全なフロントエンド開発 |
| プロジェクトリーダー | `python3 scripts/generate_all.py` | 全成果物 | 全体統合・リリース準備 |

## 📖 ドキュメント管理

### HTMLドキュメントの種類と利用方法

#### 📖 ReDoc (`docs/static/redoc.html`)
- **用途**: エンドユーザー向けの読みやすいAPIドキュメント
- **特徴**: 美しいデザイン、詳細説明、モバイルフレンドリー
- **推奨用途**: 外部パートナーやクライアントへの提供

#### 🔧 Swagger UI (`docs/static/swagger.html`)
- **用途**: 開発者向けの対話式APIテスト環境
- **特徴**: Try it out機能、リクエスト/レスポンス確認
- **推奨用途**: 内部開発チーム、API開発・テスト

### ホスティングとアクセス制御

```
- ReDoc: 限定公開（パートナー・クライアント用）
- Swagger UI: 内部限定（開発者専用）
```

**セキュリティ考慮事項**:
- Swagger UIは実際にAPIを呼び出せるため、本番環境への接続は避ける
- ReDocは静的ドキュメントなので比較的安全だが、API仕様が外部に見える
- 可能であれば社内IPからのみアクセス可能にする

詳細な情報は [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md) を参照してください。

## 🛠️ 開発環境セットアップ

### コードフォーマット設定（Ruff）

#### 自動フォーマット確認方法
1. VS Codeで任意の`.py`ファイルを開く
2. コードを意図的に崩す（スペース削除、長い行作成など）
3. `Ctrl+S` (Windows/Linux) または `Cmd+S` (Mac) で保存
4. 自動的にRuffがフォーマットすることを確認

#### __pycache__ディレクトリ問題の解決
- `.gitignore`で`__pycache__/`を除外済み
- `*.py[cod]`、`*$py.class`も除外設定済み
- VS Code設定でFlake8を無効化してRuffのみ使用

#### 詳細設定ガイド
- [docs/RUFF_SETUP_GUIDE.md](docs/RUFF_SETUP_GUIDE.md) - Ruff設定の詳細説明
- 保存時自動フォーマットの設定方法
- Flake8エラー解消方法

## 📁 プロジェクト構造

```
localllm-fastapi/
├── .vscode/                    # VSCode設定
│   ├── settings.json          # エディタ設定（Ruff自動フォーマット）
│   └── extensions.json        # 推奨拡張機能
├── app/                       # アプリケーションソース
│   ├── api/v1/endpoints/      # APIルートハンドラー
│   ├── api/endpoint_registry.py # エンドポイント設定レジストリ
│   ├── core/                  # 設定とコア機能
│   ├── models/               # Pydanticスキーマ
│   ├── services/             # ビジネスロジック
│   └── utils/                # ユーティリティ関数
├── scripts/                   # 🔧 Python生成スクリプト
│   ├── generate_all.py        # 全体統合生成
│   ├── generate_backend.py    # バックエンド専用生成
│   ├── generate_frontend.py   # フロントエンド専用生成
│   ├── generate_client_types.py # TypeScript型生成
│   └── generate_docs.py       # HTMLドキュメント生成
├── docs/                      # 📁 ドキュメント管理
│   ├── generated/            # 🤖 自動生成: OpenAPIスキーマ
│   └── static/               # 🤖 自動生成: 静的HTMLドキュメント
├── generated/                 # 🤖 自動生成: TypeScript型定義
├── source/                    # 📁 手動管理: ソース用YAML等（将来用）
├── config.yaml               # アプリケーション設定
└── main.py                   # アプリケーションエントリーポイント
```

## 🔧 APIエンドポイント

### ヘルスチェック
- `GET /api/v1/health/` - 基本ヘルスチェック
- `GET /api/v1/health/detailed` - 詳細システム情報

### テキスト生成
- `POST /api/v1/text/generate` - ルールベーステキスト生成
- `POST /api/v1/text/echo` - テキスト解析・メタデータ生成
- `POST /generate` - 後方互換性エンドポイント

### 外部サービス（モックデータ）
- `POST /api/v1/external/weather` - 天気情報
- `GET /api/v1/external/quote` - ランダム名言
- `GET /api/v1/external/fact` - 豆知識
- `GET /api/v1/external/joke` - プログラミングジョーク

## 🧪 使用例

### curlでのAPIテスト

```bash
# ヘルスチェック
curl http://localhost:8000/api/v1/health/

# テキスト生成
curl -X POST "http://localhost:8000/api/v1/text/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello world", "max_length": 100}'

# 天気情報取得
curl -X POST "http://localhost:8000/api/v1/external/weather" \
     -H "Content-Type: application/json" \
     -d '{"location": "Tokyo"}'
```

### Next.jsでの型安全なAPI呼び出し

```typescript
import { GenerateTextRequest, apiMethods } from './generated/api-types';

const MyComponent = () => {
  const handleGenerateText = async () => {
    try {
      const response = await apiMethods.generateText({
        prompt: 'Hello world',
        max_length: 100
      });
      console.log(response.generated_text);
    } catch (error) {
      console.error('API呼び出しエラー:', error);
    }
  };

  return <button onClick={handleGenerateText}>テキスト生成</button>;
};
```

## 🔧 開発ツール設定

### VSCode自動フォーマット設定

プロジェクトには`.vscode/settings.json`が含まれており、以下の機能が自動で有効になります：

- **Ruffによる自動フォーマット**: ファイル保存時にコード整形
- **インポート自動整理**: isort互換の自動インポート整理
- **構文エラー検出**: リアルタイムでのコード検証

### Ruff vs Black + isort の選択理由

**🚀 Ruffを選択した理由:**

1. **パフォーマンス**: Rustで書かれており、Black+isortより10-100倍高速
2. **統合性**: linting（flake8相当）とformatting（black相当）を1つのツールで提供
3. **設定簡素化**: pyproject.toml内の単一設定で完了
4. **互換性**: BlackやisortとほぼUI・フォーマット結果
5. **メンテナンス**: アクティブな開発と定期的な更新

**従来のBlack + isortからの移行メリット:**
- 設定ファイルの簡素化（pyproject.tomlの[tool.ruff]セクションのみ）
- ビルド・CI時間の短縮
- VSCodeでの応答性向上
- 依存関係の削減

## その他の便利なコマンド

### 開発サーバー
```bash
# 通常起動
python3 main.py

# Poetry環境での起動
poetry run uvicorn main:app --reload

# ホットリロード付き開発サーバー
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### コード品質チェック
```bash
# Ruffによるコード検証とフォーマット
poetry run ruff check .
poetry run ruff format .

# 型チェック（mypyが設定されている場合）
poetry run mypy app/
```

### テスト実行
```bash
# 全テスト実行
poetry run pytest

# カバレッジ付きテスト
poetry run pytest --cov=app tests/
```

## 🚀 本番デプロイメント

### Docker対応（予定）
```bash
# Dockerイメージビルド（将来実装予定）
docker build -t localllm-fastapi .

# コンテナ起動
docker run -p 8000:8000 localllm-fastapi
```

### 環境変数
```bash
# .env ファイル例
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false
CORS_ORIGINS=["https://yourfrontend.com"]
```

---

**開発者向けドキュメント完了** ✨

より詳細な情報については、生成されたAPIドキュメント（http://localhost:8000/docs）をご参照ください。

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

