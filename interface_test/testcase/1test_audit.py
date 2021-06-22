import unittest
import os
from requests import request
from interface_test.library.myddt import ddt, data
from interface_test.common.handle_excel import HandleExcel
from interface_test.common.handle_path import DATA_DIR
from interface_test.common.handle_config import conf
from interface_test.common.handle_data import replace_data, EnvData
from interface_test.common.handle_db import HandleMysql
from interface_test.common.handle_logging import log


@ddt
class TestAudit(unittest.TestCase):
    handle_excel = HandleExcel(os.path.join(DATA_DIR, conf.get("env", "filename")), "audit")
    cases_data, column = handle_excel.read_data()
    handle_mysql = HandleMysql()

    @classmethod
    def setUpClass(cls):
        method = "post"
        url = conf.get("env", "url") + "/member/login"
        headers = eval(conf.get("env", "headers"))
        vip_data = {"mobile_phone": conf.get("test_data", "phone"), "pwd": conf.get("test_data", "pwd")}
        admin_data = {"mobile_phone": conf.get("test_data", "admin_phone"), "pwd": conf.get("test_data", "admin_pwd")}
        vip_res = request(method=method, url=url, json=vip_data, headers=headers).json()
        cls.vip_token = "Bearer " + vip_res["data"]["token_info"]["token"]
        cls.vip_id = vip_res["data"]["id"]
        admin_res = request(method=method, url=url, json=admin_data, headers=headers).json()
        cls.admin_token = "Bearer " + admin_res["data"]["token_info"]["token"]

    def setUp(self):
        method = "post"
        url = conf.get("env", "url") + "/loan/add"
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = self.vip_token
        loan_data = {"member_id": self.vip_id, "title": "借钱实现财富自由", "amount": 2000, "loan_rate": 10.0,
                     "loan_term": 12, "loan_date_type": 1, "bidding_days": 5}
        res = request(method=method, url=url, json=loan_data, headers=headers).json()
        # self.loan_id = res["data"]["id"]
        setattr(EnvData, "loan_id", str(res["data"]["id"]))

    @data(*cases_data)
    def test_audit(self, case_data):
        case_id = case_data["case_id"]
        row = case_id + 1
        title = case_data["title"]
        method = case_data["method"]
        url = case_data["url"]
        request_url = conf.get("env", "url") + url
        data = case_data["data"]
        request_data = eval(replace_data(data))
        expected = eval(case_data["expected"])
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = self.admin_token

        response = request(method=method, url=request_url, json=request_data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)

        if title == "审核通过" and res["code"] == 0:
            setattr(EnvData, "pass_loan_id", str(request_data["loan_id"]))

        try:
            self.assertEqual(res["code"], expected["code"])
            self.assertEqual(res["msg"], expected["msg"])
            if case_data["check_sql"]:
                sql = replace_data(case_data["check_sql"])
                status = self.handle_mysql.find_one(sql)["status"]
                self.assertEqual(expected["status"], status)
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
