import pytest


@pytest.fixture()
def case_fixture():
    a = 100
    b = 10
    print("======用例====qian zhi=============")
    yield a, b
    print("=======用例===hou zhi=============")


class TestCase:

    def test01(self, case_fixture):
        res = case_fixture
        print(res)
        a,b = res
        assert a == 100
        assert b == 100