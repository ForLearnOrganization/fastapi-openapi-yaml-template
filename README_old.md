
# localLLM-FastAPI

## 概要
FastAPI経由で、localLLMを動かします。

## セットアップ

1. **Poetry の依存パッケージをインストール**

   プロジェクトディレクトリで以下のコマンドを実行して、必要なパッケージをインストールします。

   ```bash
   poetry install
   ```

2. **APIサーバの起動**

  - Poetry 経由で起動（推奨）:
    ```bash
    poetry run uvicorn main:app --reload
    ```
    
  - グローバル環境または手元の仮想環境内部で起動:
    ```bash
    uvicorn main:app --reload
    ```
   ※ (FastAPI サーバをデバッグモード（`--reload` オプション付き）で起動することで、コード変更時に自動リロードされ、開発がスムーズになります。)
 ## 使うコマンド
- **GETリクエストの送信**

  API サーバのルートエンドポイントに GET リクエストを送ります。
  ```bash
  curl -X GET "http://127.0.0.1:8000/"
  ```

- **POSTリクエストの送信**

  テキスト生成エンドポイントに POST リクエストを送ります。  
  （例として、百人一首っぽい言葉を生成）
  ```bash
  curl -X POST "http://127.0.0.1:8000/generate" \
       -H "Content-Type: application/json" \
       -d "{\"prompt\": \"百人一首っぽい言葉を並べて。\"}"
  ```

## その他の便利なコマンド

- **依存関係の更新**

  新たなパッケージを追加した場合や、既存のパッケージを更新する場合は、以下のコマンドを利用します。
  
  ```bash
  poetry add <package_name>
  ```
  
  もしくは、すべての依存関係を更新するには
  
  ```bash
  poetry update
  ```

- **仮想環境の確認**

  現在の Poetry 管理下の仮想環境情報を確認するには、次のコマンドを使います。
  
  ```bash
  poetry env info
  ```

- **Poetry シェルに入る（オプション）**

   Poetry 管理の仮想環境内で作業したい場合は、次のコマンドでシェルに入ります。

   ```bash
   poetry shell
   ```
