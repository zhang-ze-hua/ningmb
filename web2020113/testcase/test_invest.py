import time
import pytest
from web2020113.common.handle_logging import log
from web2020113.data.data_invest import DataInvest


class TestInvest:
    @pytest.mark.parametrize("case", DataInvest.success_case_data)
    def test_invest_pass(self, case, invest_fixture):
        """投资成功的用例"""
        invest_page, user_page = invest_fixture
        # 获取用户投资前的余额
        account_money1 = invest_page.get_user_amount()
        # 输入投资金额
        invest_page.input_invest_money(case["money"])
        # 点击投标
        invest_page.click_invest()
        # 获取投资成功提示信息
        res = invest_page.get_invest_info()
        # 期望的提示信息
        expected = case["expected"]
        # 点击查看并激活
        invest_page.click_invest_success()
        # 获取用户投资后的余额
        time.sleep(10)
        account_money2 = user_page.get_user_amount()
        try:
            assert expected == res
            assert float(account_money1) - float(account_money2) == float(case["money"])
        except AssertionError as e:
            log.error("用例--{}---执行未通过".format(expected))
            log.exception(e)
            raise e
        else:
            log.info("用例--{}---执行通过".format(expected))
            user_page.click_tender()
            invest_page.swipe_down(300)

    @pytest.mark.slow
    @pytest.mark.parametrize("case", DataInvest.error_case_data)
    def test_invest_error(self, case, invest_fixture):
        """投资失败，按钮上出现提示的用例"""
        invest_page, user_page = invest_fixture
        # 刷新投资页面
        invest_page.page_refresh()
        # 输入投资金额
        invest_page.input_invest_money(case["money"])
        expected = case["expected"]
        # 获取按钮的提示信息
        res = invest_page.get_btn_error_info()
        try:
            assert expected == res
        except AssertionError as e:
            log.error("用例--{}---执行未通过".format(expected))
            log.exception(e)
            raise e
        else:
            log.info("用例--{}---执行通过".format(expected))

    @pytest.mark.slow
    @pytest.mark.parametrize("case", DataInvest.error_alert_data)
    def test_invest_error_window(self, case, invest_fixture):
        """投资失败，弹框上出现提示信息的用例"""
        invest_page, user_page = invest_fixture
        # 刷新投资页面
        invest_page.page_refresh()
        # 输入投资金额
        invest_page.input_invest_money(case["money"])
        expected = case["expected"]
        # 点击投资
        invest_page.click_invest()
        # 获取页面弹框的提示
        res = invest_page.get_window_error_info()
        try:
            assert expected == res
        except AssertionError as e:
            log.error("用例--{}---执行未通过".format(expected))
            log.exception(e)
            time.sleep(10)
            raise e
        else:
            log.info("用例--{}---执行通过".format(expected))
