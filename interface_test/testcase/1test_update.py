import unittest
import os
from requests import request
from interface_test.library.myddt import ddt, data
from interface_test.common.handle_config import conf
from interface_test.common.handle_excel import HandleExcel
from interface_test.common.handle_path import DATA_DIR
from interface_test.common.handle_db import HandleMysql
from interface_test.common.handle_logging import log
from interface_test.common.handle_data import replace_data, EnvData


@ddt
class TestUpdate(unittest.TestCase):
    handle_excel = HandleExcel(os.path.join(DATA_DIR, conf.get("env", "filename")), "update")
    cases_data, column = handle_excel.read_data()
    handle_mysql = HandleMysql()

    @data(*cases_data)
    def test_update(self, case_data):
        case_id = case_data["case_id"]
        row = case_id + 1
        interface = case_data["interface"]
        title = case_data["title"]
        method = case_data["method"]
        url = case_data["url"]
        request_url = conf.get("env", "url") + url
        data = case_data["data"]
        request_data = eval(replace_data(data))
        expected = eval(case_data["expected"])
        headers = eval(conf.get("env", "headers"))

        if interface == "update":
            headers["Authorization"] = "Bearer " + getattr(EnvData, "token")

        response = request(method=method, url=request_url, json=request_data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)

        if interface == "login":
            setattr(EnvData, "member_id", str(res["data"]["id"]))
            setattr(EnvData, "token", res["data"]["token_info"]["token"])
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
