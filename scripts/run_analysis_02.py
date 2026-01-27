#!/home/chawas/deployed/deployed_env/bin/python3
"""
Lake Kariba Wind Analysis
Using virtual environment: deployed_env
"""

import sys
import os

# Add virtual environment site-packages to path
venv_path = "/home/chawas/deployed/deployed_env"
site_packages = os.path.join(venv_path, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
sys.path.insert(0, site_packages)

# Also add project directories
project_root = "/home/chawas/deployed/charara"
sys.path.insert(0, os.path.join(project_root, "scripts"))

print(f"Python: {sys.executable}")
print(f"Virtual environment: {venv_path}")

# Now try imports
try:
    import numpy as np
    import xarray as xr
    import pandas as pd
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    
    print("✅ All imports successful!")
    print(f"xarray version: {xr.__version__}")
    
    # Rest of your code here...
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"\nCheck virtual environment: {venv_path}")
    print("Activate with: source /home/chawas/deployed/deployed_env/bin/activate")
    sys.exit(1)