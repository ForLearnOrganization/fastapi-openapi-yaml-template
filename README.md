# 🚀 localLLM-FastAPI

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![Poetry](https://img.shields.io/badge/dependency-poetry-blue.svg?style=flat&logo=poetry&logoColor=white)](https://python-poetry.org)

## 概要

FastAPI経由で、localLLMを動かします。本格的なプロダクション環境で使用可能なスケーラブルなFastAPIアプリケーションです。自動生成ドキュメント、型安全なAPIエンドポイント、Next.jsプロジェクト向けのクライアントサイド型生成機能を提供します。

## ✨ 機能

- 🏗️ **モジュラーアーキテクチャ**: ルーター、サービス、モデルのクリーンな分離
- 📖 **自動生成ドキュメント**: カスタムOpenAPIスキーマを使ったSwagger UIとReDoc
- 🔄 **型生成**: クライアントサイド開発用の自動TypeScript型生成
- 🌐 **外部API統合**: 天気、名言、豆知識、ジョークのモックエンドポイント
- 🧪 **テキスト生成**: ルールベースのテキスト生成サービス（実際のLLMに拡張可能）
- ❤️ **ヘルスチェック**: 包括的なヘルス監視エンドポイント
- 🔧 **YAML設定**: 設定駆動開発
- 🌍 **CORS対応**: Next.js開発用の事前設定

## 🚀 セットアップ

### 前提条件

- Python 3.9+
- Poetry（依存関係管理用）

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

3. **APIサーバの起動**
   ```bash
   poetry run uvicorn main:app --reload
   ```

4. **アプリケーションへのアクセス**
   - **APIドキュメント**: http://localhost:8000/docs
   - **代替ドキュメント**: http://localhost:8000/redoc
   - **ルートページ**: http://localhost:8000/
   - **ヘルスチェック**: http://localhost:8000/api/v1/health/

## 📁 プロジェクト構造

```
localllm-fastapi/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── health.py        # ヘルスチェックエンドポイント
│   │   │   ├── text.py          # テキスト生成エンドポイント
│   │   │   └── external.py      # 外部APIエンドポイント
│   │   └── __init__.py          # APIルーター設定
│   ├── core/
│   │   └── config.py            # アプリケーション設定
│   ├── models/
│   │   └── __init__.py          # Pydanticモデルとスキーマ
│   ├── services/
│   │   ├── text_service.py      # テキスト生成サービス
│   │   └── external_service.py  # 外部APIサービス
│   └── utils/
│       └── openapi.py           # OpenAPIユーティリティ
├── scripts/
│   ├── generate_client_types.py # 型生成用Pythonスクリプト
│   └── generate_types.sh        # 型生成用シェルスクリプト
├── generated/                   # 自動生成ファイル（初回実行時に作成）
│   ├── openapi.json
│   ├── openapi.yaml
│   └── api-types.ts
├── config.yaml                 # 設定ファイル
├── main.py                     # アプリケーションエントリーポイント
└── pyproject.toml              # Poetry設定
```

## 🔧 APIエンドポイント

### ヘルスエンドポイント
- `GET /api/v1/health/` - 基本的なヘルスチェック
- `GET /api/v1/health/detailed` - 詳細なヘルス情報

### テキスト生成
- `POST /api/v1/text/generate` - プロンプトからテキスト生成
- `POST /api/v1/text/echo` - メタデータ付きテキストエコー

### 外部API（モックデータ）
- `POST /api/v1/external/weather` - 天気情報取得
- `GET /api/v1/external/quote` - ランダムな名言取得
- `GET /api/v1/external/fact` - ランダムな豆知識取得
- `GET /api/v1/external/joke` - プログラミングジョーク取得

### 互換性エンドポイント
- `POST /generate` - 元の`/generate`エンドポイントとの後方互換性

## 🎯 使用例

### テキスト生成（新しいエンドポイント）
```bash
curl -X POST "http://localhost:8000/api/v1/text/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello world", "max_length": 100}'
```

### テキスト生成（元の互換エンドポイント）
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "百人一首っぽい言葉を並べて。"}'
```

### 天気API
```bash
curl -X POST "http://localhost:8000/api/v1/external/weather" \
     -H "Content-Type: application/json" \
     -d '{"city": "Tokyo", "country_code": "JP"}'
