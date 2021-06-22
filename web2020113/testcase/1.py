import unittest
import time
from selenium import webdriver
from ddt import ddt, data
from web2020113.page.page_login import LoginPage
from web2020113.page.page_index import IndexPage
from web2020113.data.data_login import DataLogin


@ddt
class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.page_login_driver = LoginPage(self.driver)
        self.page_index_driver = IndexPage(self.driver)

    def test_login_pass(self):
        self.page_login_driver.login(18684720553, "python")
        res = self.page_index_driver.get_info()
        self.assertEqual(res, "登录成功")

    @data(*DataLogin.error_case)
    def test_login_error(self, case):
        self.page_login_driver.login(case["mobile"], case["pwd"])
        res = self.page_login_driver.login_error_info()
        self.assertEqual(res, case["expected"])

    def tearDown(self):
        self.driver.quit()
