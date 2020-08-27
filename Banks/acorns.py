import pandas as pd
from configs import Configs


class Acorns:
    """
    Uploading Acorns Data
    """

    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def decompose_accounts(self):
        df = pd.DataFrame(self.plaid_client.accounts()["accounts"])[["subtype", "balances"]]
        df["balances"] = df.apply(lambda row: row.balances["current"], axis=1)
        df["date"] = Configs.TODAY

        return df

    def upload_acorns_data(self):
        Configs.s3_helper_uploader("Acorns", "accounts", self.decompose_accounts())

    def run_acorns_module(self):
        self.upload_acorns_data()
