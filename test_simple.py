#!/home/chawas/deployed/deployed_env/bin/python3
"""
Simple test script
"""
print("="*80)
print("TEST SCRIPT RUNNING")
print("="*80)

import sys
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")

# Test imports
try:
    import numpy as np
    print(f"✅ numpy: {np.__version__}")
except ImportError as e:
    print(f"❌ numpy: {e}")

try:
    import xarray as xr
    print(f"✅ xarray: {xr.__version__}")
except ImportError as e:
    print(f"❌ xarray: {e}")

try:
    import pandas as pd
    print(f"✅ pandas: {pd.__version__}")
except ImportError as e:
    print(f"❌ pandas: {e}")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)