import sys
import os

# Add Backend directory to sys.path so its local imports work
backend_path = os.path.join(os.path.dirname(__file__), '..', 'Backend')
sys.path.insert(0, backend_path)

from main import app

# Vercel needs the app object to be available as 'app'