```

### ランダムな名言
```bash
curl -X GET "http://localhost:8000/api/v1/external/quote"
```

## 📦 クライアントサイド型生成

Next.jsプロジェクト用のTypeScript型を生成：

### シェルスクリプトを使用（推奨）
```bash
# すべての型とスキーマを生成
./scripts/generate_types.sh
```

### Pythonスクリプトを使用
```bash
poetry run python scripts/generate_client_types.py
```

### Next.js統合

1. **生成された型をコピー**
   ```bash
   cp generated/api-types.ts your-nextjs-project/types/api.ts
   ```

2. **HTTPクライアントをインストール**（例：axios）
   ```bash
   npm install axios
   ```

3. **Next.jsコンポーネントで使用**
   ```typescript
   import { WeatherRequest, WeatherResponse, API_ENDPOINTS } from './types/api';
   import axios from 'axios';

   const getWeather = async (request: WeatherRequest): Promise<WeatherResponse> => {
     const response = await axios.post<WeatherResponse>(
       `${process.env.NEXT_PUBLIC_API_URL}${API_ENDPOINTS.EXTERNAL_WEATHER}`,
       request
     );
     return response.data;
   };
   ```

4. **環境変数を設定**
   ```bash
   # .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## ⚙️ 設定

アプリケーションはYAMLベースの設定を使用します。`config.yaml`を編集してカスタマイズ：

```yaml
app:
  name: "localLLM-FastAPI"
  version: "1.0.0"
  debug: true

api:
  v1_prefix: "/api/v1"

cors:
  origins:
    - "http://localhost:3000"
    - "http://localhost:8000"

external_apis:
  weather:
    mock_mode: true
    api_key: "your-api-key"
```

## 🧪 開発

### テストの実行
```bash
poetry run pytest
```

### コードフォーマット
```bash
poetry run black .
poetry run isort .
```

### 型チェック
```bash
poetry run mypy .
```

### 新しいエンドポイントの追加

1. **エンドポイントファイルを作成** `app/api/v1/endpoints/`内に
2. **Pydanticモデルを定義** `app/models/__init__.py`内に
3. **ビジネスロジックを実装** `app/services/`内に
4. **ルーターを登録** `app/api/v1/__init__.py`内に

新しいエンドポイントの例：
```python
# app/api/v1/endpoints/new_feature.py
from fastapi import APIRouter
from app.models import NewFeatureRequest, NewFeatureResponse

router = APIRouter()

@router.post("/new-endpoint", response_model=NewFeatureResponse)
async def new_endpoint(request: NewFeatureRequest):
    """新機能のエンドポイント"""
    # 実装をここに
    pass
```

## 🌐 デプロイメント

### 本番環境セットアップ
```bash
# 本番用依存関係をインストール
poetry install --no-dev

# Gunicornで実行
poetry run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker（オプション）
```dockerfile
FROM python:3.9
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev
COPY . .
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## その他の便利なコマンド

- **依存関係の追加**
  新たなパッケージを追加する場合：
  ```bash
  poetry add <package_name>
  ```

- **依存関係の更新**
  すべての依存関係を更新：
  ```bash
  poetry update
  ```

- **仮想環境の確認**
  Poetry管理下の仮想環境情報を確認：
  ```bash
  poetry env info
  ```

- **Poetry シェルに入る**
  Poetry管理の仮想環境内で作業：
  ```bash
  poetry shell
  ```

## 🤝 コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. 変更を加える
4. 該当する場合はテストを追加
5. リンターとテストを実行
6. プルリクエストを送信

## 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。

## 🔗 リンク

- [FastAPI ドキュメント](https://fastapi.tiangolo.com/)
- [Pydantic ドキュメント](https://pydantic-docs.helpmanual.io/)
- [Poetry ドキュメント](https://python-poetry.org/docs/)

---

❤️ FastAPIとモダンなPython開発プラクティスで構築