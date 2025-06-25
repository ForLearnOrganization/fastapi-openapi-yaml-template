# トラブルシューティングガイド

## 🔧 venv環境エラーの解決

### 問題: `poetry run python scripts/generate_all.py` でエラーが発生する

**症状:**
```
❌ エラーが発生しました: Command 'cd /path/to/project && python3 scripts/generate_backend.py' returned non-zero exit status 1.
```

**原因:**
- 異なるPython環境間での実行による不整合
- subprocess内で異なるpython3コマンドを使用している

**解決済み:**
- ✅ `sys.executable`を使用してPython実行環境を統一
- ✅ `traceback.print_exc()`でデバッグ情報を追加
- ✅ 全スクリプトでエラーハンドリングを強化

## 🚨 VS Code Flake8エラーの解決

### 問題: VS CodeでFlake8エラーが表示される

**症状:**
```
F403: 'from app.generated.generated_models import *' used; unable to detect undefined names
F405: 'HealthResponse' may be undefined, or defined from star imports
```

**解決済みの対応:**

#### 1. VS Code設定の更新 (`.vscode/settings.json`)
```json
{
  "python.linting.flake8Enabled": false,
  "flake8.enabled": false,
  "python.analysis.ignore": ["*.py"],
  "python.analysis.autoImportCompletions": false
}
```

#### 2. 生成コードの改善
- ❌ `from app.generated.generated_models import *` (星印インポート)
- ✅ 明示的インポート:
```python
from app.generated.generated_models import (
    HealthResponse,
    DetailedHealthResponse,
    GenerateTextRequest,
    # ... 他の必要なモデル
)
```

#### 3. Ruff無視設定の追加
```python
# ruff: noqa: F401
```

### VS Code拡張機能の確認

必要な拡張機能 (`.vscode/extensions.json`):
- `charliermarsh.ruff` - Ruffリンター
- `ms-python.python` - Python言語サポート

## 🐍 Python キャッシュ (__pycache__)

### 現在の設定
- ✅ キャッシュディレクトリを `.cache/pycache/` に統合
- ✅ `.gitignore` で適切に除外
- ✅ パフォーマンスは維持される

### 確認方法
```bash
# 環境変数が設定されているか確認
echo $PYTHONPYCACHEPREFIX

# キャッシュディレクトリの確認
ls -la .cache/pycache/
```

## 🔧 生成スクリプトの実行

### 正しい実行方法

```bash
# 統合生成（推奨）
poetry run python scripts/generate_all.py

# 個別実行
poetry run python scripts/generate_backend.py
poetry run python scripts/generate_frontend.py
```

### 生成後の自動フォーマット

生成されたコードは以下で自動フォーマットされます:
```bash
poetry run ruff format .
poetry run ruff check --fix .
```

## 📝 エラーログ分析

### traceback.print_exc() について

**メリット:**
- 詳細なエラー情報が得られる
- デバッグが容易になる
- 問題の根本原因を特定できる

**現在の実装:**
- ✅ 全生成スクリプトに組み込み済み
- ✅ 本番環境でも有用
- ✅ セキュリティ上問題なし

## 🎯 エラー分類と対応

### 1. 環境エラー (E902, PATH関連)
**対応:** `sys.executable`使用で解決済み

### 2. インポートエラー (F403, F405)
**対応:** 明示的インポートで解決済み

### 3. フォーマットエラー (E501, UP035)
**対応:** Ruff自動フォーマットで解決済み

### 4. ツールが見つからないエラー
**対応:** 
```bash
# poetryがない場合
pip install poetry

# ruffがない場合
poetry install  # dev dependenciesを含む
```

## 🔄 継続的な品質管理

### 推奨ワークフロー

1. **コード変更**
   ```bash
   # YAMLを編集
   vim source/openapi.yaml
   ```

2. **再生成**
   ```bash
   poetry run python scripts/generate_all.py
   ```

3. **品質チェック**
   ```bash
   poetry run ruff check .
   poetry run ruff format .
   ```

4. **動作確認**
   ```bash
   poetry run python main.py
   ```

## 📊 成功指標

- ✅ VS Codeでエラー0表示
- ✅ `poetry run ruff check .` でAll checks passed
- ✅ 生成スクリプトがエラーなく完了
- ✅ アプリケーションが正常起動

## 🆘 それでも問題が解決しない場合

1. VS Codeを再起動
2. Python拡張機能をリロード: `Ctrl+Shift+P` → "Python: Restart Language Server"
3. 仮想環境を再作成: `poetry env remove python && poetry install`
4. `.vscode/settings.json` の設定確認