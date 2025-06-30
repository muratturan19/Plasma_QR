#!/usr/bin/env bash
# Build single-file executable with PyInstaller
# Must be run on Windows or using Wine/compat layer for Windows output.

pyinstaller --onefile run_app.py \
  --copy-metadata streamlit \
  --add-data 'Guidelines/*:Guidelines' \
  --add-data 'Prompts/*:Prompts' \
  --add-data 'Fonts/*:Fonts' \
  --add-data 'Logo/*:Logo' \
  --add-data "UI/streamlit_app.py:UI" \
  --add-data 'CC/*:CC'
