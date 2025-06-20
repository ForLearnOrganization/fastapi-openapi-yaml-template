#!/usr/bin/env python3
"""
OpenAPI YAML ファーストアプローチ用のコード生成スクリプト

手書きのopenapi.yamlからPydanticモデルとFastAPIエンドポイントを生成します。
"""

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


def load_openapi_spec(yaml_path: str) -> Dict[str, Any]:
    """OpenAPI YAML仕様をロードします。"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_pydantic_models(spec: Dict[str, Any], output_dir: str) -> None:
    """Pydanticモデルを生成します。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    models_file = output_path / "generated_models.py"
    
    content = """\"\"\"
OpenAPI YAML仕様から自動生成されたPydanticモデル
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
\"\"\"

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


"""
    
    # コンポーネント/スキーマからモデルを生成
    schemas = spec.get('components', {}).get('schemas', {})
    
    for schema_name, schema_def in schemas.items():
        if schema_def.get('type') == 'object':
            model_code = generate_model_class(schema_name, schema_def)
            content += model_code + "\n\n"
    
    with open(models_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Pydanticモデルを生成しました: {models_file}")


def generate_model_class(name: str, schema: Dict[str, Any]) -> str:
    """単一のPydanticモデルクラスを生成します。"""
    description = schema.get('description', '')
    properties = schema.get('properties', {})
    required = schema.get('required', [])
    
    # クラス定義開始
    class_def = f'class {name}(BaseModel):'
    if description:
        class_def += f'\n    """{description}"""'
    
    class_def += '\n'
    
    # プロパティを生成
    for prop_name, prop_def in properties.items():
        is_required = prop_name in required
        field_type = convert_openapi_type_to_python(prop_def)
        field_description = prop_def.get('description', '')
        
        # デフォルト値の処理
        default_value = prop_def.get('default')
        field_def = ""
        
        if not is_required:
            if default_value is not None:
                if isinstance(default_value, str):
                    field_def = f' = "{default_value}"'
                else:
                    field_def = f' = {default_value}'
            else:
                field_type = f'Optional[{field_type}]'
                field_def = ' = None'
        
        # Field()を使用した詳細定義
        field_params = []
        if field_description:
            field_params.append(f'description="{field_description}"')
        
        # 数値制約
        if 'minimum' in prop_def:
            field_params.append(f'ge={prop_def["minimum"]}')
        if 'maximum' in prop_def:
            field_params.append(f'le={prop_def["maximum"]}')
        
        # 文字列制約
        if 'minLength' in prop_def:
            field_params.append(f'min_length={prop_def["minLength"]}')
        if 'maxLength' in prop_def:
            field_params.append(f'max_length={prop_def["maxLength"]}')
        
        if field_params:
            field_def = f' = Field({", ".join(field_params)})'
        
        class_def += f'    {prop_name}: {field_type}{field_def}\n'
    
    return class_def


def convert_openapi_type_to_python(prop_def: Dict[str, Any]) -> str:
    """OpenAPIプロパティ定義をPython型に変換します。"""
    prop_type = prop_def.get('type', 'any')
    prop_format = prop_def.get('format')
    
    if prop_type == 'string':
        if prop_format == 'date-time':
            return 'datetime'
        return 'str'
    elif prop_type == 'integer':
        return 'int'
    elif prop_type == 'number':
        return 'float'
    elif prop_type == 'boolean':
        return 'bool'
    elif prop_type == 'array':
        item_type = convert_openapi_type_to_python(prop_def.get('items', {}))
        return f'List[{item_type}]'
    elif prop_type == 'object':
        return 'Dict[str, Any]'
    else:
        # $refの処理
        ref = prop_def.get('$ref')
        if ref:
            return ref.split('/')[-1]
        return 'Any'


def generate_router_stubs(spec: Dict[str, Any], output_dir: str) -> None:
    """FastAPIルータースタブを生成します。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    router_file = output_path / "generated_router.py"
    
    content = """\"\"\"
OpenAPI YAML仕様から自動生成されたFastAPIルーター
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
\"\"\"

from fastapi import APIRouter, HTTPException
from app.generated.generated_models import *

# タグ別にルーターを分割
health_router = APIRouter(prefix="/api/v1/health", tags=["health"])
text_router = APIRouter(prefix="/api/v1/text", tags=["text"])
external_router = APIRouter(prefix="/api/v1/external", tags=["external"])
legacy_router = APIRouter(tags=["text"])


"""
    
    # パスからエンドポイントを生成
    paths = spec.get('paths', {})
    
    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                endpoint_code = generate_endpoint_stub(path, method, operation)
                content += endpoint_code + "\n\n"
    
    # 主ルーターに登録
    content += """
# メインルーターを作成
main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(text_router)
main_router.include_router(external_router)
main_router.include_router(legacy_router)
"""
    
    with open(router_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ FastAPIルータースタブを生成しました: {router_file}")


def generate_endpoint_stub(path: str, method: str, operation: Dict[str, Any]) -> str:
    """単一のエンドポイントスタブを生成します。"""
    operation_id = operation.get('operationId', f'{method}_{path.replace("/", "_").replace("{", "").replace("}", "")}')
    summary = operation.get('summary', '')
    description = operation.get('description', '')
    tags = operation.get('tags', [])
    
    # ルーター選択
    router_name = "main_router"
    if tags:
        tag = tags[0]
        if tag == "health":
            router_name = "health_router"
        elif tag == "text":
            if path.startswith("/generate"):
                router_name = "legacy_router"
            else:
                router_name = "text_router"
        elif tag == "external":
            router_name = "external_router"
    
    # リクエストボディの処理
    request_body = operation.get('requestBody')
    request_param = ""
    if request_body:
        content = request_body.get('content', {})
        json_content = content.get('application/json', {})
        schema = json_content.get('schema', {})
        ref = schema.get('$ref')
        if ref:
            model_name = ref.split('/')[-1]
            request_param = f"request: {model_name}"
    
    # レスポンスの処理
    responses = operation.get('responses', {})
    success_response = responses.get('200', {})
    content = success_response.get('content', {})
    json_content = content.get('application/json', {})
    schema = json_content.get('schema', {})
    ref = schema.get('$ref')
    response_type = "dict"
    if ref:
        response_type = ref.split('/')[-1]
    
    # パスパラメータの処理
    path_params = re.findall(r'\\{([^}]+)\\}', path)
    path_param_str = ""
    if path_params:
        path_param_str = ", " + ", ".join([f"{param}: str" for param in path_params])
    
    # 関数生成
    decorator = f'@{router_name}.{method.lower()}("{path}"'
    if summary:
        decorator += f', summary="{summary}"'
    decorator += ')'
    
    function_def = f"async def {operation_id}("
    if request_param:
        function_def += request_param
    if path_param_str:
        function_def += path_param_str
    function_def += f") -> {response_type}:"
    
    docstring = ""
    if description:
        docstring = f'    """{description}"""'
    
    body = '    # TODO: 実装が必要\n    raise HTTPException(status_code=501, detail="Not implemented")'
    
    return f"{decorator}\n{function_def}\n{docstring}\n{body}"


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