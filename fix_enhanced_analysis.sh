#!/bin/bash
cd /home/chawas/deployed/charara

echo "Fixing enhanced_wind_analysis.py..."

# Backup
cp scripts/enhanced_wind_analysis.py scripts/enhanced_wind_analysis.py.backup

# Create adapter
cat > scripts/config_adapter.py << 'ADAPTER'
#!/usr/bin/env python3
from config_manager import ConfigManager

def get_config(config_file=None):
    cm = ConfigManager(config_file)
    return cm.config
ADAPTER

# Fix import
sed -i 's/from config_manager import get_config/from config_adapter import get_config/' scripts/enhanced_wind_analysis.py

# Verify
echo -e "\nVerification:"
echo "Import line:"
grep "from config_adapter" scripts/enhanced_wind_analysis.py

echo -e "\nTest import:"
python3 -c "
import sys
sys.path.append('scripts')
try:
    from config_adapter import get_config
    config = get_config()
    print('✓ Config loaded successfully')
    print(f'  Site: {config.get(\"location\", {}).get(\"site_name\", \"N/A\")}')
except Exception as e:
    print(f'✗ Error: {e}')
"

echo -e "\n✅ Fix completed!"
