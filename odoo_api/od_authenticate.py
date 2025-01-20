import xmlrpc.client
import os
import sys
# Import sensitive variables from config.py

# Add the root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from odoo_config import ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD

# Authenticate with Odoo
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
if uid:
    print(f"Authenticated successfully! User ID: {uid}")
else:
    print("Authentication failed. Check your credentials.")
