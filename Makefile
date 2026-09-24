.PHONY: help setup all start_server start_tests clean clean-backend #clean-mobile

help:
	@echo "Nome_Projeto — comandos disponíveis:"
	@echo "  make all            Roda start_tests + start_server"
	@echo "  make clean          Limpa caches e artefatos"
	@echo "  make setup          Prepara os scripts"
	@echo "  make start-server   Sobe o servidor Django"
	@echo "  make start-tests    Roda os testes (ruff + pytest)"
	@echo "  make clean-backend  Limpa caches e artefatos somente do backend"
#	@echo "  make clean-mobile   Limpa caches e artefatos somente do mobile"

all: start_tests start_server

clean: clean-backend #clean-mobile

setup:
	@chmod +x backend/start_tests.sh backend/start_server.sh

start:
	@chmod +x backend/start.sh
	@./backend/start.sh

start-server: start
	@python manage.py runserver

start-tests: start
# 1. Lint
	@python -m ruff check .

# 2. Testes
	@python -m pytest --cov=. --cov-report=term-missing

clean-tests:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name db.sqlite3 -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name venv -exec rm -rf {} + 2>/dev/null || true

#clean-mobile:
#	@rm -rf mobile/node_modules mobile/www mobile/.angular 2>/dev/null || true


