# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:39:25 2017
数据库操作
@author: guohao
"""

import pymysql

import logging

from deploy import config_util

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def init_mysql_db():

    # 读取配置文件
    mysql_host = config_util.get_config_value('mysql', 'mysql_host')
    mysql_root_username = config_util.get_config_value('mysql', 'mysql_root_username')
    mysql_root_password = config_util.get_config_value('mysql', 'mysql_root_password')

    mysql_db_name = config_util.get_config_value('mysql', 'mysql_db_name')
    mysql_db_username = config_util.get_config_value('mysql', 'mysql_db_username')
    mysql_db_password = config_util.get_config_value('mysql', 'mysql_db_password')

    # 连接数据库
    conn = pymysql.connect(mysql_host, mysql_root_username, mysql_root_password)

    cursor = conn.cursor()

    # 创建数据库
    sql_create_db = "create database {} default character set utf8 collate utf8_general_ci".format(mysql_db_name)

    cursor.execute(sql_create_db)

    logger.info("数据库{}创建成功！".format(mysql_db_name))

    # 创建用户
    sql_create_user = "create user '{}'@'localhost' identified by '{}'".format(mysql_db_username, mysql_db_password)

    cursor.execute(sql_create_user)

    logger.info("用户{}创建成功！".format(mysql_db_username))

    # 赋权限
    sql_grant_priv = "grant all on {}.* to '{}'@'localhost'".format(mysql_db_name, mysql_db_username)

    cursor.execute(sql_grant_priv)

    logger.info("赋权限成功！")

    # 插入一条数据到moneytb 里面。
    #sql_insert = "insert into money(LAST_NAME,AGE,SEX) values('de2',18,'0')"

    # 在 execute里面执行SQL语句

    #print(cursor.rowcount)

    conn.commit()

    cursor.close()

    conn.close()


if __name__ == "__main__":

    init_mysql_db()