# from HTMLTestRunnerNew import HTMLTestRunner
# import unittest
import pytest
import os
# suite = unittest.defaultTestLoader.discover(r"C:\Users\Administrator\PycharmProjects\ningmengban\web2020113\testcase")
# runner = HTMLTestRunner(stream=open('report.html', 'wb'), title="first test report")
# runner.run(suite)

pytest.main()
# pytest.main(["-m slow", "--alluredir=allure_report"])

# os.system("allure serve allure_report")
