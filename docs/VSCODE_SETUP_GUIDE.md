# VS Code開発環境設定ガイド

このプロジェクトでは、VS Codeでの効率的な開発のために以下の設定を行っています。

## 🔧 自動フォーマット設定

### 保存時の自動実行機能
ファイル保存時（`Ctrl+S` / `Cmd+S`）に以下が自動実行されます：

1. **Ruffフォーマット**: コードの整形（インデント、行長、スペースなど）
2. **Import整理**: importの並び替えと不要なimportの削除
3. **Linting**: コード品質チェックとエラー検出

### 動作確認方法
1. 任意の`.py`ファイルを開く
2. 複数の空行を追加する（例：5行以上の連続空行）
3. `Ctrl+S`で保存
4. **期待結果**: 空行が適切な数（通常1-2行）に自動調整される

### トラブルシューティング

#### 自動フォーマットが動作しない場合
1. **Ruff拡張機能の確認**:
   - `Ctrl+Shift+X`で拡張機能を開く
   - "charliermarsh.ruff"がインストールされているか確認

2. **Python拡張機能の確認**:
   - "ms-python.python"がインストールされているか確認

3. **設定の確認**:
   - `Ctrl+,`で設定を開く
   - "format on save"で検索し、チェックが入っているか確認

4. **出力パネルの確認**:
   - `Ctrl+Shift+U`で出力パネルを開く
   - ドロップダウンで"Ruff"を選択してエラーメッセージを確認

## 🗂️ __pycache__ディレクトリの統合

### 問題の解決
従来はPythonファイルと同じディレクトリに`__pycache__`フォルダが散在していましたが、以下の設定により統合されます：

- **統合先**: `.cache/pycache/`ディレクトリ
- **設定方法**: `.env`ファイルの`PYTHONPYCACHEPREFIX`環境変数

### 確認方法
```bash
# Pythonファイルをインポート実行
python3 -c "import app"

# 統合されたキャッシュディレクトリの確認
ls -la .cache/pycache/
```

### メリット
- プロジェクトディレクトリがクリーンに保たれる
- `__pycache__`フォルダが散在しない
- `.gitignore`の設定が簡素化される

## 📝 推奨拡張機能

`.vscode/extensions.json`に定義された推奨拡張機能：

- **charliermarsh.ruff**: Python linting & formatting
- **ms-python.python**: Python開発サポート
- **redhat.vscode-yaml**: YAML編集サポート
- **esbenp.prettier-vscode**: JSON/Markdown formatting
- **bradlc.vscode-tailwindcss**: CSS utility classes
- **ms-vscode.vscode-typescript-next**: TypeScript最新サポート

VS Code初回起動時に自動的にインストールを提案されます。

## ⚡ パフォーマンス設定

### Ruffの高速処理
- **Black + isort + flake8を統合**: 3つのツールを1つで代替
- **Rust実装**: 10-100倍高速な処理
- **統合設定**: `pyproject.toml`で一元管理

### メモリ効率
- Python キャッシュの統合によりディスク使用量削減
- 不要なファイル監視の削減

---

## 🚀 開発開始方法

1. 環境変数ファイルの準備: `cp .env.example .env`
2. VS Codeでプロジェクトを開く
3. 推奨拡張機能をインストール（自動提案）
4. Python インタープリターを選択（`Ctrl+Shift+P` → "Python: Select Interpreter"）
5. ファイルを編集・保存して自動フォーマットを確認

これで効率的な開発環境が整います！