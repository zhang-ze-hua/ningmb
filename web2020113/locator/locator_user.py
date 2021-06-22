from selenium.webdriver.common.by import By


class LocatorUser:
    """用户页面的元素定位"""
    # 用户余额
    user_amount_ele = (By.XPATH, '//li[@class="color_sub"]')
    # 投标
    tender = (By.XPATH, '//a[text()="投标"]')
