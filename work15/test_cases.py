import unittest
from work15.login_check import login_check
from work15.handle_excel import HandleExcel
from ddt import ddt, data

@ddt
class LoginTestCase(unittest.TestCase):
    excel = HandleExcel(r"C:\Users\Administrator\Desktop\cases.xlsx", "login")
    cases = excel.read_excel()

    @data(*cases)
    def test_login(self, case):
        # 准备数据
        data = eval(case["data"])
        expected = eval(case["expected"])
        row = case["id"] + 1
        # 实际结果
        res = login_check(*data)
        # 断言
        try:
            self.assertEqual(expected, res)
        except AssertionError as e:
            self.excel.write_excel(row=row, column=4, value="不通过")
            raise e
        else:
            self.excel.write_excel(row=row, column=4, value="通过")
