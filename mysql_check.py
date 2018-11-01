#!/usr/bin/env python

# coding=utf-8

# ----------------------------------------------------------

# Name: MySQL巡检脚本

# Purpose: 监控多台Web服务器状态,一旦出现问题就发送邮件

# Version: 1.0

# Author: nick

# BLOG: http://yywzgh.com

# EMAIL: yywzgh@gmail.com

# Created: 2018-06-01

# Copyright: (c) LEO 2013

# Python: 3.6

# ----------------------------------------------------------

import pymysql

conn = pymysql.connect(host='192.168.2.210', port=3306, user='root', password='a123456', database='mysql')

# 使用cursor()方法获取操作游标
cursor = conn.cursor()

sql = "SELECT user, host FROM user limit 1"

try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        user = row[0]
        host = row[1]
        # 打印结果
        print("fname=%s,lname=%s" % (user, host))
        print("database status is ok")
except:
    print("database can't connect !")
    raise

# 关闭数据库连接
conn.close()
