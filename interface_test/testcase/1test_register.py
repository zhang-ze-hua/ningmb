import unittest
import os
import random
from requests import request
from interface_test.library.myddt import ddt, data
from interface_test.common.handle_excel import HandleExcel
from interface_test.common.handle_path import DATA_DIR
from interface_test.common.handle_config import conf
from interface_test.common.handle_data import replace_data
from interface_test.common.handle_db import HandleMysql
from interface_test.common.handle_logging import log


@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, conf.get("env", "filename")), "register")
    cases_data, column = excel.read_data()
    handle_mysql = HandleMysql()

    @data(*cases_data)
    def test_register(self, case_data):
        case_id = case_data["case_id"]
        row = case_id + 1
        case_title = case_data["title"]
        case_method = case_data["method"]
        url = case_data["url"]
        case_url = conf.get("env", "url") + url
        expected = eval(case_data["expected"])
        headers = eval(conf.get("env", "headers"))
        headers["Connection"] = "close"

        if "#phone#" in case_data["data"]:
            phone = self.random_phone()
            case_data["data"] = case_data["data"].replace("#phone#", phone)
        data = eval(case_data["data"])

        response = request(method=case_method, url=case_url, json=data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)

        try:
            self.assertEqual(res["code"], expected["code"])
            self.assertEqual(res["msg"], expected["msg"])
            if case_data["check_sql"]:
                sql = case_data["check_sql"].replace("#phone#", phone)
                count = self.handle_mysql.find_count(sql)
                self.assertEqual(count, 1)
        except AssertionError as e:
            log.error("用例--{}--执行未通过".format(case_title))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_data(row=row, column=self.column, value="未通过")
            raise e
        else:
            log.info("用例--{}--执行通过".format(case_title))
            self.excel.write_data(row=row, column=self.column, value="通过")

    @classmethod
    def random_phone(cls):
        while True:
            phone1 = "138"
            phone2 = random.randint(00000000, 99999999)
            phone = phone1 + str(phone2)
            sql = "SELECT * FROM futureloan.member WHERE mobile_phone={}".format(phone)
            res = cls.handle_mysql.find_count(sql)
            if res == 0:
                return phone
