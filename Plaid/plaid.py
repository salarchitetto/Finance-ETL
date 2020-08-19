from plaid import Client
from configs import Configs


class Plaid:
    """
    A Class which wraps around the Plaid API
    To get API access visit https://plaid.com/ -> 'Get API keys'
    ...

    Attributes
    __________
    access_key : str
        the access key obtained from Plaids LINK service in order to retrieve data from said bank
    client_id : str
        Plaid API client id
    secret : str
        Plaid API secret
    public_key : str
        Plaid API public key
    """

    def __init__(self, access_key, client_id, secret, public_key):
        self.access_key = access_key
        self.client_id = client_id
        self.secret = secret
        self.public_key = public_key

    def client(self):
        return Client(client_id=self.client_id, secret=self.secret,
                      public_key=self.public_key, environment="development")

    def accounts(self):
        return self.client().Accounts.get(self.access_key)

    def transactions(self):
        return self.client().Transactions.get(self.access_key, Configs.START_DATE, Configs.END_DATE)
