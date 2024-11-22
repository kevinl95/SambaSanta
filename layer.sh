mkdir python
poetry run python -m pip install --target=./python openai
zip -r lambda-layer.zip python