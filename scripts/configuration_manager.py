#!/usr/bin/env python3
"""
Configuration Manager for Wind Analysis Project
Handles JSON configuration and path management
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import logging

class ConfigManager:
    """Manages configuration for wind analysis project"""
    
    def __init__(self, config_file=None):
        """Initialize configuration manager"""
        if config_file is None:
            # Default config file location
            script_dir = Path(__file__).parent
            config_file = script_dir / "config.json"
        
        self.config_file = Path(config_file)
        self.config = self.load_config()
        self.setup_directories()
        self.setup_logging()
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            print(f"✓ Configuration loaded from: {self.config_file}")
            return config
        except FileNotFoundError:
            print(f"✗ Configuration file not found: {self.config_file}")
            print("Creating default configuration...")
            return self.create_default_config()
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON: {e}")
            sys.exit(1)
    
    def create_default_config(self):
        """Create default configuration if file doesn't exist"""
        default_config = {
            "project": {
                "name": "Lake Kariba Wind Analysis",
                "version": "1.0"
            },
            "analysis_period": {
                "start_year": 2015,
                "end_year": 2020
            },
            "paths": {
                "base_directory": "/home/chawas/deployed/charara",
                "data": {
                    "wind_data": "",
                    "era5_data": ""
                },
                "output": {
                    "base": "/home/chawas/deployed/charara/output"
                }
            }
        }
        
        # Save default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print(f"✓ Default configuration created at: {self.config_file}")
        return default_config
    
    def setup_directories(self):
        """Create all necessary directories"""
        directories = [
            self.get_path("scripts"),
            self.get_path("output.base"),
            self.get_path("output.maps"),
            self.get_path("output.timeseries"),
            self.get_path("output.statistics"),
            self.get_path("output.reports"),
            self.get_path("logs"),
            self.get_path("templates")
        ]
        
        for directory in directories:
            if directory:  # Only create if path is specified
                os.makedirs(directory, exist_ok=True)
        
        print("✓ All directories created/verified")
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.get_path("logs")
        log_file = Path(log_dir) / f"wind_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=getattr(logging, self.get("debug.log_level", "INFO")),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Logging initialized. Log file: {log_file}")
    
    def get(self, key, default=None):
        """
        Get configuration value using dot notation
        Example: config.get("paths.output.base")
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_path(self, key):
        """
        Get path from config and ensure it's absolute
        """
        path_value = self.get(key)
        if not path_value:
            return None
        
        # If path is relative, make it absolute relative to base directory
        path = Path(path_value)
        if not path.is_absolute():
            base_dir = Path(self.get("paths.base_directory", "."))
            path = base_dir / path
        
        return str(path)
    
    def get_output_filename(self, base_name, extension="png", subdirectory=None):
        """
        Generate output filename with proper directory structure
        """
        # Get base output directory
        if subdirectory:
            output_dir = self.get_path(f"output.{subdirectory}")
        else:
            output_dir = self.get_path("output.base")
        
        # Create filename with year range
        year_range = f"{self.get('analysis_period.start_year')}_{self.get('analysis_period.end_year')}"
        filename = f"{base_name}_{year_range}.{extension}"
        
        return os.path.join(output_dir, filename)
    
    def update_analysis_period(self, start_year, end_year):
        """Update analysis period in config"""
        self.config['analysis_period']['start_year'] = start_year
        self.config['analysis_period']['end_year'] = end_year
        self.save_config()
    
    def save_config(self):
        """Save configuration back to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"✓ Configuration saved to: {self.config_file}")
    
    def print_summary(self):
        """Print configuration summary"""
        print("\n" + "="*60)
        print("CONFIGURATION SUMMARY")
        print("="*60)
        
        print(f"\nProject: {self.get('project.name')}")
        print(f"Version: {self.get('project.version')}")
        
        print(f"\nAnalysis Period: {self.get('analysis_period.start_year')}-{self.get('analysis_period.end_year')}")
        
        print(f"\nLocation:")
        print(f"  Site: {self.get('location.site_name')}")
        print(f"  Coordinates: {self.get('location.latitude')}°S, {self.get('location.longitude')}°E")
        
        print(f"\nPaths:")
        print(f"  Base Directory: {self.get_path('paths.base_directory')}")
        print(f"  Wind Data: {self.get_path('paths.data.wind_data')}")
        print(f"  Output Base: {self.get_path('paths.output.base')}")
        
        print(f"\nWind Thresholds:")
        thresholds = self.get('analysis_parameters.wind_speed_thresholds', {})
        for key, value in thresholds.items():
            print(f"  {key.replace('_', ' ').title()}: {value} m/s")
        
        print("="*60)

# Singleton instance for easy access
_config_manager = None

def get_config(config_file=None):
    """Get or create configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    return _config_manager