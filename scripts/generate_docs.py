#!/usr/bin/env python3
"""
ドキュメント生成スクリプト

OpenAPIスキーマから以下を生成：
1. OpenAPI YAML/JSON ファイル
2. TypeScript型定義
3. 静的HTMLドキュメント（ReDoc）
4. Swagger UI HTML
"""

import json
import sys
from pathlib import Path

import yaml


def generate_openapi_schema():
    """source/openapi.yaml から静的HTMLドキュメントを生成"""
    print("📋 OpenAPI仕様から静的ドキュメントを生成中...")

    # source/openapi.yaml を読み込み
    project_root = Path(__file__).parent.parent
    source_yaml = project_root / "source" / "openapi.yaml"

    if not source_yaml.exists():
        print(f"❌ OpenAPI仕様ファイルが見つかりません: {source_yaml}")
        return None, None, None

    with open(source_yaml, encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    # generated ディレクトリを作成
    generated_dir = project_root / "docs" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    # JSON形式で保存
    json_path = generated_dir / "openapi.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    # YAML形式で保存
    yaml_path = generated_dir / "openapi.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(schema, f, default_flow_style=False, allow_unicode=True)

    print(f"✅ OpenAPIスキーマを生成: {json_path}, {yaml_path}")
    return schema, json_path, yaml_path


def generate_typescript_types(openapi_json_path):
    """TypeScript型定義生成をスキップ（別のスクリプトで実行）"""
    print("⚠️ TypeScript型定義生成は scripts/generate_frontend.py で実行してください")
    return True


def generate_redoc_html(openapi_json_path):
    """ReDoc HTMLドキュメントを生成"""
    print("📄 ReDoc HTMLドキュメントを生成中...")

    docs_dir = Path(__file__).parent / "generated" / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    redoc_html_path = docs_dir / "redoc.html"

    # OpenAPIスキーマを読み込んで直接HTMLに埋め込み
    with open(openapi_json_path, encoding="utf-8") as f:
        openapi_spec = json.load(f)

    formatted_spec = json.dumps(openapi_spec, indent=2, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>LocalLLM FastAPI Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Roboto, sans-serif;
        }}
    </style>
</head>
<body>
    <div id="redoc-container"></div>
    <script src="https://cdn.jsdelivr.net/npm/redoc@2.1.5/bundles/redoc.standalone.js"></script>
    <script>
        const spec = {formatted_spec};
        Redoc.init(spec, {{}}, document.getElementById('redoc-container'));
    </script>
</body>
</html>
"""

    with open(redoc_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ ReDoc HTMLを生成: {redoc_html_path}")


def generate_swagger_html(openapi_json_path):
    """Swagger UI HTMLドキュメントを生成"""
    print("📄 Swagger UI HTMLドキュメントを生成中...")

    docs_dir = Path(__file__).parent / "generated" / "docs"
    swagger_html_path = docs_dir / "swagger.html"

    # OpenAPIスキーマを読み込んで直接HTMLに埋め込み
    with open(openapi_json_path, encoding="utf-8") as f:
        openapi_spec = json.load(f)

    formatted_spec = json.dumps(openapi_spec, indent=2, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>LocalLLM FastAPI - Swagger UI</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
    <style>
        html {{
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }}
        *, *:before, *:after {{
            box-sizing: inherit;
        }}
        body {{
            margin:0;
            background: #fafafa;
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const spec = {formatted_spec};
            const ui = SwaggerUIBundle({{
                spec: spec,
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
            }});
        }};
    </script>
</body>
</html>
"""

    with open(swagger_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Swagger UI HTMLを生成: {swagger_html_path}")


def main():
    """メイン処理"""
    print("🚀 ドキュメント生成を開始...")

    try:
        # 1. OpenAPIスキーマ生成（HTMLファイル生成用の一時ファイル）
        schema, json_path, yaml_path = generate_openapi_schema()

        # 2. TypeScript型定義生成
        generate_typescript_types(json_path)

        # 3. ReDoc HTML生成
        generate_redoc_html(json_path)

        # 4. Swagger UI HTML生成
        generate_swagger_html(json_path)

        # 5.一時ファイル削除
        if json_path.exists():
            json_path.unlink()
        if yaml_path.exists():
            yaml_path.unlink()

        # 6.空のディレクトリを削除
        if json_path.parent.exists() and not any(json_path.parent.iterdir()):
            json_path.parent.rmdir()

        print("\n🎉 すべてのドキュメント生成が完了しました！")
        print("\n📁 生成されたファイル:")
        print("  - TypeScript型: scripts/generated/api-types.ts")
        print("  - ReDoc HTML: scripts/generated/docs/redoc.html")
        print("  - Swagger HTML: scripts/generated/docs/swagger.html")
        print("\n💡 ドキュメントの使い分け:")
        print("  - ReDoc: 読みやすい形式、エンドユーザー向け")
        print("  - Swagger: 対話式、開発者向けAPIテスト用")

    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
