import pymysql
import setting

class Save(object):


    def __init__(self):

        self.load_setting()
        self.db_name = self.info['database_name']
        self.tb_name = self.info['table_name']
        self.conn = pymysql.connect(
            host = self.info['host'],
            port = self.info['port'],
            user = self.info['user'],
            password = self.info['password'],
            charset = self.info['charset'])

        self.init()


    def init(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(self.db_name))
        self.cursor.execute('USE {}'.format(self.db_name))

        # 采集类别、各层级栏目、指标名称、发布日期、采集时间、指标数值、精确指标数值、数值单位、地区
        create_table_sql = ("CREATE TABLE IF NOT EXISTS {}("
                            "id int not null auto_increment,"
                            "kind varchar(50),"
                            "catelogs varchar(400),"
                            "name varchar(50),"
                            "pub_date varchar(50),"
                            "run_date datetime,"
                            "norm_data varchar(50),"
                            "exact_data double,"
                            "unit varchar(30),"
                            "reg varchar(30),"
                            "primary key(id)"
                            ");").format(self.tb_name)

        self.cursor.execute(create_table_sql)


    def insert(self, datalist):

        sql = ("insert into {}(kind,catelogs,name,pub_date,"
              "run_date,norm_data,exact_data,unit,reg)"
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(self.tb_name)

        self.cursor.execute(sql, datalist)
        self.conn.commit()


    def load_setting(self):
        self.info = setting.sql_info


    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    import time

    sv = Save()
    dat = ['分省月度数据', '价格指数、居民消费价格分类指数、居民消费价格分类指数(上年同月=100)(2016-)',
          '交通和通信类居民消费价格指数(上年同月=100)', '2019年3月',
          '2019-08-09 17:26:18', '99.4', 99.4362435, '-', '北京市']
    sv.insert(dat)

    time.sleep(10)
    sv.close()