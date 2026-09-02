# ==============================================================================
# Apify B2B Lead Extractor - Elite Task Runner Makefile
# ==============================================================================

.PHONY: help setup run clean

help:
	@echo "=================================================="
	@echo " B2B Lead Extractor - Command Reference"
	@echo "=================================================="
	@echo "  make setup - Create virtual env & install dependencies"
	@echo "  make run   - Execute the lead extractor script"
	@echo "  make clean - Purge cache and virtual environment"
	@echo "=================================================="

setup:
	@echo "⚙️ Setting up Python virtual environment..."
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "✨ Setup complete! Run 'source venv/bin/activate' to activate."

run:
	@echo "🚀 Running B2B Lead Extractor pipeline..."
	python lead_extractor.py

clean:
	@echo "🧹 Cleaning up cache and virtual environment..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf venv/
	@echo "✨ Clean complete."
