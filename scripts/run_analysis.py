#!/usr/bin/env python3
"""
Simple script to run wind analysis
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from enhanced_wind_analysis import main
    print("="*80)
    print("RUNNING WIND ANALYSIS FOR LAKE KARIBA")
    print("="*80)
    
    # Run main analysis
    analyzer, results = main()
    
except ImportError as e:
    print(f"Import error: {e}")
    print("\nPlease ensure all required packages are installed:")
    print("pip install numpy xarray matplotlib cartopy geopandas pandas scipy")
    
except Exception as e:
    print(f"Error running analysis: {e}")
    import traceback
    traceback.print_exc()