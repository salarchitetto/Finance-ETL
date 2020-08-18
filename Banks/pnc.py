import pandas as pd
from Selenium.selenium import Selenium
from configs import Configs
from AWS.s3 import S3
import time
import os


class PNC:
    """
    A class which grabs PNC bank data given Plaids LINK functionality and returns
    your account balances and transactions for the past thirty days.
    ...

    Attributes
    __________
    plaid_client : Plaid Object
        Pass in the plaid class object from plaid.py
    """

    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def decompose_accounts(self):
        """
        Plaid returns a dictionary of information. For our purposes (accounts) all we want is the
        account name and the current available balance account.
        Then we grab the actual amount using a quick apply method.
        :return: A Dataframe
        """

        df = pd.DataFrame(self.plaid_client.accounts()["accounts"])[["name", "balances"]]
        df["available_balance"] = df.apply(lambda row: row.balances["available"], axis=1)
        return df[["name", "available_balance"]]

    def decompose_transactions(self):
        """
        Plaid returns a dictionary of information. For our purposes (transactions) all we want is the
        transactions name, the category (food, drink, debit, ETC), the amount the transaction was for,
        and the date.
        :return: A Dataframe
        """

        df = pd.DataFrame(self.plaid_client.transactions()["transactions"])[["name", "category", "amount", "date"]]
        # TODO: Come up with a better way to filter the below
        # df["category"] = df.apply(lambda row: row.category[0], axis=1)
        return df

    def upload_checking_savings(self):
        """
        Uploading plaid api account data into appropriate s3 bucket
        :return:
        """

        try:
            s3 = S3(f"checking_savings_{Configs.TODAY}.parquet",
                    Configs.creds_helper("BUCKET_NAME")["BUCKET"],
                    Configs.creds_helper("AWS_KEYS")["ACCESS_KEY_ID"],
                    Configs.creds_helper("AWS_KEYS")["AWS_SECRET"],
                    "PNC",
                    "checking_savings",
                    self.decompose_accounts())

            print("Uploading data to s3")

            s3.upload_file()

        except Exception as e:
            print("Something went wrong! : " + str(e))

    def upload_transactions(self):
        """
        Uploading plaid api transactions data into appropriate s3 bucket
        :return:
        """

        try:
            s3 = S3(f"checking_savings_{Configs.TODAY}.parquet",
                    Configs.creds_helper("BUCKET_NAME")["BUCKET"],
                    Configs.creds_helper("AWS_KEYS")["ACCESS_KEY_ID"],
                    Configs.creds_helper("AWS_KEYS")["AWS_SECRET"],
                    "PNC",
                    "transactions",
                    self.decompose_transactions())

            print("Uploading data to s3")

            s3.upload_file()

        except Exception as e:
            print("something went wrong! : " + str(e))

    def run_pnc_module(self):
        self.upload_checking_savings()
        self.upload_transactions()
