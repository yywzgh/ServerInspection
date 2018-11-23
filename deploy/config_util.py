# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:39:25 2017
配置文件工具类
@author: guohao
"""

import configparser


def get_config_value(section, option):

    cf = configparser.ConfigParser()

    cf.read("conf.ini")

    return cf.get(section, option)