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
