import unittest
import os
from BeautifulReport import BeautifulReport
from HTMLTestRunnerNew import HTMLTestRunner
from interface_test.common.handle_logging import log
from interface_test.common.handle_path import CASE_DIR, REPORT_DIR

log.info("---------------开始执行测试用例-----------------------")

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTests(loader.discover(CASE_DIR))
# suite = unittest.defaultTestLoader.discover(CASE_DIR)

# bf = BeautifulReport(suite)
# bf.report(description="注册接口", filename="report.html", report_dir=REPORT_DIR)

runner = HTMLTestRunner(stream=open(os.path.join(REPORT_DIR, "report.html"), 'wb'), title="", description="", tester="")
runner.run(suite)
log.info("---------------测试用例执行完毕-----------------------\n\n\n\n\n")
