#!/usr/bin/env python3
"""
Run analysis from terminal - no VS Code debugger
"""

import subprocess
import sys
import os

def main():
    print("="*80)
    print("LAKE KARIBA WIND ANALYSIS - TERMINAL LAUNCHER")
    print("="*80)
    
    # Set up paths
    venv_python = "/home/chawas/deployed/deployed_env/bin/python3"
    analysis_script = "/home/chawas/deployed/charara/scripts/enhanced_wind_analysis.py"
    
    # Check if files exist
    if not os.path.exists(venv_python):
        print(f"❌ Virtual environment not found: {venv_python}")
        return 1
    
    if not os.path.exists(analysis_script):
        print(f"❌ Analysis script not found: {analysis_script}")
        return 1
    
    print(f"✅ Using: {venv_python}")
    print(f"✅ Script: {analysis_script}")
    
    # Set environment variables for matplotlib
    env = os.environ.copy()
    env['MPLBACKEND'] = 'Agg'
    env['DISPLAY'] = ''
    
    # Change to project directory
    os.chdir("/home/chawas/deployed/charara")
    
    print("\n" + "="*80)
    print("STARTING ANALYSIS...")
    print("="*80)
    
    try:
        # Run the script
        result = subprocess.run(
            [venv_python, analysis_script],
            env=env,
            capture_output=False,  # Show output directly
            text=True
        )
        
        print("\n" + "="*80)
        
        if result.returncode == 0:
            print("✅ ANALYSIS COMPLETED!")
            return 0
        else:
            print(f"❌ ANALYSIS FAILED (code: {result.returncode})")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏹ Interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())