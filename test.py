__author__ = 'Administrator'


import os
update_detail =''
exec_result = os.popen(r"cd D:/git/mywork/test").read()
update_detail = update_detail + "cd D:/git/mywork/test" + '\n' + str(exec_result) + '\n'
# print(update_detail)

exec_result = os.popen("git pull").read()
update_detail = update_detail + "git pull" + '\n' + str(exec_result) + '\n'
# print(update_detail)

exec_result = os.popen("git checkout master").read()
update_detail = update_detail + "git checkout master" + '\n' + str(exec_result) + '\n'
# print(update_detail)

exec_result = os.popen("git pull").read()
update_detail = update_detail + "git pull" + '\n' + str(exec_result) + '\n'
print(update_detail)