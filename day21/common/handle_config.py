from configparser import ConfigParser, RawConfigParser
from day21.common.handle_path import CONF_DIR
import os


class HandleConfig(RawConfigParser):
    """配置文件解析器类的封装"""

    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding="utf8")


path = os.path.join(CONF_DIR, "config.ini")
conf = HandleConfig(path)
