"""Utility functions for the application."""

import json
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def export_openapi_to_file(app: FastAPI, output_path: str = "openapi.json") -> None:
    """
    Export OpenAPI schema to a JSON file.

    Args:
        app: FastAPI application instance
        output_path: Path to save the OpenAPI schema
    """
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)


def export_openapi_to_yaml(app: FastAPI, output_path: str = "openapi.yaml") -> None:
    """
    Export OpenAPI schema to a YAML file.

    Args:
        app: FastAPI application instance
        output_path: Path to save the OpenAPI schema
    """
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(openapi_schema, f, default_flow_style=False, allow_unicode=True)


def load_config_from_yaml(file_path: str) -> dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        file_path: Path to the YAML configuration file

    Returns:
        Dictionary containing the configuration
    """
    config_path = Path(file_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config_to_yaml(config: dict[str, Any], file_path: str) -> None:
    """
    Save configuration to a YAML file.

    Args:
        config: Configuration dictionary
        file_path: Path to save the YAML configuration file
    """
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
