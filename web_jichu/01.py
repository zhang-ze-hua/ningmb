import time
import pytesseract
from PIL import Image, ImageEnhance
from selenium import webdriver

url = "https://www.xxxxx.com"
# 1.txt、打开浏览器，最大化浏览器
driver = webdriver.Chrome()
driver.get(url)
# driver.implicitly_wait(10)#隐式等待10s
driver.maximize_window()  # 最大化窗口

name = driver.find_element_by_id("username")  # 定位账号输入框
password = driver.find_element_by_id("password_1")  # 定位密码输入框
code1 = driver.find_element_by_id("user_ck")  # 定位验证码输入框

driver.save_screenshot("H://test/01.png")  # 截取屏幕内容，保存到本地

ran = Image.open("H://test/01.png")  # 打开截图，获取验证码位置，截取保存验证码
box = (564, 395, 643, 423)  # 获取验证码位置,自动定位不是很明白，就使用了手动定位，代表（左，上，右，下）
ran.crop(box).save("H://test/02.png")  # 把获取的验证码保存
# 获取验证码图片，读取验证码
imageCode = Image.open("H://test/02.png")  # 打开保存的验证码图片
# imageCode.load()
# 图像增强，二值化
sharp_img = ImageEnhance.Contrast(imageCode).enhance(2.0)
sharp_img.save("H://test/03.png")  # 保存图像增强，二值化之后的验证码图片
sharp_img.load()  # 对比度增强
time.sleep(2)
print(sharp_img)  # 打印图片的信息
code = pytesseract.image_to_string(sharp_img).strip()  # 读取验证码
# 5、收到验证码，进行输入验证
print(code)  # 输出验证码
name.send_keys('60037')  # 给定位账号的输入框中输入值
password.send_keys('123456')  # 给定位密码的输入框中输入值
code1.send_keys(code)  # 给定位验证码的输入框中输入读取到的验证码
click = driver.find_element_by_name("yt0").click()  # 点击登录
time.sleep(2)
# 关闭浏览器
driver.quit()
