import pymysql

class Save(object):


    def __init__(self, host='127.0.0.1', 
                user='root',
                password='root', 
                charset='utf8',
                dbname='datastats',
                tbname='datas'):
        
        self.db_name = dbname
        self.tb_name = tbname

        self.conn = pymysql.connect(host=host,
            user=user, password=password,
            charset=charset)

        self.init()


    def init(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(self.db_name))
        self.cursor.execute('USE datastats')

        # 采集类别、各层级栏目、指标名称、发布日期、采集时间、指标数值、精确指标数值、数值单位、地区
        create_table_sql = """CREATE TABLE IF NOT EXISTS {}(
                            id int not null auto_increment,
                            kind varchar(30),
                            catelogs varchar(400),
                            name varchar(30),
                            pub_date varchar(30),
                            run_date datetime,
                            norm_data varchar(20),
                            exact_data double,
                            unit varchar(10),
                            reg varchar(20),
                            primary key(id)
                            );""".format(self.tb_name)

        self.cursor.execute(create_table_sql)


    def insert(self, datalist):

        sql = "insert into {}(kind,catelogs,name,pub_date,\
              run_date,norm_data,exact_data,unit,reg)\
              values(%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(self.tb_name)

        self.cursor.execute(sql, datalist)
        self.conn.commit()


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
    sv.close