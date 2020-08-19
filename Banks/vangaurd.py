import pandas as pd
from configs import Configs
from AWS.s3 import S3


class Vanguard:
    """
    Gathering and uploading Vanguard data.
    """
    # TODO: add a date column to the dataframe
    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def decompose_accounts(self):
        """
        Breaking down the accounts in Vanguard. For example this will give you something like :
        "IRA" or "Brokerage"
        :return: Datadframe
        """
        df = pd.DataFrame(self.plaid_client.accounts()["accounts"])[["subtype", "balances"]]
        df["balances"] = df.apply(lambda row: row.balances["current"], axis=1)

        return df

    def decompose_transactions(self):
        pass

    def upload_vanguard_data(self):
        """
        Pushing up the
        :return:
        """

        Configs.s3_helper_uploader("Vanguard", "accounts", self.decompose_accounts())

    def run_vanguard_module(self):
        self.upload_vanguard_data()


