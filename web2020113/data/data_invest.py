class DataInvest:
    # 投资成功的用例
    success_case_data = [
        {'money': "100", "expected": "投标成功！"},
        {'money': "200", "expected": "投标成功！"},
    ]
    # 异常的用例数据：错误提示在按钮上
    error_case_data = [
        {'money': "568", "expected": "请输入10的整数倍"},
        {'money': "-11", "expected": "请输入10的整数倍"},
    ]
    # 异常的用例数据，错误提示在弹窗中
    error_alert_data = [
        {'money': "0", "expected": "请正确填写投标金额"},
        {'money': "10000000", "expected": "购买标的金额不能大于标总金额"},
    ]
