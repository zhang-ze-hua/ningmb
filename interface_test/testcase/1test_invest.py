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
        add_data = {"member_id": self.vip_id, "title": "????????????????????????", "amount": 2000, "loan_rate": 10.0,
                    "loan_term": 12, "loan_date_type": 1, "bidding_days": 5}
        add_res = request(method=add_method, url=add_url, json=add_data, headers=add_headers).json()
        self.loan_id = add_res["data"]["id"]

        audit_method = "patch"
        audit_url = conf.get("env", "url") + "/loan/audit"
        audit_headers = eval(conf.get("env", "headers"))
        audit_headers["Authorization"] = self.admin_token
        audit_data = {"loan_id": self.loan_id, "approved_or_not": True}
        audit_res = request(method=audit_method, url=audit_url, json=audit_data, headers=audit_headers).json()
        print("?????????????????????", audit_res)

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
            # ???????????????????????????
            start_amount = self.handle_mysql.find_one(sql1)["leave_amount"]
            # ?????????????????????????????????
            start_invest = self.handle_mysql.find_count(sql2)
            # ???????????????????????????????????????
            start_fin = self.handle_mysql.find_count(sql3)

        response = request(method=method, url=request_url, json=request_data, headers=headers)
        res = response.json()
        print("???????????????", expected)
        print("???????????????", res)

        try:
            self.assertEqual(res["code"], expected["code"])
            self.assertEqual(res["msg"], expected["msg"])
            if case_data["check_sql"]:
                sql1 = "SELECT * FROM futureloan.member where id={}".format(self.invest_id)
                sql2 = "SELECT * FROM futureloan.invest WHERE member_id={} and loan_id={}".format(self.invest_id,
                                                                                                  self.loan_id)
                sql3 = "SELECT * FROM futureloan.financelog WHERE pay_member_id={}".format(self.invest_id)
                # ??????????????????????????????
                end_amount = self.handle_mysql.find_one(sql1)["leave_amount"]
                self.assertEqual(start_amount - end_amount, Decimal(str(request_data["amount"])))
                # ?????????????????????????????????
                end_invest = self.handle_mysql.find_count(sql2)
                self.assertEqual(end_invest - start_invest, 1)
                # ??????????????????????????????????????????
                end_fin = self.handle_mysql.find_count(sql3)
                self.assertEqual(end_fin - start_fin, 1)
                # ????????????????????????????????????????????????????????????????????????????????????????????????????????????
                if "??????" in case_data["title"]:
                    # ????????????????????????????????????id
                    sql4 = "SELECT id FROM futureloan.invest WHERE loan_id={}".format(self.loan_id)
                    invest_ids = self.handle_mysql.find_all(sql4)
                    # ????????????????????????????????????id
                    for invest in invest_ids:
                        sql5 = "SELECT * FROM futureloan.repayment WHERE invest_id={}".format(invest["id"])
                        # ????????????????????????????????????????????????????????????
                        count = self.handle_mysql.find_count(sql5)
                        # ?????????????????????????????????????????????True(0???????????????False,????????????0??????????????????????????????)
                        self.assertTrue(count)
        except AssertionError as e:
            log.error("??????--{}--???????????????".format(title))
            log.debug("???????????????{}".format(request_data))
            log.debug("???????????????{}".format(expected))
            log.debug("???????????????{}".format(res))
            log.exception(e)
            self.handle_excel.write_data(row=row, column=self.column, value="?????????")
            raise e
        else:
            log.info("??????--{}--????????????".format(title))
            self.handle_excel.write_data(row=row, column=self.column, value="??????")

    @classmethod
    def tearDownClass(cls):
        cls.handle_mysql.close()
