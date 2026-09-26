.PHONY: help start-backend start-mobile test-backend clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make start-backend  Instala dependências e sobe o servidor Django"
	@echo "  make test-backend   Roda o ruff e o pytest no backend"
	@echo "  make start-mobile   Instala dependências e sobe o app mobile"
	@echo "  make clean          Limpa caches de ambos os projetos"

start-backend:
	@python -m venv venv
	@venv/bin/pip install -r backend/requirements.txt
	@cd backend && ../venv/bin/python manage.py migrate
	@echo "Venv criada.\nPara ativar no seu terminal, use: source venv/bin/activate\nPara encerrar, use: deactivate"

test-backend:
	@cd backend && ../venv/bin/python -m ruff check .
	@cd backend && ../venv/bin/python -m pytest --cov=. --cov-report=term-missing

start-mobile:
	@cd mobile && npm install
	@cd mobile && npm start # ou 'ng serve', dependendo do seu framework

clean:
	@echo "Limpando artefatos do backend..."
	@find . -type d -name "venv" -prune | xargs rm -rf
	@find . -type d -name "__pycache__" -prune | xargs rm -rf
	@find . -type d -name ".pytest_cache" -prune | xargs rm -rf
	@find . -type d -name ".ruff_cache" -prune | xargs rm -rf
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "db.sqlite3" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
#	@echo "Limpando artefatos do mobile..."
#	@find . -type d -name "mobile/node_modules" -prune | xargs rm -rf
#	@find . -type d -name "mobile/www" -prune | xargs rm -rf
#	@find . -type d -name "mobile/.angular" -prune | xargs rm -rf