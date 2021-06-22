import pytest
from web2020113.data.data_login import DataLogin
from web2020113.common.handle_logging import log


class TestLogin:
    @pytest.mark.parametrize("case", DataLogin.success_case_data)
    def test_login_pass(self, login_fixture, case):
        page_login_driver, page_index_driver = login_fixture
        page_login_driver.click_re_mobile()
        page_login_driver.login(case["mobile"], case["pwd"])
        res = page_index_driver.get_my_user_info()
        try:
            assert res == case["expected"]
        except AssertionError as e:
            log.info("用例--{}---执行失败".format(case["expected"]))
            log.exception(e)
            raise e
        else:
            log.info("用例--{}---执行通过".format(case["expected"]))
            page_index_driver.click_quit()
            page_login_driver.page_refresh()

    @pytest.mark.parametrize("case", DataLogin.error_case_data)
    def test_login_error(self, case, login_fixture):
        page_login_driver, page_index_driver = login_fixture
        page_login_driver.page_refresh()
        page_login_driver.login(case["mobile"], case["pwd"])
        res = page_login_driver.get_error_info()
        try:
            assert res == case["expected"]
        except AssertionError as e:
            log.info("用例--{}---执行失败".format(case["expected"]))
            log.exception(e)
            raise e
        else:
            log.info("用例--{}---执行通过".format(case["expected"]))

    @pytest.mark.parametrize("case", DataLogin.error_alert_data)
    def test_login_error_alert(self, case, login_fixture):
        page_login_driver, page_index_driver = login_fixture
        page_login_driver.page_refresh()
        page_login_driver.login(case["mobile"], case["pwd"])
        res = page_login_driver.get_alert_error_info()
        try:
            assert res == case["expected"]
        except AssertionError as e:
            log.info("用例--{}---执行失败".format(case["expected"]))
            log.exception(e)
            raise e
        else:
            log.info("用例--{}---执行通过".format(case["expected"]))