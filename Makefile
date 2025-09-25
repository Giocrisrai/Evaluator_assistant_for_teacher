# Makefile para Sistema de Evaluación Kedro ML
# Comandos simplificados para operaciones comunes

.PHONY: help install test evaluate-single evaluate-all report clean setup validate

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
OUTPUT_DIR := evaluaciones
CSV_FILE := data/estudiantes_kedro.csv

# Colores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Muestra esta ayuda
	@echo "$(GREEN)Sistema de Evaluación Kedro ML - Comandos disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instala todas las dependencias
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencias instaladas$(NC)"

setup: ## Configuración inicial completa
	@echo "$(GREEN)Configurando el sistema...$(NC)"
	@echo "$(YELLOW)1. Creando estructura de directorios...$(NC)"
	mkdir -p $(OUTPUT_DIR)
	mkdir -p data/input
	mkdir -p data/output
	mkdir -p data/cache
	mkdir -p logs
	@echo "$(YELLOW)2. Instalando dependencias...$(NC)"
	$(MAKE) install
	@echo "$(YELLOW)3. Verificando configuración...$(NC)"
	$(MAKE) validate
	@echo "$(GREEN)✓ Sistema configurado correctamente$(NC)"

validate: ## Valida la instalación
	@echo "$(GREEN)Validando instalación...$(NC)"
	$(PYTHON) scripts/validate_installation.py

test: ## Ejecuta tests del sistema
	@echo "$(GREEN)Ejecutando tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v

evaluate-single: ## Evalúa un solo repositorio (usar con REPO=url STUDENT=nombre)
	@if [ -z "$(REPO)" ]; then \
		echo "$(RED)Error: Especifica REPO=url_repositorio$(NC)"; \
		exit 1; \
	fi
	@if [ -z "$(STUDENT)" ]; then \
		echo "$(RED)Error: Especifica STUDENT=nombre_estudiante$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Evaluando proyecto de $(STUDENT)...$(NC)"
	$(PYTHON) src/kedro_evaluator.py "$(GITHUB_TOKEN)" "$(REPO)" "$(STUDENT)"

evaluate-all: ## Evalúa todos los estudiantes del CSV
	@echo "$(GREEN)Evaluando todos los proyectos...$(NC)"
	@if [ ! -f $(CSV_FILE) ]; then \
		echo "$(RED)Error: No se encuentra $(CSV_FILE)$(NC)"; \
		exit 1; \
	fi
	$(PYTHON) scripts/evaluate_batch.py \
		--csv $(CSV_FILE) \
		--output $(OUTPUT_DIR) \
		--parallel 3

evaluate-debug: ## Evalúa en modo debug (más información)
	@echo "$(GREEN)Evaluando en modo debug...$(NC)"
	$(PYTHON) scripts/evaluate_batch.py \
		--csv $(CSV_FILE) \
		--output $(OUTPUT_DIR) \
		--parallel 1 \
		--debug

report: ## Genera reportes consolidados
	@echo "$(GREEN)Generando reportes...$(NC)"
	$(PYTHON) scripts/generate_reports.py \
		--input $(OUTPUT_DIR) \
		--format html,pdf,excel

stats: ## Muestra estadísticas de las evaluaciones
	@echo "$(GREEN)Estadísticas de evaluaciones:$(NC)"
	@find $(OUTPUT_DIR) -name "*.json" | wc -l | xargs echo "Total evaluaciones:"
	@find $(OUTPUT_DIR) -name "estadisticas_*.json" -exec cat {} \; | \
		$(PYTHON) -c "import sys, json; data=json.load(sys.stdin); \
		print(f'Aprobados: {data.get(\"aprobados\", 0)}'); \
		print(f'Reprobados: {data.get(\"reprobados\", 0)}'); \
		print(f'Nota promedio: {data.get(\"nota_promedio\", 0):.2f}')" 2>/dev/null || \
		echo "No hay estadísticas disponibles aún"

