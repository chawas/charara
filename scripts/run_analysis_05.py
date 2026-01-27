#!/usr/bin/env python3
"""
Standalone wind analysis runner - No VS Code dependencies
"""

import sys
import os
import subprocess

# CRITICAL: Set matplotlib backend BEFORE anything else
os.environ['MPLBACKEND'] = 'Agg'
os.environ['DISPLAY'] = ''  # Empty display variable

def run_analysis():
    """Run the wind analysis using virtual environment"""
    
    # Define paths
    VENV_PYTHON = "/home/chawas/deployed/deployed_env/bin/python3"
    ANALYSIS_SCRIPT = "/home/chawas/deployed/charara/scripts/enhanced_wind_analysis.py"
    PROJECT_DIR = "/home/chawas/deployed/charara"
    
    print("="*80)
    print("LAKE KARIBA WIND ANALYSIS - STANDALONE RUNNER")
    print("="*80)
    
    # Check if files exist
    if not os.path.exists(VENV_PYTHON):
        print(f"❌ Virtual environment Python not found: {VENV_PYTHON}")
        print("\nCreate virtual environment:")
        print("cd /home/chawas/deployed")
        print("python3 -m venv deployed_env")
        return 1
    
    if not os.path.exists(ANALYSIS_SCRIPT):
        print(f"❌ Analysis script not found: {ANALYSIS_SCRIPT}")
        print("\nExpected at:", ANALYSIS_SCRIPT)
        return 1
    
    print(f"✅ Virtual environment: {VENV_PYTHON}")
    print(f"✅ Analysis script: {ANALYSIS_SCRIPT}")
    print(f"✅ Matplotlib backend: {os.environ.get('MPLBACKEND')}")
    
    # Change to project directory
    original_dir = os.getcwd()
    os.chdir(PROJECT_DIR)
    
    try:
        print("\n" + "="*80)
        print("STARTING ANALYSIS...")
        print("="*80)
        
        # Run the analysis script
        # Use Popen to get real-time output
        process = subprocess.Popen(
            [VENV_PYTHON, ANALYSIS_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Print output in real-time
        for line in process.stdout:
            print(line, end='')
        
        # Wait for process to complete
        process.wait()
        
        print("\n" + "="*80)
        
        if process.returncode == 0:
            print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
            print(f"\nOutputs are in: {PROJECT_DIR}/output")
            return 0
        else:
            print(f"❌ ANALYSIS FAILED WITH EXIT CODE: {process.returncode}")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏹ Analysis interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    # Make sure we're in the right directory
    os.chdir("/home/chawas/deployed/charara")
    sys.exit(run_analysis())