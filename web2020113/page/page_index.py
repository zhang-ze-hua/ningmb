from web2020113.locator.locator_index import LocatorIndex as Loc


class IndexPage:
    def __init__(self, driver):
        self.driver = driver

    def get_my_user_info(self):
        """获取我的账户信息"""
        try:
            self.driver.find_element(*Loc.user_info)
        except:
            return '登录失败'
        else:
            return '登录成功'

    def click_quit(self):
        """点击退出登录"""
        self.driver.find_element(*Loc.quit_btn).click()

    def click_bid(self):
        """点击抢投标"""
        self.driver.find_element(*Loc.bid_btn_ele).click()
