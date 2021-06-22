from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium import webdriver
import time

desired_caps = {'platformName': 'Android',
                'platformVersion': '7.0',
                'deviceName': '2cd190db0903',
                'appPackage': 'com.tencent.mm',
                'appActivity': 'com.tencent.mm.ui.LauncherUI',
                'noReset': True,
                'automationName': 'UiAutomator2',
                'chromedriverExecutableDir': 'F:',
                'recreateChromeDriverSessions': True,
                'chromeOptions': {'androidProcess': 'com.tencent.mm:appbrand0'}
                }
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)

time.sleep(10)
# driver.find_element_by_id("com.lemon.lemonban:id/navigation_tiku").click()
# time.sleep(3)
# ele = driver.find_elements_by_android_uiautomator(
#     'new UiScrollable(new UiSelector().scrollable(true).instance(0)).'
#     'scrollIntoView(new UiSelector().textMatches("安全测试").instance(0))')


driver.find_element_by_xpath("//*[@text='发现']").click()
driver.find_element_by_xpath("//*[@text='小程序']").click()
time.sleep(5)
driver.find_element_by_xpath("//*[@text='寻味食都']").click()
time.sleep(10)
cons = driver.contexts
print("cons:", cons)
driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
hs = driver.window_handles
print("hs:", hs)
for handle in hs:
    driver.switch_to.window(handle)
    print("切换到窗口：", handle)
    # print(driver.page_source)
    if driver.page_source.find('首页') != -1:
        break
driver.find_element_by_xpath("//*[text()='我的']").click()
time.sleep(3)
hs2 = driver.window_handles
print("hs2:", hs2)
for handle in hs2:
    driver.switch_to.window(handle)
    print("切换到窗口2：", handle)
    print(driver.page_source)
    if driver.page_source.find('个人主页') != -1:
        break
driver.find_element_by_xpath("//*[text()='个人主页']").click()

time.sleep(5)
driver.quit()
