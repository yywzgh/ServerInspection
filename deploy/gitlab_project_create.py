# -*- coding: utf-8 -*-
__Author__ = "xiewm"
__Date__ = '2017/12/26 13:46'


import requests

import json

class GitLabAPI(object):

    def __init__(self, headers=None, *args, **kwargs):
        self.headers = headers

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

    def create_group(self):

        url = "http://git.vonework.com/api/v4/groups"

        data = json.dumps({'name':'hannan_test_3', 'path':'hannan_test_3'})

        response = requests.post(url, headers=self.headers, data=data)

        status_code = response.status_code

        print(status_code)

        #print(response['status'])

        status_code = response.status_code
        #data_json = json.loads(response.text)

        if status_code != 200:
            raise Exception
        #print('\n解析获取json中data的值:\n', data_json['data'])

if __name__ == "__main__":
    headers = {'Private-Token': '************','Accept': 'application/json', 'Content-Type':'application/json'} #你的gitlab账户的private token
    api = GitLabAPI(headers=headers)
    #content = api.get_user_projects()

    api.create_group();

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