clean: ## Limpia archivos temporales y cache
	@echo "$(YELLOW)Limpiando archivos temporales...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf data/cache/*
	@echo "$(GREEN)✓ Limpieza completada$(NC)"

clean-all: clean ## Limpia todo incluyendo evaluaciones
	@echo "$(RED)⚠ Eliminando todas las evaluaciones...$(NC)"
	@read -p "¿Estás seguro? [y/N]: " confirm && \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			rm -rf $(OUTPUT_DIR)/*; \
			echo "$(GREEN)✓ Evaluaciones eliminadas$(NC)"; \
		else \
			echo "$(YELLOW)Operación cancelada$(NC)"; \
		fi

docker-build: ## Construye imagen Docker
	@echo "$(GREEN)Construyendo imagen Docker...$(NC)"
	docker build -t kedro-evaluator:latest .

docker-run: ## Ejecuta el evaluador en Docker
	@echo "$(GREEN)Ejecutando en Docker...$(NC)"
	docker run -it --rm \
		-v $(PWD)/data:/app/data \
		-v $(PWD)/evaluaciones:/app/evaluaciones \
		-e GITHUB_TOKEN=$(GITHUB_TOKEN) \
		kedro-evaluator:latest

ollama-install: ## Instala y configura Ollama
	@echo "$(GREEN)Instalando Ollama...$(NC)"
	@if command -v ollama >/dev/null 2>&1; then \
		echo "$(YELLOW)Ollama ya está instalado$(NC)"; \
	else \
		curl -fsSL https://ollama.ai/install.sh | sh; \
	fi
	@echo "$(GREEN)Descargando modelo llama2...$(NC)"
	ollama pull llama2

ollama-status: ## Verifica estado de Ollama
	@echo "$(GREEN)Estado de Ollama:$(NC)"
	@if command -v ollama >/dev/null 2>&1; then \
		echo "✓ Ollama instalado"; \
		ollama list 2>/dev/null || echo "⚠ Servicio no activo"; \
	else \
		echo "✗ Ollama no instalado"; \
	fi

backup: ## Crea backup de evaluaciones
	@echo "$(GREEN)Creando backup...$(NC)"
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	tar -czf backups/evaluaciones_$$timestamp.tar.gz $(OUTPUT_DIR)/; \
	echo "$(GREEN)✓ Backup creado: backups/evaluaciones_$$timestamp.tar.gz$(NC)"

restore: ## Restaura backup (usar con BACKUP=archivo.tar.gz)
	@if [ -z "$(BACKUP)" ]; then \
		echo "$(RED)Error: Especifica BACKUP=archivo.tar.gz$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Restaurando backup...$(NC)"
	tar -xzf $(BACKUP) -C .
	@echo "$(GREEN)✓ Backup restaurado$(NC)"

# Comandos de desarrollo
dev-install: ## Instala dependencias de desarrollo
	$(PIP) install -r requirements-dev.txt

dev-format: ## Formatea código con black
	black src/ scripts/ tests/

dev-lint: ## Ejecuta linters
	flake8 src/ scripts/
	mypy src/

dev-test-coverage: ## Ejecuta tests con cobertura
	pytest tests/ --cov=src --cov-report=html

# Atajo para configuración rápida
quick-start: setup ## Configuración rápida inicial
	@echo "$(GREEN)================================$(NC)"
	@echo "$(GREEN)Sistema listo para usar!$(NC)"
	@echo "$(GREEN)================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Siguiente paso:$(NC)"
	@echo "1. Configura tu GitHub token:"
	@echo "   export GITHUB_TOKEN='tu_token_aqui'"
	@echo ""
	@echo "2. Edita el archivo CSV con los estudiantes:"
	@echo "   nano $(CSV_FILE)"
	@echo ""
	@echo "3. Ejecuta la evaluación:"
	@echo "   make evaluate-all"
	@echo ""
	@echo "$(GREEN)Para más ayuda: make help$(NC)"

.DEFAULT_GOAL := help
