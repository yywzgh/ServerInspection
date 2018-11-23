# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:39:25 2017
数据库操作
@author: guohao
"""

import pymysql

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def init_mysql_db():

    conn = pymysql.connect('192.168.0.210', 'root', 'a123456','mysql')

    cursor = conn.cursor()

    sql_create_db = "create database han_test default character set utf8 collate utf8_general_ci"

    cursor.execute(sql_create_db)

    logger.info("数据库创建成功！")

    sql_create_user = "create user 'han_test'@'localhost' identified by 'a123456'"

    cursor.execute(sql_create_user)

    logger.info("用户创建成功！")

    sql_grant_priv = "grant all on han_test.* to 'han_test'@'localhost'"

    cursor.execute(sql_grant_priv)

    logger.info("赋权限成功！")

    # 插入一条数据到moneytb 里面。
    #sql_insert = "insert into money(LAST_NAME,AGE,SEX) values('de2',18,'0')"

    # 在 execute里面执行SQL语句

    print(cursor.rowcount)

    conn.commit()

    cursor.close()

    conn.close()


if __name__ == "__main__":

    init_mysql_db()