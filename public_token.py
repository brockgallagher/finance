import plaid
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.api import plaid_api
import os

class PublicToken:
    def __init__(self):
        self.public_token = self.create_public_token()


    def create_client(self):

        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,

            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SECRET'),
                'plaidVersion': '2020-09-14'
            }
        )
        api_client = plaid.ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)
        return client

    def create_request(self):
        # Create the request
        request = SandboxPublicTokenCreateRequest(
            institution_id="ins_109508",  # 'Plaid Bank' institution ID for sandbox
            initial_products=[Products('transactions')],
        )
        return request

    def create_response(self):
        # Use the client to create a public token
        client = self.create_client()
        request = self.create_request()
        response = client.sandbox_public_token_create(request)
        return response

    def create_public_token(self):
        response = self.create_response()
        public_token = response['public_token']
        return public_token

