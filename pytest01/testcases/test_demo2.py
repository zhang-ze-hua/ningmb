import pytest


@pytest.fixture()
def case_fixture():
    print("===============前置条件============")
    yield
    print("===============后置条件============")


class Test01:
    def test01(self, case_fixture):
        print("============用例1============")
        assert 1 == 1

    def test02(self):
        print("==============用例2===========")
        assert 1 == 2
