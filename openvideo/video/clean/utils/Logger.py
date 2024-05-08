#！/usr/bin/env python
# _*_ coding:utf-8 _*_

# -*- coding:utf-8 -*-
import logging
import time
import os

from IDcard.configs import config

def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class Logger:
    def __init__(self, loggername, log_path=config.log_dir, log_level=config.log_level):
        local_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

        #创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(log_level)

        #创建一个handler，用于写入日志文件
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        logname = '%s/%s_%s.log' % (log_path, loggername, local_time) #指定输出的日志文件名
        fh = logging.FileHandler(logname, encoding = 'utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(log_level)
        #创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        # 定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s-%(levelname)s-[%(filename)s--funcname:%(funcName)s--line:%(lineno)d]\n"
                                      "    %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def get_log(self):
        """定义一个函数，回调logger实例"""
        return self.logger


if __name__ == '__main__':
    t = Logger("hmk").get_log().debug("User %s is loging" % 'jeck')
