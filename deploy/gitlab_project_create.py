# -*- coding: utf-8 -*-
__Author__ = "guohao"
__Date__ = '2018-11-13'


import requests

import json

from deploy import config_util


class GitLabAPI(object):

    def __init__(self, headers=None, host=None, *args, **kwargs):
        self.headers = headers
        self.host = host

    def get_user_id(self, username):
        user_id = None
        res = requests.get("https://gitlab地址/api/v3/users?username=%s"%username, headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(res.get('message'))
        content = res.json()
        if content:
            user_id = content[0].get('id')
        return user_id

    def get_user_projects(self):
        res = requests.get("https://gitlab地址/api/v3/projects", headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(res.get('message'))
        content = res.json()
        return content

    def get_user_project_id(self, name):
        """
        :param name: 项目名称
        :return:
        """
        project_id = None
        projects = self.get_user_projects()
        if projects:
            for item in projects:
                if item.get('name') == name:
                    project_id = item.get('id')
        return project_id

    def get_project_branchs(self, project_id):
        branchs = []
        res = requests.get("https://gitlab地址/api/v3/projects/%s/repository/branches"%project_id, headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(res.get('message'))
        content = res.json()
        if content:
            for item in content:
                branchs.append(item.get('name'))
        return branchs

    def get_project_tags(self, project_id):
        tags = []
        res = requests.get("https://gitlab地址/api/v3/projects/%s/repository/tags" % project_id,
                           headers=self.headers, verify=False)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(res.get('message'))
        content = res.json()
        if content:
            for item in content:
                tag_name = item.get('name')
                commit = item.get('commit')
                info = ''
                if commit:
                    commit_id = commit.get('id')
                    commit_info = commit.get('message')
                    info = "%s * %s"%(commit_id[:9], commit_info)
                tags.append("%s     %s"%(tag_name, info))
        return tags

    # 添加成员到project
    def add_member_to_project(self, project_id):

        # url = "http://git.vonework.com/api/v4/projects/18/members"

        url = self.host + "/projects/" + str(project_id) + "/members"

        # userid 3 秦晓武
        # userid 4 陶君行
        # userid 5 卞淼
        # userid 6 杨芳
        # userid 7 李微
        # userid 13 王诗晨

        for i in [3, 4, 5, 6, 7, 13]:

            data = json.dumps({'id': project_id, 'user_id': i, 'access_level': 40})

            response = requests.post(url, headers=self.headers, data=data)

            # print(response.json())

            return_code = response.status_code

            if return_code not in [200, 201]:
                return_text = response.text
                raise Exception(return_text)

        print("------------project member 更新成功-------------------")

    # 创建project
    def create_project(self, namespace_id):

        url = self.host + "/projects"

        project_name = config_util.get_config_value('gitlab', 'project_name')

        data = json.dumps({'name': project_name, 'namespace_id': namespace_id})

        response = requests.post(url, headers=self.headers, data=data)

        # print(response.json())

        return_code = response.status_code

        if return_code not in [200, 201]:
            return_text = response.text
            raise Exception(return_text)

        print("------------project 创建成功-------------------")

        return response.json()['id']

    # 创建group
    def create_group(self):

        url = self.host + "/groups"

        group_name = config_util.get_config_value('gitlab', 'group_name')

        group_path = config_util.get_config_value('gitlab', 'group_path')

        data = json.dumps({'name': group_name, 'path': group_path})

        response = requests.post(url, headers=self.headers, data=data)

        #print(response.json())

        return_code = response.status_code

        if return_code not in [200, 201]:
            return_text = response.text
            raise Exception(return_text)

        print("------------group 创建成功-------------------")

        return response.json()['id']


if __name__ == "__main__":

    token = config_util.get_config_value('gitlab', 'token')

    host = config_util.get_config_value('gitlab', 'host')

    # 你的gitlab账户的private token
    headers = {'Private-Token': token, 'Accept': 'application/json', 'Content-Type': 'application/json'}

    api = GitLabAPI(headers=headers, host=host)

    group_id = api.create_group()

    project_id = api.create_project(group_id)

    api.add_member_to_project(project_id)

    # user_id = api.get_user_id('liming')
    # print "user_id:", user_id
    #
    # project_id = api.get_user_project_id('project1')
    # print "project:", project_id
    #
    # branchs = api.get_project_branchs('345')
    # print "project branchs:", branchs
    #
    # tags = api.get_project_tags('345')
    # print "project tags:", tags
