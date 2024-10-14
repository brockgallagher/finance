import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Plaid API credentials
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENV = os.getenv('PLAID_ENV', 'SANDBOX')  # Default to sandbox if not specified

# Other configuration variables can be added here

