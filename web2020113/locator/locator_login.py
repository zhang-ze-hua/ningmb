from selenium.webdriver.common.by import By


class LocatorLogin:
    # 账号输入框
    mobile_loc = (By.XPATH, '//input[@placeholder="手机号"]')
    # 密码输入框
    pwd_loc = (By.XPATH, '//input[@placeholder="密码"]')
    # 点击按钮
    login_loc = (By.XPATH, "//button[text()='登录']")
    # 失败的提示内容
    error_info = (By.XPATH, "//div[@class='form-error-info']")
    # 失败的弹框
    alert_error_info = (By.XPATH, '//div[@class="layui-layer-content"]')
    # 记住手机号选框
    re_mobile = (By.XPATH, '//input[@name="remember_me"]')
