import pandas as pd
from Selenium.selenium import Selenium
from configs import Configs
from AWS.s3 import S3
import time
import os


class CapitalOne:
    """

    """

    def __init__(self, driver, capital_link):
        self.driver = driver
        self.capital_link = capital_link

    def kick_off_capital(self):
        """

        :return:
        """

        self.driver.get(self.capital_link)
        time.sleep(Configs.TIME_TO_SLEEP)

    def capital_login(self):
        self.driver.find_element_by_id("noAcctUid") \
            .send_keys(Configs.creds_helper("CAPITAL_ONE")["USERNAME"])

        time.sleep(3)

        self.driver.find_element_by_id("noAcctPw") \
            .send_keys(Configs.creds_helper("CAPITAL_ONE")["PASSWORD"])

        time.sleep(3)

        self.driver.find_element_by_id("noAcctSubmit").click()

    def capital_runner(self):
        self.kick_off_capital()
        self.capital_login()
