import logging
from day21.common.handle_config import conf


class HandleLogger:
    """处理日志相关的模块"""
    @staticmethod
    def create_logger():
        """
        创建日志收集器
        :return: 日志收集器
        """
        # 第一步：创建一个日志收集器
        log = logging.getLogger("zhang")

        # 第二步：设置收集器收集的等级
        log.setLevel(conf.get("log", "level"))

        # 第三步：设置输出渠道以及输出渠道的等级
        fh = logging.FileHandler(conf.get("log", "filename"), encoding="utf8")
        fh.setLevel(conf.get("log", "fh_level"))
        log.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(conf.get("log", "sh_level"))
        log.addHandler(sh)
        # 创建一个输出格式对象
        form = logging.Formatter(conf.get("log", "formats"))
        # 将输出格式添加到输出渠道
        fh.setFormatter(form)
        sh.setFormatter(form)

        return log


log = HandleLogger.create_logger()
