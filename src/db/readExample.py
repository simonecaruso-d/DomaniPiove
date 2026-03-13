# Environment Setting
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import configuration.Configuration as Configuration
import db.ReadFromSupabase as SupabaseReader

# Run
print(SupabaseReader.SafeTableRead(Configuration.SupabaseUrl, Configuration.SupabaseKey, tableName='Calendar'))