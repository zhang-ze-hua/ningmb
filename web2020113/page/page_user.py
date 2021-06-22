from selenium.webdriver.chrome.webdriver import WebDriver
from web2020113.locator.locator_user import LocatorUser as Loc


class UserPage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_user_amount(self):
        """获取用户的余额"""
        amount = self.driver.find_element(*Loc.user_amount_ele).text
        amount = amount.replace('元', '')
        return amount

    def click_tender(self):
        """获取用户的余额"""
        self.driver.find_element(*Loc.tender).click()
