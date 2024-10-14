import plaid
from plaid.api import plaid_api
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from config import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV
import os
from public_token import PublicToken

class PlaidFinanceApp:
    def __init__(self):
        self.client = self._initialize_plaid_client()

    def _initialize_plaid_client(self):
        plaid_env = os.getenv('PLAID_ENV', 'SANDBOX').upper()
        
        environment_map = {
            'SANDBOX': plaid.Environment.Sandbox,
            # 'DEVELOPMENT': plaid.Environment.Development,
            'PRODUCTION': plaid.Environment.Production
        }
        
        if plaid_env not in environment_map:
            raise ValueError(f"Invalid PLAID_ENV: {plaid_env}")
        
        configuration = plaid.Configuration(
            host=environment_map[plaid_env],
            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SECRET')
            }
        )
        
        return plaid_api.PlaidApi(plaid.ApiClient(configuration))

    def exchange_public_token(self, public_token):
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = self.client.item_public_token_exchange(exchange_request)
        return exchange_response['access_token']

    def get_account_balances(self, access_token):
        request = AccountsBalanceGetRequest(access_token=access_token)
        response = self.client.accounts_balance_get(request)
        return response['accounts']

    def display_account_info(self, accounts):
        for account in accounts:
            print(f"Account Name: {account['name']}")
            print(f"Current Balance: ${account['balances']['current']:.2f}")
            print(f"Available Balance: ${account['balances'].get('available', 'N/A')}")
            print(f"Account Type: {account['type']}")
            print(f"Account Subtype: {account['subtype']}")
            print("-" * 40)

def main():
    app = PlaidFinanceApp()
    
    # Replace with the public token you receive from Plaid Link
    # public_token = 'your_public_token'
    public_token = PublicToken().public_token
    print(public_token)
    
    try:
        access_token = app.exchange_public_token(public_token)
        accounts = app.get_account_balances(access_token)
        
        if accounts:
            print("Your Financial Accounts:")
            app.display_account_info(accounts)
        else:
            print("No accounts found.")
    except plaid.ApiException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
