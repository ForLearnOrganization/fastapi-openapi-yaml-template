# 自作コマンド定義ファイル

# コードの整形コマンド
# (lintでエラーが出てもtrueで無視してformat実行するとすると、lintエラーが直るため下記コマンドとしている)
# (--fixとformatは整形内容が違うため両方実行する)
format:
	poetry run ruff check --fix || true
	poetry run ruff format

lint:
	poetry run ruff check .

test:
	poetry run pytest
