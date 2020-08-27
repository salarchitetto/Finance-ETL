import pandas as pd
from configs import Configs


class Nelnet:

    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def decompose_accounts(self):
        """
        "This breaks down how much is my student loan balance... which hopefully hits zero
        relatively soon...
        :return: A dataframe with a total amount for the loans I stupidly took out at a very young age...
        """

        df = pd.DataFrame(self.plaid_client.accounts()["accounts"])[["name", "balances"]]
        df["balances"] = df.apply(lambda row: row.balances["available"], axis=1)
        df["date"] = Configs.TODAY

        return df.groupby(["name", "date"]).sum().reset_index() \
            .rename(columns={"name": "Nelnet Student Loan", "balances": "balance"}) \
            [["Nelnet Student Loan", "balance", "date"]]

    def upload_nelnet_balance(self):
        """
        Uploads this beautiful bit of data into an s3 bucket somewhere.. hopefully its mine..
        :return: Nothin
        """

        Configs.s3_helper_uploader("nelnet", "loan_balance", self.decompose_accounts())

    def run_nelnet_module(self):
        """
        Runs all of this beautiful code ;)
        :return: Nothin
        """

        self.upload_nelnet_balance()
# plaid_client = Plaid(Configs.creds_helper("NELNET")["ACCESS_KEY"], Configs.creds_helper("PLAID_API_KEYS")["CLIENT_ID"], Configs.creds_helper("PLAID_API_KEYS")["SECRET"], Configs.creds_helper("PLAID_API_KEYS")["PUBLIC_KEY"])
