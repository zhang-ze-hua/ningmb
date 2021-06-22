from web2020113.locator.locator_login import LocatorLogin as Loc
from selenium.webdriver.chrome.webdriver import WebDriver
from web2020113.common.handle_config import conf
import time


class LoginPage:
    url = conf.get("env", "base_url") + conf.get("url", "login_url")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def login(self, user, pwd):
        """输入账号密码点击登录"""
        self.driver.find_element(*Loc.mobile_loc).send_keys(user)
        # 输入密码
        self.driver.find_element(*Loc.pwd_loc).send_keys(pwd)
        # 点击登录
        self.driver.find_element(*Loc.login_loc).click()

    def get_error_info(self):
        """获取登录失败的提示信息"""
        return self.driver.find_element(*Loc.error_info).text

    def get_alert_error_info(self):
        """获取页面弹窗的错误提示信息"""
        time.sleep(1)
        return self.driver.find_element(*Loc.alert_error_info).text

    def page_refresh(self):
        """刷新页面"""
        self.driver.get(url=self.url)

    def click_re_mobile(self):
        """取消记住手机号"""
        self.driver.find_element(*Loc.re_mobile).click()
