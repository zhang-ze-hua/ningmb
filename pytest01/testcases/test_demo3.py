import pytest


error_case_data = [
    {'mobile': "", "pwd": "python1", "expected": "请输入手机号"},
    {'mobile': "1868472055a", "pwd": "python1", "expected": "请输入正确的手机号"},
    {'mobile': "18684720553", "pwd": "", "expected": "请输入密码"}
]


# 读取excel数据
@pytest.mark.parametrize('musen', error_case_data)
def test_dome_04(musen):
    print(musen)
    print('--------------用例执行-------------')
    assert True