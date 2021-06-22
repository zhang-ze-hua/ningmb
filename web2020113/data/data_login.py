class DataLogin:
    # 正常登录的用例
    success_case_data = [
        {'mobile': "18684720553", "pwd": "python", "expected": "登录成功"},
        {'mobile': "18684720553", "pwd": "python", "expected": "登录成功"},
    ]
    # 异常的用例数据：错误提示在页面上
    error_case_data = [
        {'mobile': "", "pwd": "python1", "expected": "请输入手机号"},
        {'mobile': "1868472055a", "pwd": "python1", "expected": "请输入正确的手机号"},
        {'mobile': "18684720553", "pwd": "", "expected": "请输入密码"}
    ]
    # 异常的用例数据，错误提示在弹窗中
    error_alert_data = [
        {'mobile': "18684720553", "pwd": "pyt1234", "expected": "帐号或密码错误!"},
        {'mobile': "18684727888", "pwd": "python1", "expected": "此账号没有经过授权，请联系管理员!"},
    ]
