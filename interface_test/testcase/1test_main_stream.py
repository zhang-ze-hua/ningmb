import unittest
import os
import random
from requests import request
from interface_test.library.myddt import ddt, data
from interface_test.common.handle_excel import HandleExcel
from interface_test.common.handle_path import DATA_DIR
from interface_test.common.handle_config import conf
from interface_test.common.handle_data import replace_data, EnvData
from interface_test.common.handle_db import HandleMysql
from interface_test.common.handle_logging import log


@ddt
class TestMainStream(unittest.TestCase):
    handle_excel = HandleExcel(os.path.join(DATA_DIR, conf.get("env", "filename")), "main_stream")
    cases_data, column = handle_excel.read_data()
    handle_mysql = HandleMysql()

    @data(*cases_data)
    def test_main_stream(self, case_data):
        case_id = case_data["case_id"]
        row = case_id + 1
        interface = case_data["interface"]
        title = case_data["title"]
        method = case_data["method"]
        url = case_data["url"]
        request_url = conf.get("env", "url") + replace_data(url)
        if interface == "register":
            setattr(EnvData, "mobilephone", self.random_phone())
        request_data = eval(replace_data(case_data["data"]))
        expected = eval(case_data["expected"])
        headers = eval(conf.get("env", "headers"))

        if interface not in ["register", "login", "loans"]:
            headers["Authorization"] = "Bearer " + getattr(EnvData, "token")

        response = request(method=method, url=request_url, json=request_data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)

        if interface == "login":
            setattr(EnvData, "member_id", str(res["data"]["id"]))
            setattr(EnvData, "token", res["data"]["token_info"]["token"])
        if interface == "add":
            setattr(EnvData, "loan_id", str(res["data"]["id"]))

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
