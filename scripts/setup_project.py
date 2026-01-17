#!/usr/bin/env python3
"""
Setup script for wind analysis project
Creates directory structure and initial configuration
"""

import os
import json
from pathlib import Path

def setup_project():
    """Setup project directory structure"""
    
    # Base directory (update this to your path)
    base_dir = Path("/home/chawas/deployed/charara")
    
    # Directory structure
    dirs = [
        base_dir / "scripts",
        base_dir / "data" / "era5_downloads",
        base_dir / "data" / "shapefiles",
        base_dir / "output" / "wind_maps",
        base_dir / "output" / "timeseries",
        base_dir / "output" / "statistics",
        base_dir / "output" / "reports",
        base_dir / "templates",
        base_dir / "logs",
        base_dir / "config"
    ]
    
    # Create directories
    print("Creating directory structure...")
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {directory}")
    
    # Create default config file
    config_file = base_dir / "scripts" / "config.json"
    
    default_config = {
        "project": {
            "name": "Lake Kariba Floating Solar Wind Analysis",
            "version": "1.0"
        },
        "analysis_period": {
            "start_year": 2015,
            "end_year": 2020
        },
        "paths": {
            "base_directory": str(base_dir),
            "data": {
                "wind_data": str(base_dir / "data" / "era5_downloads" / "wind_data_2015_2020.nc"),
                "era5_data": str(base_dir / "data" / "era5_downloads" / "era5_data.nc"),
                "lake_shapefile": str(base_dir / "data" / "shapefiles" / "lake_kariba.shp")
            },
            "scripts": str(base_dir / "scripts"),
            "output": {
                "base": str(base_dir / "output"),
                "maps": str(base_dir / "output" / "wind_maps"),
                "timeseries": str(base_dir / "output" / "timeseries"),
                "statistics": str(base_dir / "output" / "statistics"),
                "reports": str(base_dir / "output" / "reports")
            },
            "templates": str(base_dir / "templates"),
            "logs": str(base_dir / "logs")
        },
        "location": {
            "site_name": "Charara Floating Solar Site",
            "latitude": -16.53,
            "longitude": 28.83
        }
    }
    
    with open(config_file, 'w') as f:
        json.dump(default_config, f, indent=2)
    
    print(f"\nDefault configuration created: {config_file}")
    print("\nPlease update the configuration with your actual file paths.")
    print("Then run: python enhanced_wind_analysis.py")


if __name__ == "__main__":
    setup_project()