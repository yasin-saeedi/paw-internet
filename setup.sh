#!/bin/bash
pip install playwright requests -q
playwright install chromium
playwright install-deps chromium
echo "✅ آماده است"
