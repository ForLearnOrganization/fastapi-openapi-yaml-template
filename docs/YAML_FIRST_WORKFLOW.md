# 🔄 YAML-First開発ワークフロー

このプロジェクトでは、OpenAPI YAML仕様を起点とした開発フローを採用しています。

## 📝 基本原則

1. **YAML仕様が真実の源泉**: `source/openapi.yaml`がすべてのAPI定義の起点
2. **コード自動生成**: PydanticモデルとFastAPIルーターはYAMLから自動生成
3. **実装のみ手動**: 生成されたスタブ関数の中身のみを編集

## 🔧 開発フロー

### 1. API仕様の定義

```yaml
# source/openapi.yaml
paths:
  /api/v1/users:
    post:
      tags: [users]
      summary: ユーザー作成
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'

components:
  schemas:
    CreateUserRequest:
      type: object
      required: [name, email]
      properties:
        name:
          type: string
          description: ユーザー名
        email:
          type: string
          format: email
          description: メールアドレス
```

### 2. コード生成

```bash
# バックエンド開発者向け
python3 scripts/generate_backend.py

# または統合生成
python3 scripts/generate_yaml_first.py
```

### 3. 実装の追加

生成されたファイル `app/generated/generated_router.py` の関数を実装：

```python
@users_router.post("/api/v1/users", summary="ユーザー作成")
async def create_user(request: CreateUserRequest) -> UserResponse:
    """新しいユーザーを作成"""
    # TODO: 実装が必要 ← この部分のみ編集
    
    # ビジネスロジックの実装
    user_id = generate_user_id()
    save_user_to_database(request.name, request.email)
    
    return UserResponse(
        id=user_id,
        name=request.name,
        email=request.email,
        created_at=datetime.now()
    )
```

## ⚠️ 重要な注意事項

### 編集してはいけないもの
- `app/generated/generated_models.py` - Pydanticモデル（YAML自動生成）
- `app/generated/generated_router.py` の関数定義部分（デコレーター、引数、戻り値型）

### 編集してもよいもの
- `app/generated/generated_router.py` の関数内部（`# TODO: 実装が必要` の部分）
- `source/openapi.yaml` - API仕様の定義

### 再生成について
- `source/openapi.yaml` を変更した場合は、必ず `python3 scripts/generate_backend.py` を実行
- 再生成時に手動実装部分は保持されません（TODOコメント付きに戻る）

## 🚀 実際の開発例

### 新しいエンドポイント追加

1. **YAML編集**
   ```yaml
   # source/openapi.yaml に追加
   /api/v1/posts/{post_id}:
     get:
       tags: [posts]
       summary: 投稿取得
       parameters:
         - name: post_id
           in: path
           required: true
           schema:
             type: integer
   ```

2. **コード生成**
   ```bash
   python3 scripts/generate_backend.py
   ```

3. **実装**
   ```python
   # app/generated/generated_router.py で自動生成された関数を実装
   async def get_post(post_id: int) -> PostResponse:
       post = get_post_from_database(post_id)
       if not post:
           raise HTTPException(status_code=404, detail="投稿が見つかりません")
       return PostResponse(**post)
   ```

## 👥 チーム開発での活用

### バックエンド担当者
1. `source/openapi.yaml` でAPI仕様を定義・更新
2. フロントエンド担当者と仕様確認・合意
3. `python3 scripts/generate_backend.py` でコード生成
4. 生成されたスタブの実装を追加

### フロントエンド担当者
1. バックエンド担当者との仕様合意後
2. `python3 scripts/generate_frontend.py` で型定義取得
3. 型安全なAPIクライアント実装

この方式により、API仕様の一貫性を保ちながら効率的なチーム開発が実現できます。