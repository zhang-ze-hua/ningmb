import pytest
from selenium import webdriver
from web2020113.common.handle_config import conf
from web2020113.page.page_login import LoginPage
from web2020113.page.page_index import IndexPage
from web2020113.page.page_invest import InvestPage
from web2020113.page.page_user import UserPage


# 用例级别的前置后置
# @pytest.fixture()
# def login_fixture():
#     driver = webdriver.Chrome()
#     page_login_driver = LoginPage(driver)
#     page_index_driver = IndexPage(driver)
#     yield page_login_driver, page_index_driver
#     driver.quit()

# 类级别的前置后置
@pytest.fixture(scope='class')
def login_fixture():
    driver = webdriver.Chrome()
    page_login_driver = LoginPage(driver)
    page_index_driver = IndexPage(driver)
    yield page_login_driver, page_index_driver
    driver.quit()


@pytest.fixture(scope='class')
def invest_fixture():
    # 前置条件
    driver = webdriver.Chrome()
    # 创建登录页面
    login_page = LoginPage(driver)
    # 登录
    login_page.login(user=conf.get('test_data', 'mobile'), pwd=conf.get('test_data', 'pwd'))
    # 创建首页对象
    index_page = IndexPage(driver)
    # 点击抢标
    js = "var q=document.documentElement.scrollTop=500"
    driver.execute_script(js)
    index_page.click_bid()
    driver.execute_script(js)
    # 创建投资页面
    invest_page = InvestPage(driver)
    # 创建个人信息页面
    user_page = UserPage(driver)
    yield invest_page, user_page
    # 后置条件
    driver.quit()

# 模块级别的前置后置
# @pytest.fixture(scope='module', autouse=True)
# def module_fixture():
#     print("======模块====qian zhi=============")
#     yield
#     print("======模块====hou zhi=============")


# 会话级别的前置后置
# @pytest.fixture(scope='session', autouse=True)
# def session_fixture():
#     print("======会话====qian zhi=============")
#     yield
#     print("======会话====hou zhi=============")
