#!/usr/bin/env python3
import re

with open('scripts/enhanced_wind_analysis.py', 'r') as f:
    lines = f.readlines()

# Find the __init__ method start
for i, line in enumerate(lines):
    if 'def __init__' in line and 'EnhancedWindAnalysis' in lines[i-2]:
        start_line = i
        break

# Find where __init__ ends (next method or class)
for j in range(start_line, len(lines)):
    if j > start_line and (lines[j].startswith('    def ') or lines[j].startswith('class ')):
        end_line = j
        break
else:
    end_line = len(lines)

print(f"Replacing lines {start_line+1} to {end_line+1}")

# Create new __init__ method
new_init = '''    def __init__(self, config_file=None):
        """Initialize enhanced wind analysis"""
        
        # Load configuration
        from config_adapter import get_config
        config_dict = get_config(config_file)
        self.config = config_dict
        
        # Setup logger - use module logger
        import logging
        self.logger = logging.getLogger(__name__)
        
        # Setup paths from config dict
        paths = config_dict.get('paths', {})
        self.project_dir = Path(paths.get('base_directory', '/home/chawas/deployed/charara'))
        
        # Extract analysis period
        analysis_period = config_dict.get('analysis_period', {})
        self.start_year = analysis_period.get('start_year', 2015)
        self.end_year = analysis_period.get('end_year', 2020)
        
        # Extract location
        location = config_dict.get('location', {})
        self.site_name = location.get('site_name', 'Charara Floating Solar Site')
        self.latitude = location.get('latitude', -16.53)
        self.longitude = location.get('longitude', 28.83)
        
        # Setup data paths
        data_paths = paths.get('data', {})
        self.wind_data_path = Path(data_paths.get('wind_data', 
            self.project_dir / 'data' / 'era5_downloads' / 'wind_data_2015_2020.nc'))
        self.era5_data_path = Path(data_paths.get('era5_data',
            self.project_dir / 'data' / 'era5_downloads' / 'era5_data.nc'))
        self.lake_shapefile_path = Path(data_paths.get('lake_shapefile',
            self.project_dir / 'data' / 'shapefiles' / 'lake_kariba.shp'))
        
        # Setup output directories
        output_paths = paths.get('output', {})
        self.output_base = Path(output_paths.get('base', self.project_dir / 'output'))
        self.output_maps = Path(output_paths.get('maps', self.output_base / 'wind_maps'))
        self.output_timeseries = Path(output_paths.get('timeseries', self.output_base / 'timeseries'))
        self.output_statistics = Path(output_paths.get('statistics', self.output_base / 'statistics'))
        self.output_reports = Path(output_paths.get('reports', self.output_base / 'reports'))
        
        # Create directories
        for directory in [self.output_maps, self.output_timeseries, 
                          self.output_statistics, self.output_reports]:
            directory.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"EnhancedWindAnalysis initialized for {self.site_name}")
        self.logger.info(f"Analysis period: {self.start_year}-{self.end_year}")
        self.logger.info(f"Output directory: {self.output_base}")
'''

# Replace the old __init__ method
lines[start_line:end_line] = [new_init + '\n']

# Write back
with open('scripts/enhanced_wind_analysis.py', 'w') as f:
    f.writelines(lines)

print("Fixed __init__ method")
