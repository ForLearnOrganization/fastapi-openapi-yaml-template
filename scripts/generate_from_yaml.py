#!/usr/bin/env python3
"""
OpenAPI YAML ファーストアプローチ用のコード生成スクリプト

手書きのopenapi.yamlからPydanticモデルとFastAPIエンドポイントを生成します。
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


def load_openapi_spec(yaml_path: str) -> dict[str, Any]:
    """OpenAPI YAML仕様をロードします。"""
    with open(yaml_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def format_generated_files(output_dir: Path) -> None:
    """生成されたPythonファイルをruffでフォーマットします。"""
    try:
        python_files = list(output_dir.glob("*.py"))
        if not python_files:
            return

        print("🎨 生成されたファイルをフォーマット中...")

        # PYTHONPYCACHEPREFIX環境変数を設定
        import os

        env = os.environ.copy()
        env["PYTHONPYCACHEPREFIX"] = ".cache/pycache"

        # まずpoetry run ruffを試す
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "poetry",
                    "run",
                    "ruff",
                    "format",
                    *[str(f) for f in python_files],
                ],
                check=True,
                cwd=output_dir.parent.parent,
                capture_output=True,
                env=env,
            )

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "poetry",
                    "run",
                    "ruff",
                    "check",
                    "--fix",
                    *[str(f) for f in python_files],
                ],
                check=False,
                cwd=output_dir.parent.parent,
                capture_output=True,
                env=env,
            )

            print("✨ フォーマット完了（poetry経由）")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # 次に直接ruffを試す
        try:
            subprocess.run(
                ["ruff", "format", *[str(f) for f in python_files]],
                check=True,
                cwd=output_dir.parent.parent,
                capture_output=True,
                env=env,
            )

            subprocess.run(
                ["ruff", "check", "--fix", *[str(f) for f in python_files]],
                check=False,
                cwd=output_dir.parent.parent,
                capture_output=True,
                env=env,
            )

            print("✨ フォーマット完了（直接実行）")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # 最後にpip install ruffでインストールして試す
        print("⚠️  ruffが見つかりません。基本的なフォーマットを適用します...")

    except Exception as e:
        print(f"⚠️  フォーマットに失敗しましたが、生成は完了しています: {e}")


def generate_pydantic_models(spec: dict[str, Any], output_dir: str) -> None:
    """Pydanticモデルを生成します。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    models_file = output_path / "generated_models.py"

    content = """\"\"\"
OpenAPI YAML仕様から自動生成されたPydanticモデル
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
\"\"\"

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


"""

    # コンポーネント/スキーマからモデルを生成
    schemas = spec.get("components", {}).get("schemas", {})

    for schema_name, schema_def in schemas.items():
        if schema_def.get("type") == "object":
            model_code = generate_model_class(schema_name, schema_def)
            content += model_code + "\n\n"

    with open(models_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Pydanticモデルを生成しました: {models_file}")


def generate_model_class(name: str, schema: dict[str, Any]) -> str:
    """単一のPydanticモデルクラスを生成します。"""
    description = schema.get("description", "")
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    # クラス定義開始
    class_def = f"class {name}(BaseModel):"
    if description:
        class_def += f'\n    """{description}"""'

    class_def += "\n"

    # プロパティを生成
    for prop_name, prop_def in properties.items():
        is_required = prop_name in required
        field_type = convert_openapi_type_to_python(prop_def)
        field_description = prop_def.get("description", "")

        # デフォルト値の処理
        default_value = prop_def.get("default")
        field_def = ""

        if not is_required:
            if default_value is not None:
                if isinstance(default_value, str):
                    field_def = f' = "{default_value}"'
                else:
                    field_def = f" = {default_value}"
            else:
                field_type = f"Optional[{field_type}]"
                field_def = " = None"

        # Field()を使用した詳細定義
        field_params = []
        if field_description:
            field_params.append(f'description="{field_description}"')

        # 数値制約
        if "minimum" in prop_def:
            field_params.append(f'ge={prop_def["minimum"]}')
        if "maximum" in prop_def:
            field_params.append(f'le={prop_def["maximum"]}')

        # 文字列制約
        if "minLength" in prop_def:
            field_params.append(f'min_length={prop_def["minLength"]}')
        if "maxLength" in prop_def:
            field_params.append(f'max_length={prop_def["maxLength"]}')

        if field_params:
            # 長い行を避けるため、パラメータが多い場合は複数行に分割
            params_str = ", ".join(field_params)
            if len(f"    {prop_name}: {field_type} = Field({params_str})") > 80:
                # バックスラッシュを含む文字列を変数に分離
                multiline_params = ",\n        ".join(field_params)
                field_def = f" = Field(\n        {multiline_params}\n    )"
            else:
                field_def = f" = Field({params_str})"

        class_def += f"    {prop_name}: {field_type}{field_def}\n"

    return class_def


def convert_openapi_type_to_python(prop_def: dict[str, Any]) -> str:
    """OpenAPIプロパティ定義をPython型に変換します。"""
    prop_type = prop_def.get("type", "any")
    prop_format = prop_def.get("format")

    if prop_type == "string":
        if prop_format == "date-time":
            return "datetime"
        return "str"
    elif prop_type == "integer":
        return "int"
    elif prop_type == "number":
        return "float"
    elif prop_type == "boolean":
        return "bool"
    elif prop_type == "array":
        item_type = convert_openapi_type_to_python(prop_def.get("items", {}))
        return f"list[{item_type}]"
    elif prop_type == "object":
        return "dict[str, Any]"
    else:
        # $refの処理
        ref = prop_def.get("$ref")
        if ref:
            return ref.split("/")[-1]
        return "Any"


def generate_router_stubs(spec: dict[str, Any], output_dir: str) -> None:
    """FastAPIルータースタブを生成します。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    router_file = output_path / "generated_router.py"

    # モデルをインポートするための名前を収集
    schemas = spec.get("components", {}).get("schemas", {})
    model_imports = []
    for schema_name in schemas.keys():
        model_imports.append(schema_name)

    imports_str = ""
    if model_imports:
        # 長い行を避けるため、インポートを複数行に分割
        if len(", ".join(model_imports)) > 60:
            imports_str = "(\n    " + ",\n    ".join(model_imports) + ",\n)"
        else:
            imports_str = ", ".join(model_imports)

    content = f'''"""
OpenAPI YAML仕様から自動生成されたFastAPIルーター
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException

# ruff: noqa: F401
from app.generated.generated_models import {imports_str}
from app.services.text_service import TextService
from app.services.external_service import ExternalAPIService

# サービスインスタンス
text_service = TextService()
external_service = ExternalAPIService()

# タグ別にルーターを分割（prefixは相対パスのみ、main.pyで/api/v1が追加される）
health_router = APIRouter(prefix="/health", tags=["health"])
text_router = APIRouter(prefix="/text", tags=["text"])
external_router = APIRouter(prefix="/external", tags=["external"])
legacy_router = APIRouter(tags=["text"])


'''

    # パスからエンドポイントを生成
    paths = spec.get("paths", {})

    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.lower() in ["get", "post", "put", "delete", "patch"]:
                endpoint_code = generate_endpoint_implementation(
                    path, method, operation
                )
                content += endpoint_code + "\n\n"

    # 主ルーターに登録
    content += """
# メインルーターを作成
main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(text_router)
main_router.include_router(external_router)

# Legacy router should be separate (not include in main_router)
# so it can be mounted without /api/v1 prefix
"""

    with open(router_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ FastAPIルータースタブを生成しました: {router_file}")


def generate_endpoint_implementation(
    path: str, method: str, operation: dict[str, Any]
) -> str:
    """単一のエンドポイント実装を生成します。"""
    operation_id = operation.get(
        "operationId",
        f'{method}_{path.replace("/", "_").replace("{", "").replace("}", "")}',
    )
    summary = operation.get("summary", "")
    description = operation.get("description", "")
    tags = operation.get("tags", [])

    # ルーター選択と相対パス計算
    router_name = "main_router"
    relative_path = path

    if tags:
        tag = tags[0]
        if tag == "health":
            router_name = "health_router"
            # /api/v1/health/ -> /
            # /api/v1/health/detailed -> /detailed
            relative_path = path.replace("/api/v1/health", "") or "/"
        elif tag == "text":
            if path.startswith("/generate"):
                router_name = "legacy_router"
                relative_path = path  # /generate stays as is
            else:
                router_name = "text_router"
                # /api/v1/text/generate -> /generate
                # /api/v1/text/echo -> /echo
                relative_path = path.replace("/api/v1/text", "") or "/"
        elif tag == "external":
            router_name = "external_router"
            # /api/v1/external/weather -> /weather
            # /api/v1/external/quote -> /quote
            relative_path = path.replace("/api/v1/external", "") or "/"

    # リクエストボディの処理
    request_body = operation.get("requestBody")
    request_param = ""
    if request_body:
        content = request_body.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})
        ref = schema.get("$ref")
        if ref:
            model_name = ref.split("/")[-1]
            request_param = f"request: {model_name}"

    # レスポンスの処理
    responses = operation.get("responses", {})
    success_response = responses.get("200", {})
    content = success_response.get("content", {})
    json_content = content.get("application/json", {})
    schema = json_content.get("schema", {})
    ref = schema.get("$ref")
    response_type = "dict"
    if ref:
        response_type = ref.split("/")[-1]

    # パスパラメータの処理
    path_params = re.findall(r"\\{([^}]+)\\}", path)
    path_param_str = ""
    if path_params:
        path_param_str = ", " + ", ".join([f"{param}: str" for param in path_params])

    # 関数生成
    decorator = f'@{router_name}.{method.lower()}("{relative_path}"'
    if summary:
        decorator += f', summary="{summary}"'
    decorator += ")"

    function_def = f"async def {operation_id}("
    if request_param:
        function_def += request_param
    if path_param_str:
        function_def += path_param_str
    function_def += f") -> {response_type}:"

    docstring = ""
    if description:
        docstring = f'    """{description}"""'

    # 実装本体を生成
    body = generate_endpoint_body(operation_id, path, request_param, response_type)

    return f"{decorator}\n{function_def}\n{docstring}\n{body}"


def generate_endpoint_body(
    operation_id: str, path: str, request_param: str, response_type: str
) -> str:
    """エンドポイントの実装本体を生成します。"""

    # Health check endpoints
    if operation_id == "health_check":
        return """    from datetime import datetime
    return HealthResponse(status="healthy", timestamp=datetime.now())"""

    elif operation_id == "detailed_health_check":
        return """    from datetime import datetime
    import platform
    import sys
    import time

    start_time = getattr(detailed_health_check, 'start_time', time.time())
    if not hasattr(detailed_health_check, 'start_time'):
        detailed_health_check.start_time = start_time

    return DetailedHealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        system_info={
            "python_version": sys.version,
            "platform": platform.platform(),
            "memory_usage": "not_available",  # MB (psutil not installed)
            "uptime": time.time() - start_time
        },
        services={
            "database": "not_configured",
            "cache": "not_configured",
            "external_apis": "mock_mode"
        }
    )"""

    # Text generation endpoints
    elif operation_id == "generate_text":
        return """    try:
        result = await text_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length or 100,
            temperature=request.temperature or 0.7,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"テキスト生成に失敗しました: {str(e)}"
        )"""

    elif operation_id == "generate_text_legacy":
        return """    try:
        result = await text_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length or 100,
            temperature=request.temperature or 0.7,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"テキスト生成に失敗しました: {str(e)}"
        )"""

    elif operation_id == "echo_text":
        return """    from datetime import datetime
    import re

    # Simple text analysis
    text = request.text
    character_count = len(text)
    word_count = len(text.split())

    # Simple language detection (very basic)
    if re.search(r'[ひらがなカタカナ漢字]', text):
        language = "ja"
    elif re.search(r'[a-zA-Z]', text):
        language = "en"
    else:
        language = "unknown"

    # Simple sentiment analysis (keyword based)
    positive_words = ['good', 'great', 'excellent', '良い', '素晴らしい', '最高']
    negative_words = ['bad', 'terrible', 'awful', '悪い', '最悪', 'ひどい']

    sentiment = "neutral"
    for word in positive_words:
        if word in text.lower():
            sentiment = "positive"
            break
    for word in negative_words:
        if word in text.lower():
            sentiment = "negative"
            break

    return EchoTextResponse(
        echo=text,
        analysis={
            "character_count": character_count,
            "word_count": word_count,
            "language": language,
            "sentiment": sentiment
        },
        timestamp=datetime.now()
    )"""

    # External API endpoints
    elif operation_id == "get_weather":
        return """    try:
        result = await external_service.get_weather(city=request.city)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"天気情報の取得に失敗しました: {str(e)}"
        )"""

    elif operation_id == "get_random_quote":
        return """    try:
        result = await external_service.get_random_quote()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"名言の取得に失敗しました: {str(e)}"
        )"""

    elif operation_id == "get_random_fact":
        return """    try:
        result = await external_service.get_random_fact()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"豆知識の取得に失敗しました: {str(e)}"
        )"""

    elif operation_id == "get_programming_joke":
        return """    try:
        joke_data = await external_service.get_random_joke()
        return JokeResponse(
            joke=joke_data["joke"],
            type=joke_data.get("category", "programming")
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ジョークの取得に失敗しました: {str(e)}"
        )"""

    # Default fallback
    else:
        return '    # TODO: 実装が必要\n    raise HTTPException(status_code=501, detail="Not implemented")'


def main():
    """メイン処理"""
    print("🚀 OpenAPI YAML-firstコード生成を開始...")

    # パス設定
    project_root = Path(__file__).parent.parent
    yaml_path = project_root / "source" / "openapi.yaml"
    output_dir = project_root / "app" / "generated"

    if not yaml_path.exists():
        print(f"❌ OpenAPI YAML ファイルが見つかりません: {yaml_path}")
        sys.exit(1)

    try:
        # OpenAPI仕様をロード
        spec = load_openapi_spec(str(yaml_path))
        print(f"📖 OpenAPI仕様をロードしました: {yaml_path}")

        # モデル生成
        generate_pydantic_models(spec, str(output_dir))

        # ルーター生成
        generate_router_stubs(spec, str(output_dir))

        # 生成されたファイルをフォーマット
        format_generated_files(output_dir)

        print("✅ コード生成が完了しました！")
        print()
        print("📁 生成されたファイル:")
        print(f"  🔧 Pydanticモデル: {output_dir}/generated_models.py")
        print(f"  🌐 FastAPIルーター: {output_dir}/generated_router.py")
        print()
        print("💡 次のステップ:")
        print("  1. 生成されたスタブファイルに実装を追加")
        print("  2. main.pyでルーターをインポート・登録")
        print("  3. 型生成スクリプトを実行")

    except Exception as e:
        print(f"❌ コード生成エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
