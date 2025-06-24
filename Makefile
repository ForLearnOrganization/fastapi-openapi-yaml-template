# 自作コマンド定義ファイル
# (makeコマンドに半角スペースは使えないため、代わりにハイフンを使用)

start:
	poetry run uvicorn main:app --reload

# コードの整形コマンド
# (lintでエラーが出てもtrueで無視してformat実行すると、lintエラーが直るため下記コマンドとしている)
# (--fixとformatは整形内容が違うため両方実行する)
format:
	poetry run ruff check --fix || true
	poetry run ruff format

lint:
	poetry run ruff check .

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=app tests/

generate:
	python3 scripts/generate_all.py

generate-docs:
	python3 scripts/generate_docs.py

generate-frontend:
	python3 scripts/generate_frontend_code.py

generate-backend:
	python3 scripts/generate_backend_code.py
