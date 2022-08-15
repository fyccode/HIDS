import time,os,re,json
from mysql import Mysql

class Alert:
    def read_log(self):
        print('======正在实时读取apache日志======')
        file_path = '/opt/lampp/logs/access_log'
        content = os.popen(f'tail -n 0 -f {file_path}')
        while True:
            line = content.readline().strip()
            self.sql_injection_check(line)
            time.sleep(1)
    
    def sql_injection_check(self,line):
        # 匹配解码器
        with open('./decoder/decoder.txt','r') as fp:
            content = fp.readlines()
        for i in content:
            decoder = re.findall(r'^01=(.+)',i.strip())
            if decoder:
                decoder = decoder[0]
                break
        # 提取日志中的信息，依次是ip, date, request_method, path, status_code
        info = re.findall(decoder,line)
        if not info:
            return 1
        path = info[0][3]
        # 匹配规则
        with open('./rules/rule.json','r') as fp:
            content = fp.read()
        rule = json.loads(content)['r1']
        regex_rule = rule['regex']
        count = 1
        for i in regex_rule:
            if i in path:
                count = 0
                print("检测到疑似sql注入")
                break
        if count:
            return 1
        # 输出预警信息,并将预警信息保存到alert.json与数据库中
        alert_info = f'ip:{info[0][0]}\ndate: {info[0][1]}\nrequest method:{info[0][2]}\npath: {info[0][3]}\nstatus code: {info[0][4]}\n\n'
        print(alert_info)
        m1 = Mysql()
        sql = f'insert into alert(srcip,date,method,path,code,type) values("{info[0][0]}","{info[0][1]}","{info[0][2]}","{info[0][3]}","{info[0][4]}","sql injection")'
        m1.insert(sql)
        with open('alert.json','a') as fp:
            content = {"srcip":info[0][0],"date":info[0][1],"method":info[0][2],"path":info[0][3],"status_code":info[0][4]}
            fp.write(json.dumps(content) + '\n')
    
a = Alert()
a.read_log()