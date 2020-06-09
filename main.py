from configs import Configs
from Selenium.selenium import Selenium
from Banks.pnc import PNC

driver = Selenium.driver()

if __name__ == '__main__':
    pnc = PNC(driver, Configs.PNC_LINK)
    pnc.pnc_runner()
    driver.close()

