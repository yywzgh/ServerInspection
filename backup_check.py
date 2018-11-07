#!/usr/bin/env python

# coding=utf-8


# ----------------------------------------------------------

# Name: WEB服务器巡检脚本

# Copyright: (c) LEO 2013

# Python: 2.4/2.7

# ----------------------------------------------------------


import os

import paramiko

from functools import wraps

from datetime import datetime

import time


def getDate() :
    now = int(time.time())
    # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeStruct = time.localtime(now)
    strTime = time.strftime("%Y-%m-%d", timeStruct)
    return strTime





class SSHManager:
    def __init__(self, host, usr, passwd):
        self._host = host
        self._usr = usr
        self._passwd = passwd
        self._ssh = None
        self._sftp = None
        self._sftp_connect()
        self._ssh_connect()

    def __del__(self):
        if self._ssh:
            self._ssh.close()
        if self._sftp:
            self._sftp.close()

    def _sftp_connect(self):
        try:
            transport = paramiko.Transport((self._host, 22))
            transport.connect(username=self._usr, password=self._passwd)
            self._sftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            raise RuntimeError("sftp connect failed [%s]" % str(e))

    def _ssh_connect(self):
        try:
            # 创建ssh对象
            self._ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            self._ssh.connect(hostname=self._host,
                              port=22,
                              username=self._usr,
                              password=self._passwd,
                              timeout=5)
        except Exception:
            raise RuntimeError("ssh connected to [host:%s, usr:%s, passwd:%s] failed" %
                               (self._host, self._usr, self._passwd))


    def ssh_exec_cmd(self, cmd, path='~'):
        """
        通过ssh连接到远程服务器，执行给定的命令
        :param cmd: 执行的命令
        :param path: 命令执行的目录
        :return: 返回结果
        """
        try:
            result = self._exec_command('cd ' + path + ';' + cmd)
            print(result)
        except Exception:
            raise RuntimeError('exec cmd [%s] failed' % cmd)

    def _exec_command(self, cmd):
            """
            通过ssh执行远程命令
            :param cmd:
            :return:
            """
            try:
                stdin, stdout, stderr = self._ssh.exec_command(cmd)
                result = stdout.read()
                if result is not None:
                    result = stderr.read()
                    print(result.decode())

                if '没有那个文件或目录' in result.decode():
                    print('备份服务器有备份没有成功')

                return result.decode()
            except Exception as e:
                raise RuntimeError('Exec command [%s] failed' % str(cmd))




if __name__ == '__main__':
    ip = '192.168.0.220'
    usr = 'root'
    passwd = 'a123456'
    currDate = getDate()
    ssh = SSHManager(ip, usr, passwd)
    command = 'ls -l /backup/mysql/mysql-backup_%s.tar.gz' % currDate
    ssh._exec_command(command)
