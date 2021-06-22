import unittest
import os
from requests import request
from interface_test.library.myddt import ddt, data
from interface_test.common.handle_config import conf
from interface_test.common.handle_excel import HandleExcel
from interface_test.common.handle_path import DATA_DIR
from interface_test.common.handle_db import HandleMysql
from interface_test.common.handle_logging import log


@ddt
class TestInfo(unittest.TestCase):
    handle_excel = HandleExcel(os.path.join(DATA_DIR, conf.get("env", "filename")), "info")
    cases_data, column = handle_excel.read_data()
    handle_mysql = HandleMysql()

    @classmethod
    def setUpClass(cls):
        method = "post"
        url = conf.get("env", "url") + "/member/login"
        headers = eval(conf.get("env", "headers"))
        vip_data = {"mobile_phone": conf.get("test_data", "phone"), "pwd": conf.get("test_data", "pwd")}
        vip_res = request(method=method, url=url, json=vip_data, headers=headers).json()
        cls.vip_token = "Bearer " + vip_res["data"]["token_info"]["token"]
        cls.vip_id = vip_res["data"]["id"]

    @data(*cases_data)
    def test_info(self, case_data):
        case_id = case_data["case_id"]
        row = case_id + 1
        title = case_data["title"]
        method = case_data["method"]
        url = case_data["url"]
        request_url = conf.get("env", "url") + url.replace("#member_id#", str(self.vip_id))
        expected = eval(case_data["expected"])
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = self.vip_token

        response = request(method=method, url=request_url, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)

        try:
            self.assertEqual(res["code"], expected["code"])
            self.assertEqual(res["msg"], expected["msg"])
        except AssertionError as e:
            log.error("用例--{}--执行未通过".format(title))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.handle_excel.write_data(row=row, column=self.column, value="未通过")
            raise e
        else:
            log.info("用例--{}--执行通过".format(title))
            self.handle_excel.write_data(row=row, column=self.column, value="通过")
