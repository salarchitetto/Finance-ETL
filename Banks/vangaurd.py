import pandas as pd
from Selenium.selenium import Selenium
from configs import Configs
from AWS.s3 import S3
import time
import os


class Vanguard:
    """

    """
    def __init__(self, driver, vanguard_link):
        self.driver = driver
        self.vanguard_link = vanguard_link

    def kick_off_vanguard(self):
        """

        :return:
        """
        self.driver.get(self.vanguard_link)
        time.sleep(Configs.TIME_TO_SLEEP)

    def vanguard_login(self):
        """

        :return:
        """

        self.driver.find_element_by_id("username") \
            .send_keys(Configs.creds_helper("VANGUARD_CREDS")["USERNAME"])

        self.driver.find_element_by_id("password") \
            .send_keys(Configs.creds_helper("VANGUARD_CREDS")["PASSWORD"])

        self.driver.find_element_by_css_selector("""#mainContent > 
        psx-my-accounts-page > section > div.row > div > section > form > 
        div.row.form-row.button-row.loginbutton-wrap > vui-button > button""").click()

        time.sleep(Configs.TIME_TO_SLEEP)

    def grab_ira_info(self):
        """

        :return:
        """

        vanguard_html = Selenium.get_page_source(self.driver)
        vanguard_df = pd.read_html(vanguard_html)[7]

        vanguard_df.columns = ["vanguard_account_type", "amount"]
        vanguard_df.drop(vanguard_df.tail(2).index, inplace=True)
        vanguard_df["date"] = Configs.TODAYS_DATE

        return vanguard_df

    def upload_vanguard_data(self):
        """

        :return:
        """

        s3 = S3(f"vanguard_accounts_{Configs.TODAYS_DATE}.parquet",
                Configs.creds_helper("BUCKET_NAME")["BUCKET"],
                Configs.creds_helper("AWS_KEYS")["ACCESS_KEY_ID"],
                Configs.creds_helper("AWS_KEYS")["AWS_SECRET"],
                "Vanguard",
                "accounts",
                self.grab_ira_info())

        print("Uploading data to s3")

        s3.upload_file()

    def vanguard_runner(self):
        self.kick_off_vanguard()
        self.vanguard_login()
        self.upload_vanguard_data()

