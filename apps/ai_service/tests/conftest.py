"""
Pytest configuration and fixtures for ClearStack AI Service tests.
This file ensures Python can find and import the apps.ai_service module.
"""
import sys
from pathlib import Path

# Add project root to Python path so imports like 'from apps.ai_service...' work
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
