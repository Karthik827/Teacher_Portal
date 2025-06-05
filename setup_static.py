#!/usr/bin/env python
"""
Script to ensure static directories are properly set up.
"""
import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

# Create static directory if it doesn't exist
STATIC_DIR = BASE_DIR / 'static'
STATIC_DIR.mkdir(exist_ok=True)

# Create staticfiles directory if it doesn't exist
STATICFILES_DIR = BASE_DIR / 'staticfiles'
STATICFILES_DIR.mkdir(exist_ok=True)

print("Static directories created successfully!")