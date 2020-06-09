import pandas as pd
from Selenium.selenium import Selenium
from configs import Configs
from AWS.s3 import S3
import time
import os


class PNC:
    """
    PNC Class to kick off chrome browser and login to bank account.
    More stuff to come
    """

    def __init__(self, driver, pnc_link):
        self.driver = driver
        self.pnc_link = pnc_link

    def kick_off_pnc(self):
        """
        Start PNC task
        :return: none
        """

        self.driver.get(self.pnc_link)
        time.sleep(Configs.TIME_TO_SLEEP)

    def pnc_login(self):
        """
        Uses driver to enter login credentials and what not
        :return: none
        """

        Selenium.on_click_class_name(self.driver, "login-toggle")

        self.driver.find_element_by_id("userId") \
            .send_keys(Configs.creds_helper("PNC_CREDS")["USERNAME"])

        self.driver.find_element_by_id("passwordInputField") \
            .send_keys(Configs.creds_helper("PNC_CREDS")["PASSWORD"])

        self.driver.find_element_by_id("olb-btn").click()

        time.sleep(Configs.TIME_TO_SLEEP)

    def switch_frames_verify(self):
        """
        Checks to see if we need to verify ourselves and finishes the login process
        :return: none
        """
        if Selenium.check_if_verify_identity(self.driver, "/html/frameset/frame[1]") is not False:
            self.driver.switch_to.frame(self.driver.find_element_by_xpath("/html/frameset/frame[1]"))
            self.driver.find_element_by_name("answer").send_keys(os.environ.get("VERIFY_IDENTITY"))
            self.driver.find_element_by_class_name("formButton").click()
        else:
            pass

        time.sleep(Configs.TIME_TO_SLEEP)

    def grab_current_bank_amounts(self):
        """
        Scraper portion to obtain data from the pnc bank account
        :return: Dataframe with pnc bank information.
        """

        pnc_html = Selenium.get_page_source(self.driver)
        pnc_df = pd.read_html(pnc_html)[1].drop(columns=[1, 2])
        pnc_df.columns = ["bank_type", "amount"]
        pnc_df["date"] = Configs.TODAYS_DATE

        return pnc_df

    def upload_checking_savings(self):
        """
        Uploading the scraped data to designated s3 bucket
        :return:
        """

        s3 = S3(f"checking_savings_{Configs.TODAYS_DATE}.parquet",
                Configs.creds_helper("BUCKET_NAME")["BUCKET"],
                Configs.creds_helper("AWS_KEYS")["ACCESS_KEY_ID"],
                Configs.creds_helper("AWS_KEYS")["AWS_SECRET"],
                "PNC",
                "checking_savings",
                self.grab_current_bank_amounts())

        print("Uploading data to s3")

        s3.upload_file()

    def pnc_runner(self):
        """
        Kick starter to start the PNC process
        :return: nothing
        """

        self.kick_off_pnc()
        self.pnc_login()
        self.switch_frames_verify()
        self.upload_checking_savings()

