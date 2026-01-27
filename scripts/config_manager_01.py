#!/usr/bin/env python3
"""
Configuration Manager for Wind Analysis Project
Fixed version with better error handling
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
        self.logger = self.setup_logging()
        
        if config_file is None:
            # Default config file location
            script_dir = Path(__file__).parent
            config_file = script_dir / "config.json"
        
        self.config_file = Path(config_file)
        self.config = self.load_config()
        self.setup_directories()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if not self.config_file.exists():
                self.logger.error(f"Config file not found: {self.config_file}")
                return self.create_default_config()
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            self.logger.info(f"Configuration loaded from: {self.config_file}")
            return config
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON: {e}")
            return self.create_default_config()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration if file doesn't exist"""
        default_config = {
            "project": {
                "name": "Lake Kariba Wind Analysis",
                "version": "1.0.0",
                "description": "Wind analysis for floating solar panels at Lake Kariba"
            },
            "analysis_period": {
                "start_year": 2015,
                "end_year": 2020
            },
            "paths": {
                "base_directory": "/home/chawas/deployed/charara",
                "data": {
                    "wind_data": "/home/chawas/deployed/charara/data/era5_downloads/wind_data.nc",
                    "era5_data": "/home/chawas/deployed/charara/data/era5_downloads/era5_data.nc"
                },
                "scripts": "/home/chawas/deployed/charara/scripts",
                "output": {
                    "base": "/home/chawas/deployed/charara/output",
                    "maps": "/home/chawas/deployed/charara/output/wind_maps",
                    "timeseries": "/home/chawas/deployed/charara/output/timeseries",
                    "statistics": "/home/chawas/deployed/charara/output/statistics",
                    "reports": "/home/chawas/deployed/charara/output/reports"
                },
                "templates": "/home/chawas/deployed/charara/templates",
                "logs": "/home/chawas/deployed/charara/logs"
            },
            "location": {
                "site_name": "Charara Floating Solar Site",
                "latitude": -16.53,
                "longitude": 28.83,
                "description": "Northeastern Lake Kariba, Zimbabwe"
            },
            "analysis_parameters": {
                "wind_speed_thresholds": {
                    "normal_operation": 8.0,
                    "caution": 12.0,
                    "danger": 15.0,
                    "emergency_shutdown": 18.0
                },
                "map_extent": {
                    "min_lon": 26.5,
                    "max_lon": 29.5,
                    "min_lat": -18.0,
                    "max_lat": -16.0
                },
                "charara_highlight_radius": 0.2,
                "wind_speed_range": [0, 10]
            },
            "plotting": {
                "figure_size": [16, 12],
                "dpi": 300,
                "font_size": {
                    "title": 16,
                    "axis": 12,
                    "legend": 10,
                    "annotation": 9
                }
            }
        }
        
        # Save default config
        try:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            self.logger.info(f"Default configuration created at: {self.config_file}")
        except Exception as e:
            self.logger.error(f"Could not save default config: {e}")
        
        return default_config
    
    def setup_directories(self):
        """Create all necessary directories with error handling"""
        directories = []
        
        # Get directories from config
        base_dir = self.get("paths.base_directory")
        if base_dir:
            directories.append(base_dir)
        
        # Add output directories
        output_base = self.get("paths.output.base")
        if output_base:
            directories.extend([
                output_base,
                self.get_path("output.maps"),
                self.get_path("output.timeseries"),
                self.get_path("output.statistics"),
                self.get_path("output.reports")
            ])
        
        # Add other directories
        other_dirs = [
            self.get_path("scripts"),
            self.get_path("logs"),
            self.get_path("templates")
        ]
        
        directories.extend([d for d in other_dirs if d])
        
        # Create directories
        for directory in directories:
            if directory and isinstance(directory, (str, Path)):
                try:
                    os.makedirs(directory, exist_ok=True)
                    self.logger.debug(f"Created/verified directory: {directory}")
                except Exception as e:
                    self.logger.error(f"Error creating directory {directory}: {e}")
            else:
                self.logger.warning(f"Skipping invalid directory path: {directory}")
        
        self.logger.info("Directories setup complete")
    
    def get(self, key, default=None):
        """
        Get configuration value using dot notation
        Example: config.get("paths.output.base")
        """
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
        except Exception as e:
            self.logger.debug(f"Error getting key '{key}': {e}")
            return default
    
    def get_path(self, key):
        """
        Get path from config and ensure it's absolute
        Returns None if path is invalid or not found
        """
        try:
            path_value = self.get(key)
            if not path_value:
                self.logger.debug(f"Path key '{key}' returned None or empty")
                return None
            
            # Convert to Path object
            path = Path(str(path_value))
            
            # If path is relative, make it absolute relative to base directory
            if not path.is_absolute():
                base_dir = self.get("paths.base_directory")
                if base_dir:
                    path = Path(base_dir) / path
                else:
                    self.logger.warning(f"Cannot make path absolute, no base directory: {key}")
            
            return str(path)
            
        except Exception as e:
            self.logger.error(f"Error getting path for key '{key}': {e}")
            return None
    
    def get_output_filename(self, base_name, extension="png", subdirectory=None):
        """
        Generate output filename with proper directory structure
        """
        try:
            # Get base output directory
            if subdirectory:
                output_dir = self.get_path(f"output.{subdirectory}")
            else:
                output_dir = self.get_path("output.base")
            
            if not output_dir:
                self.logger.error(f"Cannot get output directory for {subdirectory}")
                return None
            
            # Create filename with year range
            start_year = self.get("analysis_period.start_year", "")
            end_year = self.get("analysis_period.end_year", "")
            year_range = f"{start_year}_{end_year}" if start_year and end_year else ""
            
            if year_range:
                filename = f"{base_name}_{year_range}.{extension}"
            else:
                filename = f"{base_name}.{extension}"
            
            full_path = os.path.join(output_dir, filename)
            return full_path
            
        except Exception as e:
            self.logger.error(f"Error generating output filename: {e}")
            return None
    
    def update_analysis_period(self, start_year, end_year):
        """Update analysis period in config"""
        if "analysis_period" not in self.config:
            self.config["analysis_period"] = {}
        
        self.config["analysis_period"]["start_year"] = start_year
        self.config["analysis_period"]["end_year"] = end_year
        self.save_config()
    
    def save_config(self):
        """Save configuration back to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.info(f"Configuration saved to: {self.config_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False
    
    def print_summary(self):
        """Print configuration summary"""
        print("\n" + "="*60)
        print("CONFIGURATION SUMMARY")
        print("="*60)
        
        print(f"\nProject: {self.get('project.name', 'N/A')}")
        print(f"Version: {self.get('project.version', 'N/A')}")
        
        print(f"\nAnalysis Period: {self.get('analysis_period.start_year', 'N/A')}-{self.get('analysis_period.end_year', 'N/A')}")
        
        print(f"\nLocation:")
        print(f"  Site: {self.get('location.site_name', 'N/A')}")
        print(f"  Coordinates: {self.get('location.latitude', 'N/A')}°S, {self.get('location.longitude', 'N/A')}°E")
        
        print(f"\nPaths:")
        print(f"  Base Directory: {self.get_path('paths.base_directory')}")
        
        wind_data = self.get_path('paths.data.wind_data')
        print(f"  Wind Data: {wind_data if wind_data else 'Not specified'}")
        
        output_base = self.get_path('output.base')
        print(f"  Output Base: {output_base if output_base else 'Not specified'}")
        
        print(f"\nWind Thresholds:")
        thresholds = self.get('analysis_parameters.wind_speed_thresholds', {})
        for key, value in thresholds.items():
            print(f"  {key.replace('_', ' ').title()}: {value} m/s")
        
        print("="*60)
    
    def validate(self):
        """Validate configuration"""
        errors = []
        
        # Check required fields
        required = [
            "project.name",
            "analysis_period.start_year",
            "analysis_period.end_year",
            "location.latitude",
            "location.longitude"
        ]
        
        for field in required:
            if not self.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Check that paths are valid
        path_fields = [
            "paths.base_directory",
            "output.base"
        ]
        
        for field in path_fields:
            path = self.get_path(field)
            if not path:
                errors.append(f"Invalid or missing path: {field}")
        
        if errors:
            self.logger.error("Configuration validation failed:")
            for error in errors:
                self.logger.error(f"  - {error}")
            return False
        
        self.logger.info("Configuration validation passed")
        return True


# Test if run directly
if __name__ == "__main__":
    print("="*80)
    print("CONFIG MANAGER TEST")
    print("="*80)
    
    try:
        # Initialize config manager
        config = ConfigManager()
        print("✅ ConfigManager initialized successfully")
        
        # Print summary
        config.print_summary()
        
        # Validate config
        if config.validate():
            print("\n✅ Configuration is valid")
        else:
            print("\n⚠ Configuration has issues")
        
        # Test path resolution
        print("\n" + "="*80)
        print("PATH RESOLUTION TEST")
        print("="*80)
        
        test_paths = [
            "paths.base_directory",
            "paths.data.wind_data",
            "output.base",
            "output.maps"
        ]
        
        for path_key in test_paths:
            resolved = config.get_path(path_key)
            print(f"{path_key:30} -> {resolved if resolved else 'NOT FOUND'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)