source venv/bin/activate

# 1. Lint
python -m ruff check .

# 2. Testes
python -m pytest --cov=. --cov-report=term-missing