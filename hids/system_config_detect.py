import os
import re

class SystemDetect:
    # print("======检测系统配置项======")
    def sys_ver(self):
        # 检测系统内核及发行版本
        print('\n======检测系统版本======')
        sys_version = os.popen("uname -a | awk '{print $3}'").read().strip()
        print('[Linux内核版本]:',sys_version)
        centos_version = os.popen("cat /etc/redhat-release").read().strip()
        print('[CentOs版本]:',centos_version)
    
   
    def user_check(self):
        # 检测除root用户外的其余用户
        print('\n======检测额外用户======')
        user_info = os.popen('cat /etc/passwd').read().strip()
        user_info_list = user_info.split('\n')
        count = 0
        for user in user_info_list:
            if int(user.split(':')[2]) >= 1000:
                count += 1
        if count == 0:
            print("不存在除root以外的用户")
        else:
            print("root以外的用户:")
        for user in user_info_list:
            user_list = user.split(':')
            if int(user_list[2]) >= 1000:
                print(f'[user]:{user_list[0]}',f'[uid]:{user_list[2]}',f'[gid]:{user_list[3]}')
        # 检测空口令账户和root权限账户
        print('\n======检测空口令账户和root权限账户======')
        command1 = os.popen("awk -F: '($2==" + '""' + ")' /etc/shadow ").read().strip()
        if command1 == '':
            print('不存在空口令账户')
        else:
            print('存在空口令账户:',command1)
        command2 = os.popen("awk -F: '($3 == 0) { print $1 }' /etc/passwd").read().strip()
        print('uid为0的账户:',command2)

   
    def authority_check(self):
        # 检测初始化文件权限
        print('\n======权限检测======')
        command = os.popen('grep "umask 027" /etc/profile').read().strip()
        if command == '':
            print('警告: 初始化文件权限异常,建议修改umask值')
        else:
            print('初始化文件权限正常')
        # 检测su root
        with open('/etc/pam.d/su','r') as fp:
            content = fp.readlines()
        for i in content:
            res = re.findall(r'^auth\s+required\s+pam_wheel.so\s+group=',i.strip())
            if res:
                res = i.strip().split('=')[1]
                break
        if res:
            print('只允许su root的组为:',res)
        else:
            print('警告: 任何用户均可su root,建议进行限制')
        # 检测sudo权限
        with open('/etc/sudoers','r') as fp:
            content = fp.readlines()
        sudo_list = []
        for i in content:
            res = re.findall(r'^\w+\s+ALL=\(ALL\)\s+ALL',i.strip())
            if res:
                sudo_list.append(i.strip())
        if len(sudo_list) == 1 and sudo_list[0].split('\t')[0] == 'root':
            print('只有root拥有所有权限')
        else:
            print('警告: 除了root外,还有其余用户拥有所有权限')


s1 = SystemDetect()
s1.sys_ver()
s1.user_check()
s1.authority_check()