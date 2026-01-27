#!/usr/bin/env python3
"""
Run wind analysis with virtual environment - Improved error handling
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



# Define paths
VENV_PATH = "/home/chawas/deployed/deployed_env"
VENV_PYTHON = os.path.join(VENV_PATH, "bin", "python3")
PROJECT_ROOT = "/home/chawas/deployed/charara"
SCRIPT_DIR = os.path.join(PROJECT_ROOT, "scripts")
ANALYSIS_SCRIPT = os.path.join(SCRIPT_DIR, "enhanced_wind_analysis.py")

def debug_info():
    """Print debugging information"""
    print("="*80)
    print("DEBUG INFORMATION")
    print("="*80)
    print(f"Current directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Virtual environment path: {VENV_PATH}")
    print(f"Virtual environment exists: {os.path.exists(VENV_PATH)}")
    print(f"Analysis script exists: {os.path.exists(ANALYSIS_SCRIPT)}")
    print(f"Script directory exists: {os.path.exists(SCRIPT_DIR)}")

def run_simple_test():
    """Run a simple test to see if basic Python works"""
    print("\n" + "="*80)
    print("RUNNING SIMPLE TEST")
    print("="*80)
    
    test_code = "print('Hello from Python'); import sys; print(f'Python path: {sys.executable}')"
    
    try:
        # Try with system Python first
        result = subprocess.run(
            [sys.executable, "-c", test_code],
            capture_output=True,
            text=True
        )
        print("System Python test:")
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")
    except Exception as e:
        print(f"System Python test failed: {e}")
    
    # Try with virtual environment Python
    if os.path.exists(VENV_PYTHON):
        try:
            result = subprocess.run(
                [VENV_PYTHON, "-c", test_code],
                capture_output=True,
                text=True
            )
            print("\nVirtual environment Python test:")
            print(result.stdout)
            if result.stderr:
                print(f"Stderr: {result.stderr}")
        except Exception as e:
            print(f"Virtual environment test failed: {e}")
    else:
        print(f"\nVirtual environment Python not found: {VENV_PYTHON}")

def check_virtual_environment_simple():
    """Simple check for virtual environment"""
    if not os.path.exists(VENV_PATH):
        print(f"❌ Virtual environment not found at: {VENV_PATH}")
        return False
    
    if not os.path.exists(VENV_PYTHON):
        print(f"❌ Python not found in virtual environment: {VENV_PYTHON}")
        return False
    
    return True

def run_analysis_directly():
    """Try to run analysis directly"""
    print("\n" + "="*80)
    print("ATTEMPTING TO RUN ANALYSIS DIRECTLY")
    print("="*80)
    
    if not os.path.exists(ANALYSIS_SCRIPT):
        print(f"❌ Analysis script not found: {ANALYSIS_SCRIPT}")
        print("\nLooking for scripts in:", SCRIPT_DIR)
        if os.path.exists(SCRIPT_DIR):
            print("Files in scripts directory:")
            for f in os.listdir(SCRIPT_DIR):
                print(f"  - {f}")
        return False
    
    print(f"✓ Found analysis script: {ANALYSIS_SCRIPT}")
    
    # Change to project directory
    original_dir = os.getcwd()
    os.chdir(PROJECT_ROOT)
    
    try:
        # Try to import and run directly
        sys.path.insert(0, SCRIPT_DIR)
        
        # First check if we can import basic modules
        print("\nTesting imports...")
        try:
            import numpy as np
            print(f"✅ numpy: {np.__version__}")
        except ImportError as e:
            print(f"❌ numpy: {e}")
            return False
            
        try:
            import xarray as xr
            print(f"✅ xarray: {xr.__version__}")
        except ImportError as e:
            print(f"❌ xarray: {e}")
            return False
        
        # Now try to import the analysis module
        print("\nImporting analysis module...")
        try:
            from enhanced_wind_analysis import main
            print("✅ Successfully imported enhanced_wind_analysis")
        except ImportError as e:
            print(f"❌ Failed to import enhanced_wind_analysis: {e}")
            print("\nTrying to import config_manager first...")
            try:
                from config_manager import ConfigManager
                print("✅ config_manager imported successfully")
            except ImportError as e2:
                print(f"❌ config_manager import failed: {e2}")
            return False
        
        # Run the analysis
        print("\n" + "="*80)
        print("RUNNING WIND ANALYSIS")
        print("="*80)
        
        try:
            analyzer, results = main()
            print("\n✅ Analysis completed successfully!")
            return True
        except Exception as e:
            print(f"\n❌ Error during analysis execution: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.chdir(original_dir)

def run_with_virtual_env():
    """Run analysis using virtual environment Python"""
    print("\n" + "="*80)
    print("RUNNING WITH VIRTUAL ENVIRONMENT")
    print("="*80)
    
    if not os.path.exists(VENV_PYTHON):
        print(f"❌ Virtual environment Python not found: {VENV_PYTHON}")
        return False
    
    if not os.path.exists(ANALYSIS_SCRIPT):
        print(f"❌ Analysis script not found: {ANALYSIS_SCRIPT}")
        return False
    
    print(f"Using: {VENV_PYTHON}")
    print(f"Script: {ANALYSIS_SCRIPT}")
    
    # Change to project directory
    os.chdir(PROJECT_ROOT)
    
    try:
        # Run the script
        result = subprocess.run(
            [VENV_PYTHON, ANALYSIS_SCRIPT],
            capture_output=False,  # Let output go directly to console
            text=True
        )
        
        if result.returncode == 0:
            print("\n✅ Analysis completed successfully!")
            return True
        else:
            print(f"\n⚠ Analysis exited with code: {result.returncode}")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⏹ Analysis interrupted by user.")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main function with better error handling"""
    print("="*80)
    print("LAKE KARIBA WIND ANALYSIS LAUNCHER")
    print("="*80)
    
    # Show debug info
    debug_info()
    
    # Run simple test
    run_simple_test()
    
    # Check virtual environment
    if not check_virtual_environment_simple():
        print("\n" + "="*80)
        print("VIRTUAL ENVIRONMENT SETUP")
        print("="*80)
        
        print(f"\nVirtual environment not found at: {VENV_PATH}")
        print("\nTo create it:")
        print("1. cd /home/chawas/deployed")
        print("2. python3 -m venv deployed_env")
        print("3. source deployed_env/bin/activate")
        print("4. pip install xarray numpy pandas matplotlib cartopy")
        
        create = input("\nCreate virtual environment now? (y/n): ").lower()
        if create == 'y':
            try:
                print("\nCreating virtual environment...")
                subprocess.run(["python3", "-m", "venv", VENV_PATH], check=True)
                print(f"✓ Created: {VENV_PATH}")
                
                # Install packages
                print("\nInstalling packages...")
                packages = ["numpy", "xarray", "pandas", "matplotlib"]
                for pkg in packages:
                    subprocess.run([f"{VENV_PATH}/bin/pip", "install", pkg], check=True)
                    print(f"✓ Installed: {pkg}")
                    
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed: {e}")
                return 1
        else:
            print("\nCannot proceed without virtual environment.")
            return 1
    
    # Ask which method to use
    print("\n" + "="*80)
    print("SELECT RUN METHOD")
    print("="*80)
    print("1. Run directly (import module)")
    print("2. Run with virtual environment Python")
    print("3. Try both methods")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    success = False
    
    if choice == "1":
        success = run_analysis_directly()
    elif choice == "2":
        success = run_with_virtual_env()
    elif choice == "3":
        print("\nTrying method 1 (direct)...")
        success = run_analysis_directly()
        if not success:
            print("\nTrying method 2 (virtual env)...")
            success = run_with_virtual_env()
    else:
        print("Invalid choice. Defaulting to method 2.")
        success = run_with_virtual_env()
    
    print("\n" + "="*80)
    if success:
        print("✅ ANALYSIS COMPLETE!")
        print(f"\nOutputs are in: {os.path.join(PROJECT_ROOT, 'output')}")
        return 0
    else:
        print("❌ ANALYSIS FAILED")
        print("\nTroubleshooting steps:")
        print("1. Check virtual environment exists:", VENV_PATH)
        print("2. Check analysis script exists:", ANALYSIS_SCRIPT)
        print("3. Install packages: source deployed_env/bin/activate && pip install xarray numpy pandas")
        print("4. Check Python version: python3 --version")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹ Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error in launcher: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)