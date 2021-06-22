import os

# 获取项目所在的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
# 用例数据所在的目录路径
DATA_DIR = os.path.join(BASE_DIR, "data")

# 配置文件所在的目录路径
CONF_DIR = os.path.join(BASE_DIR, "conf")

# 测试报告所在的目录路径
REPORT_DIR = os.path.join(BASE_DIR, "result/report")

# 日志文件所在的目录路径
LOG_DIR = os.path.join(BASE_DIR, "result/log")

# 错误截图的路径
ERROR_IMG = os.path.join(BASE_DIR, "result/error_image")
