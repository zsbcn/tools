# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : logger.py
# Time       ：2023/7/9 20:24
# Author     ：zsbcn
# version    ：python 3.10
# Description：
"""
import sys
from logging import getLogger, StreamHandler, Formatter, FileHandler
from typing import Literal, NewType

LOG_DATE = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = "%(asctime)s %(pathname)s:%(lineno)d %(funcName)s %(levelname)s: %(message)s"

__all__ = ["MyLogger"]

LOG_LEVEL = NewType("LOG_LEVEL", Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])


class MyLogger:
    _LEVEL = "DEBUG"

    def __init__(self, name: str, level: LOG_LEVEL = _LEVEL):
        self._mylogger = getLogger(name)
        self._level = level
        self._mylogger.setLevel(self._level)

    def setConsole(self):
        if self.checkHandler()[0]:
            return self
        stream_handler = StreamHandler(sys.stdout)
        # 构造logger格式
        formatter = Formatter(LOG_FORMAT, LOG_DATE)
        # 应用logger格式
        stream_handler.setFormatter(formatter)
        # 添加到logger记录器集合
        self._mylogger.addHandler(stream_handler)

        return self

    def setLogFile(self, log_dir: str):
        if self.checkHandler()[1]:
            return self
        # 路径文件不存在则创建
        # if not exists(log_dir):
        #     makedirs(log_dir)
        # 设置logger路径
        file_handler = FileHandler("log.log", encoding="utf-8")
        # 构造logger格式
        formatter = Formatter(LOG_FORMAT, LOG_DATE)
        # 应用logger格式
        file_handler.setFormatter(formatter)
        # 添加到logger记录器集合
        self._mylogger.addHandler(file_handler)
        return self

    def checkHandler(self) -> (bool, bool):
        hasStreamHandler = False
        hasFileHandler = False
        for handler in self._mylogger.handlers:
            if not hasStreamHandler and type(handler) == StreamHandler:
                hasStreamHandler = True
            elif not hasFileHandler and type(handler) == FileHandler:
                hasFileHandler = True
        return hasStreamHandler, hasFileHandler

    def getLogger(self):
        """
        * 根据名字获取Logger
        :return:
        """
        return self._mylogger


if __name__ == '__main__':
    logger = MyLogger(__name__).setConsole().setLogFile(__file__).getLogger()

    logger.debug("this is a log")
    logger.info("this is a log")
    logger.warning("this is a log")
    logger.error("this is a log")
    logger.critical("this is a log")
