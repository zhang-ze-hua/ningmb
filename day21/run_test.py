import unittest
from BeautifulReport import BeautifulReport
from day21.common.handle_path import REPORT_DIR, TESTCASE_DIR

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.discover(TESTCASE_DIR))

bf = BeautifulReport(suite)
bf.report("注册接口", "report.html", REPORT_DIR)
