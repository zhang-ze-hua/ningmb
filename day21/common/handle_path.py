import os


# 项目绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 各模块绝对路径
TESTCASE_DIR = os.path.join(BASE_DIR, "testcase")
REPORT_DIR = os.path.join(BASE_DIR, "report")
LOG_DIR = os.path.join(BASE_DIR, "log")
DATA_DIR = os.path.join(BASE_DIR, "data")
CONF_DIR = os.path.join(BASE_DIR, "conf")
