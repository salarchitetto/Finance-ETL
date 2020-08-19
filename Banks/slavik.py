import pandas as pd
from configs import Configs
from AWS.s3 import S3


class Slavik:
    """
    Class to process Slavic401k data
    """

    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def decompose_accounts(self):
        """
        Breaking down the Slavik data
        :return: A Dataframe
        """

        df = pd.DataFrame(self.plaid_client.accounts()["accounts"])[["name", "balances"]]
        df["balances"] = df.apply(lambda row: row.balances["current"], axis=1)

        return df

    def decompose_transactions(self):
        pass

    def upload_slavik_data(self):
        """
        Uploading the data
        :return: None
        """

        Configs.s3_helper_uploader("Slavik", "accounts", self.decompose_accounts())

    def run_slavik_module(self):
        self.upload_slavik_data()
