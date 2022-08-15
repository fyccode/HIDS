import pymysql

class Mysql:
    def __init__(self):
        self.con = pymysql.connect(host='localhost',port=3306,user='root',password='123456',database='test',charset='utf8')
    
    # 执行插入数据的操作
    def insert(self,sql):
        cursor = self.con.cursor()
        cursor.execute(sql)
        self.con.commit()
        cursor.close()
        self.con.close()
