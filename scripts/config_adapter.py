#!/usr/bin/env python3
from config_manager import ConfigManager

def get_config(config_file=None):
    cm = ConfigManager(config_file)
    return cm.config
