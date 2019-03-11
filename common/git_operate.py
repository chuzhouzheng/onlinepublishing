__author__ = 'Administrator'
import os

class GitOperate(object):
    '''
        git代码更新；
        repository_path：仓库所在路径；
        repository_name：仓库名称；
        branch_name：分支名称
    '''

    def __init__(self, repository_path, repository_name, branch_name, operate_type='pull'):
        self.repository_path = repository_path
        self.repository_name = str(repository_name)
        self.branch_name = str(branch_name)
        self.operate_type = str(operate_type)

    def run(self):
        '''
            执行命令
        '''
        exec_results = []

        if self.operate_type == 'pull':
            # 进入路径
            exec_command = 'cd ' + self.repository_path + self.repository_name
            exec_results.append('执行命令：    ' + exec_command)
            exec_result = os.popen(exec_command).read()
            exec_results.append('执行结果：' + exec_result)

            # checkout前先拉取代码
            exec_command = 'git pull'
            exec_results.append('执行命令：    ' + exec_command)
            exec_result = os.popen(exec_command).read()
            exec_results.append('执行结果：' + exec_result)

            # 切换分支
            exec_command = 'git checkout ' + self.branch_name
            exec_results.append('执行命令：    ' + exec_command)
            exec_result = os.popen(exec_command).read()
            exec_results.append('执行结果：' + exec_result)

            # checkout后拉取代码
            exec_command = 'git pull'
            exec_results.append('执行命令：    ' + exec_command)
            exec_result = os.popen(exec_command).read()
            exec_results.append('执行结果：' + exec_result)

        return exec_results

