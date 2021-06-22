import unittest
import os
from requests import request
from day21.library.myddt import ddt, data
from day21.common.handle_excel import HandleExcel
from day21.common.handle_logging import log
from day21.common.handle_config import conf
from day21.common.handle_path import DATA_DIR


@ddt
class LoginTestCase(unittest.TestCase):
    path = os.path.join(DATA_DIR, "apicases.xlsx")
    excel = HandleExcel(path, "login")
    cases = excel.read_data()

    @data(*cases)
    def test_login(self, case):
        # 准备数据
        method = case["method"]
        url = case["url"]
        data = eval(case["data"])
        expected = eval(case["expected"])
        headers = eval(conf.get("env", "headers"))
        row = case["case_id"] + 1
        # 实际结果
        response = request(method=method, url=url, json=data, headers=headers)
        res = response.json()
        # 断言
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
        except AssertionError as e:
            log.error("用例--{}--执行不通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            print("预期结果：{}".format(expected))
            print("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value="不通过")
            raise e
        else:
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")
