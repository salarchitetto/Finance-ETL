from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os


class Selenium:
    """
    Clear cut functions for ChromeDriver Stuff
    """

    @staticmethod
    def driver():
        """
        Easily accessible webdriver to kick things off
        :return: ChromeDriver
        """

        return webdriver.Chrome(os.environ.get("WEB_DRIVER"))

    @staticmethod
    def on_click_class_name(driver, class_name):
        """
        Click on something given a css class name
        :param driver: Chrome driver
        :param class_name: the css class name
        :return: nothing
        """

        driver.find_element_by_class_name(class_name).click()

    @staticmethod
    def get_page_url(driver):
        """
        Return page url
        """

        return driver.current_url

    @staticmethod
    def get_page_source(driver):
        return driver.page_source

    @staticmethod
    def check_if_verify_identity(driver, to_check):
        try:
            return driver.find_element_by_id(to_check)
        except NoSuchElementException:
            try:
                return driver.find_element_by_class_name(to_check)
            except NoSuchElementException:
                try:
                    return driver.find_element_by_xpath(to_check)
                except NoSuchElementException:
                    return False
