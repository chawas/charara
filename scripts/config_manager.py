cd /home/chawas/deployed/charara

# Create a clean, working config_manager.py
cat > scripts/config_manager.py << 'EOF'
#!/usr/bin/env python3
"""
Configuration Manager for Kariba Wind Analysis
Provides both dictionary and object-like access to configuration
"""

import yaml
import logging
from pathlib import Path
import json
from datetime import datetime
import sys
import os

class ConfigManager:
    """Manages configuration for wind analysis project"""
    
    def __init__(self, config_file=None):
        """Initialize configuration manager"""
        
        # Setup logger first
        self.logger = self._setup_logger()
        
        # Set default config file if not provided
        if config_file is None:
            config_file = self._get_default_config_path()
        
        self.config_file = Path(config_file)
        
        # Load configuration
        self.config = self._load_config()
        
        # Setup paths
        self._setup_paths()
        
        # Create directories
        self._create_directories()
        
        self.logger.info(f"Configuration loaded from: {self.config_file}")
        self.logger.info(f"Project: {self.config['project']['name']}")
    
    def _setup_logger(self):
        """Setup logging configuration"""
        logger = logging.getLogger('config_manager')
        
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            ch.setFormatter(formatter)
            
            logger.addHandler(ch)
        
        return logger
    
    def _get_default_config_path(self):
        """Get default configuration file path"""
        # Try multiple possible locations
        possible_paths = [
            Path('config/kariba_config.yaml'),
            Path('../config/kariba_config.yaml'),
            Path('/home/chawas/deployed/charara/config/kariba_config.yaml'),
            Path(__file__).parent.parent / 'config' / 'kariba_config.yaml'
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # If no config file found, use first one and create default
        default_path = Path('config/kariba_config.yaml')
        default_path.parent.mkdir(parents=True, exist_ok=True)
        return default_path
    
    def _load_config(self):
        """Load configuration from YAML file"""
        
        # Default configuration
        default_config = {
            'project': {
                'name': 'Lake Kariba Floating Solar Wind Analysis',
                'version': '2.0',
                'description': 'Enhanced wind analysis for floating solar feasibility',
                'author': 'Wind Analysis Team',
                'created': datetime.now().strftime('%Y-%m-%d')
            },
            'analysis_period': {
                'start_year': 2015,
                'end_year': 2020,
                'years': [2015, 2016, 2017, 2018, 2019, 2020]
            },
            'location': {
                'site_name': 'Charara Floating Solar Site',
                'latitude': -16.53,
                'longitude': 28.83,
                'region': 'Lake Kariba, Zimbabwe-Zambia border',
                'elevation': 485  # meters above sea level
            },
            'wind_analysis': {
                'variables': ['u10', 'v10', 't2m', 'sp', 'd2m', 'blh'],
                'wind_speed_bins': [0, 2, 5, 8, 12, 20],
                'direction_bins': 16,
                'seasons': {
                    'summer': [12, 1, 2],
                    'autumn': [3, 4, 5],
                    'winter': [6, 7, 8],
                    'spring': [9, 10, 11]
                },
                'percentiles': [5, 25, 50, 75, 95, 99]
            },
            'era5': {
                'dataset': 'reanalysis-era5-single-levels',
                'variables': [
                    '10m_u_component_of_wind',
                    '10m_v_component_of_wind',
                    '2m_temperature',
                    'surface_pressure',
                    '2m_dewpoint_temperature',
                    'boundary_layer_height'
                ],
                'area': [-10.0, 26.0, -18.0, 30.0],  # North, West, South, East
                'grid_resolution': [0.25, 0.25],
                'time_step': 'hourly'
            },
            'paths': {
                'base_directory': '/home/chawas/deployed/charara',
                'data': {
                    'era5_raw': 'data/era5_raw',
                    'era5_processed': 'data/era5_processed',
                    'wind_data': 'data/wind_data.nc',
                    'lake_shapefile': 'data/shapefiles/lake_kariba.shp',
                    'topography': 'data/topography'
                },
                'output': {
                    'base': 'output',
                    'maps': 'output/maps',
                    'timeseries': 'output/timeseries',
                    'statistics': 'output/statistics',
                    'reports': 'output/reports',
                    'clustering': 'output/clustering',
                    'validation': 'output/validation'
                },
                'scripts': 'scripts',
                'templates': 'templates',
                'logs': 'logs'
            },
            'visualization': {
                'colormaps': {
                    'wind_speed': 'viridis',
                    'temperature': 'plasma',
                    'pressure': 'cividis',
                    'direction': 'hsv'
                },
                'figure_size': [12, 8],
                'dpi': 150,
                'font_size': 12,
                'style': 'seaborn-v0_8-darkgrid'
            },
            'clustering': {
                'n_clusters': 4,
                'features': ['wind_speed', 'wind_direction', 'temperature'],
                'algorithm': 'kmeans',
                'random_state': 42
            },
            'reporting': {
                'format': 'html',
                'include_sections': ['executive_summary', 'methodology', 'results', 'conclusions'],
                'generate_pdf': True,
                'email_report': False
            }
        }
        
        # Try to load user config
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    user_config = yaml.safe_load(f)
                
                if user_config:
                    # Merge with defaults (simple deep merge for top-level keys)
                    config = default_config.copy()
                    for key, value in user_config.items():
                        if key in config and isinstance(config[key], dict) and isinstance(value, dict):
                            config[key].update(value)
                        else:
                            config[key] = value
                    
                    self.logger.info(f"Loaded configuration from {self.config_file}")
                    return config
                else:
                    self.logger.warning(f"Config file is empty: {self.config_file}")
                    
            except Exception as e:
                self.logger.error(f"Error loading config file: {e}")
        
        # Save default config if file doesn't exist or is empty
        self._save_default_config(default_config)
        return default_config
    
    def _save_default_config(self, config):
        """Save default configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            self.logger.info(f"Created default configuration at: {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error saving default config: {e}")
    
    def _setup_paths(self):
        """Setup path attributes for easy access"""
        paths = self.config['paths']
        
        # Base directory
        self.base_dir = Path(paths['base_directory'])
        
        # Data paths
        data_paths = paths['data']
        self.data_dir = self.base_dir / 'data'
        self.era5_raw_dir = self.base_dir / data_paths['era5_raw']
        self.era5_processed_dir = self.base_dir / data_paths['era5_processed']
        self.wind_data_path = self.base_dir / data_paths['wind_data']
        self.lake_shapefile_path = self.base_dir / data_paths['lake_shapefile']
        
        # Output paths
        output_paths = paths['output']
        self.output_dir = self.base_dir / output_paths['base']
        self.maps_dir = self.base_dir / output_paths['maps']
        self.timeseries_dir = self.base_dir / output_paths['timeseries']
        self.statistics_dir = self.base_dir / output_paths['statistics']
        self.reports_dir = self.base_dir / output_paths['reports']
        self.clustering_dir = self.base_dir / output_paths['clustering']
        self.validation_dir = self.base_dir / output_paths['validation']
        
        # Other paths
        self.scripts_dir = self.base_dir / paths['scripts']
        self.templates_dir = self.base_dir / paths['templates']
        self.logs_dir = self.base_dir / paths['logs']
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            self.data_dir,
            self.era5_raw_dir,
            self.era5_processed_dir,
            self.output_dir,
            self.maps_dir,
            self.timeseries_dir,
            self.statistics_dir,
            self.reports_dir,
            self.clustering_dir,
            self.validation_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Created all necessary directories")
    
    # Convenience properties for easy access
    @property
    def project_name(self):
        return self.config['project']['name']
    
    @property
    def start_year(self):
        return self.config['analysis_period']['start_year']
    
    @property
    def end_year(self):
        return self.config['analysis_period']['end_year']
    
    @property
    def years(self):
        return list(range(self.start_year, self.end_year + 1))
    
    @property
    def site_name(self):
        return self.config['location']['site_name']
    
    @property
    def latitude(self):
        return self.config['location']['latitude']
    
    @property
    def longitude(self):
        return self.config['location']['longitude']
    
    @property
    def wind_variables(self):
        return self.config['wind_analysis']['variables']
    
    @property
    def era5_variables(self):
        return self.config['era5']['variables']
    
    def print_summary(self):
        """Print configuration summary"""
        print("="*70)
        print("CONFIGURATION SUMMARY")
        print("="*70)
        print(f"Project: {self.project_name}")
        print(f"Version: {self.config['project']['version']}")
        print(f"Analysis Period: {self.start_year} - {self.end_year}")
        print(f"Location: {self.site_name}")
        print(f"Coordinates: {self.latitude:.3f}°N, {self.longitude:.3f}°E")
        print(f"Base Directory: {self.base_dir}")
        print(f"Wind Variables: {', '.join(self.wind_variables)}")
        print(f"Output Directories:")
        print(f"  • Maps: {self.maps_dir}")
        print(f"  • Timeseries: {self.timeseries_dir}")
        print(f"  • Statistics: {self.statistics_dir}")
        print(f"  • Reports: {self.reports_dir}")
        print("="*70)
    
    def save_config_copy(self, output_path=None):
        """Save a copy of the current configuration"""
        if output_path is None:
            output_path = self.output_dir / 'config_backup.yaml'
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
        
        self.logger.info(f"Configuration backup saved to: {output_path}")
        return output_path
    
    def get(self, key, default=None):
        """Dict-like get method"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

# Convenience function for backward compatibility
def get_config(config_file=None):
    """
    Get configuration dictionary (for backward compatibility)
    
    Args:
        config_file: Path to config file (optional)
    
    Returns:
        dict: Configuration dictionary
    """
    cm = ConfigManager(config_file)
    return cm.config

# For direct execution
if __name__ == "__main__":
    # Test the config manager
    print("Testing ConfigManager...")
    cm = ConfigManager()
    cm.print_summary()
    
    # Test convenience function
    config = get_config()
    print(f"\nBackward compatibility test: config is {type(config).__name__}")
    print(f"Project name from dict: {config['project']['name']}")
EOF