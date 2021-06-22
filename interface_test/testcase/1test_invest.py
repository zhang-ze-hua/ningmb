import unittest
import os
from decimal import Decimal
from requests import request
from interface_test.library.myddt import ddt, data
from interface_test.common.handle_excel import HandleExcel
from interface_test.common.handle_path import DATA_DIR
from interface_test.common.handle_config import conf
from interface_test.common.handle_data import replace_data, EnvData
from interface_test.common.handle_db import HandleMysql
from interface_test.common.handle_logging import log


@ddt
class TestInvest(unittest.TestCase):
    handle_excel = HandleExcel(os.path.join(DATA_DIR, conf.get("env", "filename")), "invest")
    cases_data, column = handle_excel.read_data()
    handle_mysql = HandleMysql()

    @classmethod
    def setUpClass(cls):
        method = "post"
        url = conf.get("env", "url") + "/member/login"
        headers = eval(conf.get("env", "headers"))
        vip_data = {"mobile_phone": conf.get("test_data", "phone"), "pwd": conf.get("test_data", "pwd")}
        admin_data = {"mobile_phone": conf.get("test_data", "admin_phone"), "pwd": conf.get("test_data", "admin_pwd")}
        invest_data = {"mobile_phone": conf.get("test_data", "invest_phone"),
                       "pwd": conf.get("test_data", "invest_pwd")}
        vip_res = request(method=method, url=url, json=vip_data, headers=headers).json()
        cls.vip_token = "Bearer " + vip_res["data"]["token_info"]["token"]
        cls.vip_id = vip_res["data"]["id"]
        admin_res = request(method=method, url=url, json=admin_data, headers=headers).json()
        cls.admin_token = "Bearer " + admin_res["data"]["token_info"]["token"]
        invest_res = request(method=method, url=url, json=invest_data, headers=headers).json()
        cls.invest_token = "Bearer " + invest_res["data"]["token_info"]["token"]
        cls.invest_id = invest_res["data"]["id"]

    def setUp(self):
        add_method = "post"
        add_url = conf.get("env", "url") + "/loan/add"
        add_headers = eval(conf.get("env", "headers"))
        add_headers["Authorization"] = self.vip_token
        add_data = {"member_id": self.vip_id, "title": "借钱实现财富自由", "amount": 2000, "loan_rate": 10.0,
                    "loan_term": 12, "loan_date_type": 1, "bidding_days": 5}
        add_res = request(method=add_method, url=add_url, json=add_data, headers=add_headers).json()
        self.loan_id = add_res["data"]["id"]

        audit_method = "patch"
        audit_url = conf.get("env", "url") + "/loan/audit"
        audit_headers = eval(conf.get("env", "headers"))
        audit_headers["Authorization"] = self.admin_token
        audit_data = {"loan_id": self.loan_id, "approved_or_not": True}
        audit_res = request(method=audit_method, url=audit_url, json=audit_data, headers=audit_headers).json()
        print("项目审核返回：", audit_res)

    @data(*cases_data)
    def test_invest(self, case_data):
        case_id = case_data["case_id"]
        row = case_id + 1
        title = case_data["title"]
        method = case_data["method"]
        url = case_data["url"]
        request_url = conf.get("env", "url") + url
        if "#member_id#" in case_data["data"]:
            case_data["data"] = case_data["data"].replace("#member_id#", str(self.invest_id))
        if "#loan_id#" in case_data["data"]:
            case_data["data"] = case_data["data"].replace("#loan_id#", str(self.loan_id))
        request_data = eval(case_data["data"])
        expected = eval(case_data["expected"])
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = self.invest_token

        if case_data["check_sql"]:
            sql1 = "SELECT * FROM futureloan.member where id={}".format(self.invest_id)
            sql2 = "SELECT * FROM futureloan.invest WHERE member_id={} and loan_id={}".format(self.invest_id,
                                                                                              self.loan_id)
            sql3 = "SELECT * FROM futureloan.financelog WHERE pay_member_id={}".format(self.invest_id)
            # 获取开始的用户余额
            start_amount = self.handle_mysql.find_one(sql1)["leave_amount"]
            # 获取开始的投资记录条数
            start_invest = self.handle_mysql.find_count(sql2)
            # 获取用户开始的流水记录条数
            start_fin = self.handle_mysql.find_count(sql3)

        response = request(method=method, url=request_url, json=request_data, headers=headers)
        res = response.json()
        print("预期结果：", expected)
        print("实际结果：", res)

        try:
            self.assertEqual(res["code"], expected["code"])
            self.assertEqual(res["msg"], expected["msg"])
            if case_data["check_sql"]:
                sql1 = "SELECT * FROM futureloan.member where id={}".format(self.invest_id)
                sql2 = "SELECT * FROM futureloan.invest WHERE member_id={} and loan_id={}".format(self.invest_id,
                                                                                                  self.loan_id)
                sql3 = "SELECT * FROM futureloan.financelog WHERE pay_member_id={}".format(self.invest_id)
                # 获取投资后的用户余额
                end_amount = self.handle_mysql.find_one(sql1)["leave_amount"]
                self.assertEqual(start_amount - end_amount, Decimal(str(request_data["amount"])))
                # 获取投资后投资记录条数
                end_invest = self.handle_mysql.find_count(sql2)
                self.assertEqual(end_invest - start_invest, 1)
                # 获取用户投资后的流水记录条数
                end_fin = self.handle_mysql.find_count(sql3)
                self.assertEqual(end_fin - start_fin, 1)
                # 如果是满标的用例，再去校验该标的每一条投资记录有没有生成对应的回款计划表
                if "满标" in case_data["title"]:
                    # 获取当前标所有的投资记录id
                    sql4 = "SELECT id FROM futureloan.invest WHERE loan_id={}".format(self.loan_id)
                    invest_ids = self.handle_mysql.find_all(sql4)
                    # 遍历该标所有的投资记录的id
                    for invest in invest_ids:
                        sql5 = "SELECT * FROM futureloan.repayment WHERE invest_id={}".format(invest["id"])
                        # 获取当前这条投资记录，生成对应的回款计划
                        count = self.handle_mysql.find_count(sql5)
                        # 断言查询到的条数的布尔值是否为True(0的布尔值是False,只要不是0条，这个断言就会通过)
                        self.assertTrue(count)
        except AssertionError as e:
            log.error("用例--{}--执行未通过".format(title))
            log.debug("请求数据：{}".format(request_data))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.handle_excel.write_data(row=row, column=self.column, value="未通过")
            raise e
        else:
            log.info("用例--{}--执行通过".format(title))
            self.handle_excel.write_data(row=row, column=self.column, value="通过")

    @classmethod
    def tearDownClass(cls):
        cls.handle_mysql.close()
