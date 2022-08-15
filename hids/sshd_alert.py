import re,os,time
from datetime import datetime 
from mysql import Mysql

class SshdAlert:
    def f1(self):
        file_path = '/var/log/secure'
        content = os.popen(f'tail -n 0 -f {file_path}')
        while True:
            line = content.readline().strip()
            self.sshd_check(line)
            time.sleep(1)

    @staticmethod
    def sshd_check(line):
        # 匹配以Invalid和Failed开头的日志信息
        content = re.findall(r'^Invalid|Failed.+',line)
        if content:
            content = content[0]
            srcip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',content)
            info = f'\n检测到远程登录失败\nsrcip: {srcip[0]}\ntime: {datetime.now()}\n'
            print(info)
            # 写入文件
            with open('alert.txt','a') as fp:
                fp.write(info)
            # 写入数据库
            m = Mysql()
            sql = f'insert into alert(srcip,date,method,type) values("{srcip[0]}",now(),"ssh","ssh-remote-login")'
            m.insert(sql)
            return 1

s1 = SshdAlert()
s1.f1()