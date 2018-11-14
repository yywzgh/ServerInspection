# -*- coding: utf-8 -*-
__Author__ = "guohao"
__Date__ = '2018-11-13'

import configparser

'''
cf = configparser.ConfigParser()

# read config
cf.read("conf.ini")

# return all section
secs = cf.sections()
print('sections:', secs)

opts = cf.options("gitlab")
print('url:', opts)

items = cf.items("gitlab")
print('url:', items)

vaule = cf.get('gitlab', 'host')

print(vaule)
'''


def get_config_value(section, option):

    cf = configparser.ConfigParser()

    cf.read("conf.ini")

    return cf.get(section, option)