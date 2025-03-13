#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies for Playwright
playwright install-deps

# Install Playwright browsers
python -m playwright install --with-deps chromium firefox webkit

# Make browsers executable
chmod -R 777 ~/.cache/ms-playwright/ 