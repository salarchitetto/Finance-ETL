import pandas as pd
from configs import Configs
from AWS.s3 import S3


class Acorns:
    """

    """

    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def decompose_accounts(self):
        pass

    def decompose_transactions(self):
        pass

    def upload_acorns_data(self):
        pass

    def run_acorns_module(self):
        self.upload_acorns_data()
