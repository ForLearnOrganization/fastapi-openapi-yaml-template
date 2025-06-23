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


def extract_tags_from_spec(spec: dict[str, Any]) -> list[dict[str, str]]:
    """OpenAPI仕様からタグ情報を抽出します。"""
    tags = spec.get("tags", [])
    return [{"name": tag["name"], "description": tag.get("description", "")} for tag in tags]


def extract_router_prefixes_from_paths(spec: dict[str, Any]) -> dict[str, str]:
    """パスから各タグのプレフィックスを抽出します。"""
    paths = spec.get("paths", {})
    tag_prefixes = {}
    
    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.lower() in ["get", "post", "put", "delete", "patch"]:
                tags = operation.get("tags", [])
                if tags:
                    tag_name = tags[0]  # 最初のタグを使用
                    
                    # レガシーパスは特別扱い
                    if path.startswith("/generate"):
                        continue  # レガシーパスはプレフィックス抽出をスキップ
                    
                    # パスからプレフィックスを推測
                    if path.startswith("/api/v1/"):
                        # /api/v1/health/ -> /health
                        # /api/v1/text/generate -> /text
                        path_parts = path.split("/")[3:]  # ['health', ''] または ['text', 'generate']
                        if path_parts and path_parts[0]:
                            prefix = f"/{path_parts[0]}"
                            if tag_name not in tag_prefixes:
                                tag_prefixes[tag_name] = prefix
    
    return tag_prefixes


def generate_router_definitions(spec: dict[str, Any]) -> str:
    """タグ情報から動的にルーター定義を生成します。"""
    tags = extract_tags_from_spec(spec)
    tag_prefixes = extract_router_prefixes_from_paths(spec)
    
    router_definitions = []
    router_names = []
    
    for tag in tags:
        tag_name = tag["name"]
        prefix = tag_prefixes.get(tag_name, f"/{tag_name}")
        
        router_var_name = f"{tag_name}_router"
        router_names.append(router_var_name)
        
        router_def = f'{router_var_name} = APIRouter(prefix="{prefix}", tags=["{tag_name}"])'
        router_definitions.append(router_def)
    
    # レガシールーター（プレフィックスなし）の処理
    legacy_needed = False
    paths = spec.get("paths", {})
    for path in paths.keys():
        if not path.startswith("/api/v1/"):
            legacy_needed = True
            break
    
    if legacy_needed:
        router_definitions.append('legacy_router = APIRouter(tags=["text"])')
        router_names.append("legacy_router")
    
    return "\n".join(router_definitions), router_names


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

    # 動的ルーター定義を生成
    router_definitions, router_names = generate_router_definitions(spec)

    content = f'''"""
OpenAPI YAML仕様から自動生成されたFastAPIルーター
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
"""

from fastapi import APIRouter

# ruff: noqa: F401
from app.generated.generated_models import {imports_str}
from app.services.external_service import (
    get_external_fact,
    get_external_joke,
    get_external_quote,
    post_external_weather,
)
from app.services.health import get_health, get_health_detailed
from app.services.text_service import post_generate, post_text_echo, post_text_generate

# タグ別にルーターを分割（prefixは相対パスのみ、main.pyで/api/v1が追加される）
{router_definitions}


'''

    # パスからエンドポイントを生成
    paths = spec.get("paths", {})

    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.lower() in ["get", "post", "put", "delete", "patch"]:
                endpoint_code = generate_endpoint_implementation(
                    path, method, operation, spec
                )
                content += endpoint_code + "\n\n"

    # 主ルーターに登録 - 動的生成
    main_router_includes = []
    for router_name in router_names:
        if router_name != "legacy_router":  # Legacy router is mounted separately
            main_router_includes.append(f"main_router.include_router({router_name})")
    
    router_registration = "\n".join(main_router_includes)
    
    content += f"""
# メインルーターを作成
main_router = APIRouter()
{router_registration}

# Legacy router should be separate (not include in main_router)
# so it can be mounted without /api/v1 prefix
"""

    with open(router_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ FastAPIルータースタブを生成しました: {router_file}")


def generate_endpoint_implementation(
    path: str, method: str, operation: dict[str, Any], spec: dict[str, Any]
) -> str:
    """単一のエンドポイント実装を生成します。"""
    operation_id = operation.get(
        "operationId",
        f'{method}_{path.replace("/", "_").replace("{", "").replace("}", "")}',
    )
    summary = operation.get("summary", "")
    description = operation.get("description", "")
    tags = operation.get("tags", [])

    # ルーター選択と相対パス計算 - 動的生成
    router_name = "main_router"
    relative_path = path

    if tags:
        tag = tags[0]
        tag_prefixes = extract_router_prefixes_from_paths(spec)
        
        if tag in tag_prefixes:
            if path.startswith("/generate"):
                # レガシーエンドポイントの特別処理
                router_name = "legacy_router"
                relative_path = path  # /generate stays as is
            else:
                router_name = f"{tag}_router"
                prefix = tag_prefixes[tag]
                if prefix and path.startswith(f"/api/v1{prefix}"):
                    # /api/v1/health/ -> / または /api/v1/health/detailed -> /detailed
                    relative_path = path.replace(f"/api/v1{prefix}", "") or "/"
                elif not prefix:
                    # プレフィックスが空の場合はそのまま
                    relative_path = path

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

    # Create service function mapping based on operation_id and path
    service_function_map = {
        "health_check": "return await get_health()",
        "detailed_health_check": "return await get_health_detailed()",
        "generate_text": "return await post_text_generate(request)" if request_param else "return await post_text_generate()",
        "generate_text_legacy": "return await post_generate(request)" if request_param else "return await post_generate()",
        "echo_text": "return await post_text_echo(request)" if request_param else "return await post_text_echo()",
        "get_weather": "return await post_external_weather(request)" if request_param else "return await post_external_weather()",
        "get_random_quote": "return await get_external_quote()",
        "get_random_fact": "return await get_external_fact()",
        "get_programming_joke": "return await get_external_joke()",
    }

    # Return the service function call if mapped, otherwise default
    if operation_id in service_function_map:
        return f"    {service_function_map[operation_id]}"
    else:
        # Default fallback - still use service pattern
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
