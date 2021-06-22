import unittest
from BeautifulReport import BeautifulReport


suit = unittest.defaultTestLoader.discover(r"C:\Users\Administrator\PycharmProjects\ningmengban\work15")
br = BeautifulReport(suit)
br.report("登录测试报告", "login_test.html")