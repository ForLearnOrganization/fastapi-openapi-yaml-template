# Ruff 設定と使用方法

## 概要
このプロジェクトでは、PythonコードのリンティングとフォーマットにRuffを使用しています。RuffはRust製の高速なPythonリンター・フォーマッターで、Black + isort + Flake8の機能を統合したツールです。

## VS Code設定

### 必要な拡張機能
- `charliermarsh.ruff` - Ruff拡張機能

### 自動フォーマット設定
`.vscode/settings.json`に以下の設定が含まれています：

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    }
  },
  "python.linting.enabled": false,
  "python.linting.flake8Enabled": false,
  "ruff.enable": true,
  "ruff.lint.enable": true,
  "ruff.format.enable": true
}
```

## Ruffフォーマットの確認方法

### 1. VS Codeでの確認
1. 任意の`.py`ファイルを開く
2. 意図的にフォーマットを崩す（スペースを削除、長い行を作成など）
3. `Ctrl+S` (Windows/Linux) または `Cmd+S` (Mac) で保存
4. 自動的にフォーマットされることを確認

### 2. テストファイルでの確認
以下のような悪いフォーマットのコードを作成してテスト：

```python
# フォーマット前（悪い例）
def bad_function(param1,param2,param3):
    if param1>param2:
        result=[x*2 for x in range(10) if x%2==0]
        return {"result":result,"status":"success"}

# 保存後、Ruffが自動的に以下のようにフォーマット
def bad_function(param1, param2, param3):
    if param1 > param2:
        result = [x * 2 for x in range(10) if x % 2 == 0]
        return {"result": result, "status": "success"}
```

### 3. コマンドラインでの確認
プロジェクトルートで以下のコマンドを実行：

```bash
# フォーマット確認（変更は行わない）
python3 -m ruff format --check .

# フォーマット実行
python3 -m ruff format .

# リンティング確認
python3 -m ruff check .
```

## Flake8の無効化
VS Code設定で以下が無効化されています：
- `python.linting.flake8Enabled: false`
- `python.linting.enabled: false`

これにより、Flake8のエラーが表示されず、Ruffのみが使用されます。

## トラブルシューティング

### Ruffが動作しない場合
1. VS CodeでRuff拡張機能がインストールされているか確認
2. VS Codeを再起動
3. プロジェクトのワークスペース設定が正しいか確認
4. Python拡張機能との競合がないか確認

### まだFlake8エラーが表示される場合
1. VS Codeの設定画面で「flake8」を検索
2. すべてのFlake8関連設定を無効化
3. VS Codeを再起動

## Ruff設定詳細
`pyproject.toml`でRuffの設定を管理：

```toml
[tool.ruff]
target-version = "py39"
line-length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["B904"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

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
