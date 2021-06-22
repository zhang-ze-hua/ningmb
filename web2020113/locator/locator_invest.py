from selenium.webdriver.common.by import By


class LocatorInvest:
    """投资页面的元素定位"""
    # 投资金额输入框
    invest_amount_ele = (By.XPATH, "//input[@data-amount]")

    # 投资点击按钮
    invest_btn_ele = (By.XPATH, '//button[@class="btn btn-special height_style"]')

    # 投资成功的提示元素
    invest_success = (By.XPATH, '//div[text()="投标成功！"]')

    # 投资成功点击查看更多的方法
    click_success_info = (By.XPATH, '//div[@class="layui-layer-content"]//button[text()="查看并激活"]')

    # 投资失败，错误弹框提示信息
    invest_error_info = (By.XPATH, '//div[@class="text-center"]')
