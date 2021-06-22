import time
from selenium.webdriver.chrome.webdriver import WebDriver
from web2020113.locator.locator_invest import LocatorInvest as Loc


class InvestPage:
    """投资页面"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_user_amount(self):
        """获取用户投资前的余额"""
        return self.driver.find_element(*Loc.invest_amount_ele).get_attribute('data-amount')

    def input_invest_money(self, money):
        """输入投资金额"""
        self.driver.find_element(*Loc.invest_amount_ele).send_keys(money)

    def click_invest(self):
        """点击投资"""
        self.driver.find_element(*Loc.invest_btn_ele).click()

    def get_invest_info(self):
        """获取投资成功提示信息"""
        time.sleep(1)
        return self.driver.find_element(*Loc.invest_success).text

    def click_invest_success(self):
        """点击投资成功更多信息"""
        time.sleep(1)
        self.driver.find_element(*Loc.click_success_info).click()

    def get_btn_error_info(self):
        """获取按钮上的提示信息"""
        return self.driver.find_element(*Loc.invest_btn_ele).text

    def get_window_error_info(self):
        """获取弹框的错误信息"""
        time.sleep(3)
        return self.driver.find_element(*Loc.invest_error_info).text

    def page_refresh(self):
        """刷新页面"""
        self.driver.refresh()

    def swipe_down(self, num):
        js = "var q=document.documentElement.scrollTop={}".format(num)
        self.driver.execute_script(js)
