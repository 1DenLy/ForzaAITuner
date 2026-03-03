# ============================================================
#  ForzaAITuner — Developer Makefile
# ============================================================
.PHONY: ui install test run lint

## Compile all .ui assets to Python (AOT — Ahead-of-Time)
ui:
	python scripts/compile_ui.py

## Install all dependencies
install:
	pip install -r requirements.txt

## Run unit tests
test:
	pytest tests/ -v

## Run the desktop application
run:
	python src/main.py

## Lint with flake8 (optional)
lint:
	flake8 src/ tests/ --max-line-length=120
