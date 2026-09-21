.PHONY: help setup all start_server start_tests backend mobile clean clean-backend clean-mobile

help:
	@echo "Nome_Projeto — comandos disponíveis:"
	@echo "  make setup          Prepara os scripts"
	@echo "  make all            Roda start_tests + start_server"
	@echo "  make start_tests    Roda os testes (ruff + pytest)"
	@echo "  make start_server   Sobe o servidor Django"
	@echo "  make backend        Atalho para start_server"
	@echo "  make mobile         Sobe só o mobile (Ionic)"
	@echo "  make clean          Limpa caches e artefatos"

setup:
	@chmod +x backend/start_tests.sh backend/start_server.sh
	@echo "✅ Scripts prontos para uso."

all: start_tests start_server

start_server:
	@chmod +x backend/start_server.sh
	@./backend/start_server.sh

start_tests:
	@chmod +x backend/start_tests.sh
	@./backend/start_tests.sh

backend: start_server

mobile:
	@cd mobile && ./start.sh

clean-backend:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache do backend limpo."

clean-mobile:
	@rm -rf mobile/node_modules mobile/www mobile/.angular 2>/dev/null || true
	@echo "✅ Cache do mobile limpo."

clean: clean-backend clean-mobile
	@echo "✅ Limpeza completa."
