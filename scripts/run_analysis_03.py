#!/usr/bin/env python3
"""
Simple script to run wind analysis - ALWAYS uses virtual environment
"""


#!/usr/bin/env python3
"""
Enhanced Wind Analysis for Lake Kariba
"""

import matplotlib
# Use non-interactive backend to avoid display issues
matplotlib.use('Agg')  # Use 'Agg' backend which doesn't require display
import matplotlib.pyplot as plt

# Rest of your imports...
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import pandas as pd
import os
import sys
from datetime import datetime
from pathlib import Path

# Rest of your code...






# Define virtual environment path
VENV_PATH = "/home/chawas/deployed/deployed_env"
VENV_PYTHON = os.path.join(VENV_PATH, "bin", "python3")
PROJECT_ROOT = "/home/chawas/deployed/charara"
SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "enhanced_wind_analysis.py")

def check_virtual_environment():
    """Check if virtual environment exists and is usable"""
    print("="*80)
    print("CHECKING VIRTUAL ENVIRONMENT")
    print("="*80)
    
    # Check if virtual environment directory exists
    if not os.path.exists(VENV_PATH):
        print(f"❌ Virtual environment not found at: {VENV_PATH}")
        print("\nTo create virtual environment:")
        print(f"cd /home/chawas/deployed")
        print(f"python3 -m venv deployed_env")
        print(f"source deployed_env/bin/activate")
        print(f"pip install xarray numpy pandas matplotlib cartopy geopandas scipy")
        return False
    
    # Check if Python exists in virtual environment
    if not os.path.exists(VENV_PYTHON):
        print(f"❌ Python not found in virtual environment: {VENV_PYTHON}")
        return False
    
    print(f"✓ Virtual environment found: {VENV_PATH}")
    print(f"✓ Virtual environment Python: {VENV_PYTHON}")
    return True

def check_imports():
    """Check if required packages are installed in virtual environment"""
    print("\n" + "="*80)
    print("CHECKING PACKAGES IN VIRTUAL ENVIRONMENT")
    print("="*80)
    
    test_code = """
import sys
print(f"Python: {sys.executable}")
print(f"Version: {sys.version}")

try:
    import numpy as np
    import xarray as xr
    import pandas as pd
    import matplotlib as mpl
    print(f"✅ numpy: {np.__version__}")
    print(f"✅ xarray: {xr.__version__}")
    print(f"✅ pandas: {pd.__version__}")
    print(f"✅ matplotlib: {mpl.__version__}")
    
    # Try optional imports
    try:
        import cartopy.crs as ccrs
        print(f"✅ cartopy: {ccrs.__version__}")
    except:
        print("⚠ cartopy: Not installed (optional)")
        
    try:
        import geopandas as gpd
        print("✅ geopandas: Installed")
    except:
        print("⚠ geopandas: Not installed (optional)")
        
    return 0
    
except ImportError as e:
    print(f"❌ Missing package: {e}")
    return 1
"""
    
    try:
        # Run the test using virtual environment Python
        result = subprocess.run(
            [VENV_PYTHON, "-c", test_code],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(result.stdout)
        
        if "❌ Missing package" in result.stdout:
            return False
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking packages: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def install_missing_packages():
    """Install missing packages in virtual environment"""
    print("\n" + "="*80)
    print("INSTALLING MISSING PACKAGES")
    print("="*80)
    
    packages = [
        "numpy",
        "xarray",
        "pandas",
        "matplotlib",
        "scipy",
        "netCDF4",
        "cartopy",
        "geopandas",
        "shapely",
        "pyproj",
        "fiona"
    ]
    
    print("Installing packages in virtual environment...")
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.run(
                [VENV_PYTHON, "-m", "pip", "install", package],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"  ✓ {package}")
        except subprocess.CalledProcessError as e:
            print(f"  ⚠ {package}: {e.stderr}")
    
    return True

def run_analysis():
    """Run the wind analysis using virtual environment"""
    print("\n" + "="*80)
    print("RUNNING WIND ANALYSIS FOR LAKE KARIBA")
    print("="*80)
    
    # Check if analysis script exists
    if not os.path.exists(SCRIPT_PATH):
        print(f"❌ Analysis script not found: {SCRIPT_PATH}")
        print(f"\nExpected at: {SCRIPT_PATH}")
        return False
    
    print(f"✓ Analysis script found: {SCRIPT_PATH}")
    print(f"✓ Using virtual environment: {VENV_PATH}")
    print("\nStarting analysis...")
    print("-" * 80)
    
    try:
        # Run the analysis script using virtual environment Python
        result = subprocess.run(
            [VENV_PYTHON, SCRIPT_PATH],
            check=False  # Don't raise exception, we'll handle it
        )
        
        print("-" * 80)
        
        if result.returncode == 0:
            print("\n✅ ANALYSIS COMPLETED SUCCESSFULLY!")
            return True
        else:
            print("\n⚠ Analysis completed with exit code:", result.returncode)
            return False
            
    except KeyboardInterrupt:
        print("\n\n⏹ Analysis interrupted by user.")
        return False
    except Exception as e:
        print(f"\n❌ Error running analysis: {e}")
        return False

def main():
    """Main function"""
    
    # Step 1: Check virtual environment
    if not check_virtual_environment():
        create_env = input("\nCreate virtual environment? (y/n): ").lower()
        if create_env == 'y':
            print("\nCreating virtual environment...")
            try:
                subprocess.run(["python3", "-m", "venv", VENV_PATH], check=True)
                print(f"✓ Created virtual environment: {VENV_PATH}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to create virtual environment: {e}")
                return 1
        else:
            print("\nCannot proceed without virtual environment.")
            return 1
    
    # Step 2: Check packages
    if not check_imports():
        install = input("\nInstall missing packages? (y/n): ").lower()
        if install == 'y':
            install_missing_packages()
            # Re-check
            if not check_imports():
                print("\n❌ Still missing required packages.")
                return 1
        else:
            print("\n❌ Cannot proceed without required packages.")
            return 1
    
    # Step 3: Run analysis
    success = run_analysis()
    
    print("\n" + "="*80)
    if success:
        print("✅ WIND ANALYSIS COMPLETE!")
        print(f"\nOutputs are in: {os.path.join(PROJECT_ROOT, 'output')}")
    else:
        print("⚠ Analysis had issues. Check output above.")
    
    print("="*80)
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹ Script interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)