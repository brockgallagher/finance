import plaid
# from plaid import client
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from flask import jsonify
import os
from config import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV
from plaid.api import plaid_api

# Initialize the Plaid client
class PlaidClient:
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


def create_link_token():
    # Use a test client_user_id
    client_user_id = "test_user_123"
    client = PlaidClient()

    # Create a link_token for the given user
    request = LinkTokenCreateRequest(
            products=[Products("auth")],
            client_name="Plaid Test App",
            country_codes=[CountryCode('US')],
            redirect_uri='https://domainname.com/oauth-page.html',
            language='en',
            webhook='https://webhook.example.com',
            user=LinkTokenCreateRequestUser(
                client_user_id=client_user_id
            )
        )
    response = client.client.link_token_create(request)

    # Send the data to the client
    return jsonify(response.to_dict())



def main():
    test = create_link_token()
    print(test)