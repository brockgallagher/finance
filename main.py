import plaid
from plaid.api import plaid_api
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.account_type import AccountType
from plaid.model.account_subtype import AccountSubtype

# Initialize Plaid client
client = plaid_api.PlaidApi(plaid.Configuration(
    host=plaid.Environment.Sandbox, # Replace with Plaid's environment you're using
    api_key={'clientId': 'your_client_id', 'secret': 'your_secret'}
))

# Exchange the public token for an access token (you need to have this from link)
public_token = 'your_public_token'
exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
exchange_response = client.item_public_token_exchange(exchange_request)
access_token = exchange_response['access_token']

# Retrieve account balances
request = AccountsBalanceGetRequest(access_token=access_token)
response = client.accounts_balance_get(request)

# Access the current amount in an account (assuming first account)
accounts = response['accounts']
if accounts:
    account = accounts[0]
    print(f"Account Name: {account['name']}")
    print(f"Current Balance: {account['balances']['current']}")
else:
    print("No accounts found.")
