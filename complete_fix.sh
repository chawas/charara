#!/bin/bash
cd /home/chawas/deployed/charara

echo "=== COMPLETE FIX FOR enhanced_wind_analysis.py ==="

# Backup
cp scripts/enhanced_wind_analysis.py scripts/enhanced_wind_analysis.py.backup3

# Create ConfigObject
cat > scripts/config_object.py << 'PYTHON'
from config_adapter import get_config as get_config_dict
import logging
from pathlib import Path

class ConfigObject:
    def __init__(self, config_dict=None):
        if config_dict is None:
            config_dict = get_config_dict()
        self._config = config_dict
        self.logger = logging.getLogger(__name__)
        self._setup_attributes()
    
    def _setup_attributes(self):
        """Set dictionary items as attributes"""
        paths = self._config.get('paths', {})
        self.base_directory = Path(paths.get('base_directory', '/home/chawas/deployed/charara'))
        
        # Data paths
        data_paths = paths.get('data', {})
        self.wind_data = data_paths.get('wind_data')
        self.era5_data = data_paths.get('era5_data')
        self.lake_shapefile = data_paths.get('lake_shapefile')
        
        # Analysis period
        analysis = self._config.get('analysis_period', {})
        self.start_year = analysis.get('start_year', 2015)
        self.end_year = analysis.get('end_year', 2020)
        
        # Location
        location = self._config.get('location', {})
        self.site_name = location.get('site_name', 'Charara')
        self.latitude = location.get('latitude', -16.53)
        self.longitude = location.get('longitude', 28.83)
    
    def print_summary(self):
        print("Config summary printed")
    
    # Dict-like access
    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def __getitem__(self, key):
        return self._config[key]

def get_config(config_file=None):
    """Main get_config function that returns ConfigObject"""
    config_dict = get_config_dict(config_file)
    return ConfigObject(config_dict)
PYTHON

# Update the import
sed -i 's/from config_adapter import get_config/from config_object import get_config/' scripts/enhanced_wind_analysis.py

# Also fix any remaining attribute accesses that expect dict
# Change self.config['key'] to self.config.get('key')
sed -i 's/self\.config\[/self.config.get(/g' scripts/enhanced_wind_analysis.py
sed -i "s/self\.config\[/self.config.get(/g" scripts/enhanced_wind_analysis.py

echo -e "\n✅ Fix applied!"
echo -e "\nTest the fix:"
python3 -c "
import sys
sys.path.append('scripts')
try:
    from config_object import get_config
    config = get_config()
    print(f'✓ ConfigObject created')
    print(f'  Type: {type(config)}')
    print(f'  Has logger: {hasattr(config, \"logger\")}')
    print(f'  base_directory: {config.base_directory}')
    print(f'  start_year: {config.start_year}')
except Exception as e:
    print(f'✗ Error: {e}')
    import traceback
    traceback.print_exc()
"
