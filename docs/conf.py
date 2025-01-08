import os
import sys
from pathlib import Path
import django

root = Path.cwd().parent.resolve()
sys.path.append(str(root))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banjo.settings_docs')
django.setup()

project = 'Banjo'
copyright = '2024, Chris Proctor'
author = 'Chris Proctor'
release = '0.8.1'
extensions = ['sphinx.ext.viewcode', 'sphinx.ext.autodoc']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'furo'
html_static_path = ['_static']

"""
   http
   models
   runner
   urls
   views
"""
