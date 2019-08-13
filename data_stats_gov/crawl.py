import os
import sys
import time
import json
import requests
import setting

from save import Save
from jsonpath import jsonpath


class Crawl(object):

    def __init__(self):
        self.load_setting()
        self.sv = Save()
        self.session = requests.session()
        self.dup_keys = {}
        self.has_reg = False  # 参数是否包含地区
        self.base_url = "http://data.stats.gov.cn/easyquery.htm"
        self.reg_code_list = []
        # 加载栏目
        dbname = ["月度数据","季度数据","季度数据","分省月度数据","分省季度数据","分省年度数据",
                "主要城市月度价格","主要城市年度数据","港澳台月度数据","港澳台年度数据"]
        self.dbcode = {
            "月度数据": "hgyd",
            "季度数据": "hgjd",
            "年度数据": "hgnd",
            "分省月度数据": "fsyd",
            "分省季度数据": "fsjd",
            "分省年度数据": "fsnd",
            "主要城市月度价格": "csyd",
            "主要城市年度数据": "csnd",
            "港澳台月度数据": "gatyd",
            "港澳台年度数据": "gatnd",
        }


    def run(self):
        self.get_input_info()
        if self.has_reg:
            self.reg_code_list = self.get_reg_code_list()
        self.load_dup()
        res = self.get_json_data()
        self.select_time()
        self.dfs(res)
        self.regather()
        self.clean()


    def get_input_info(self):
        self.selected_item = input("现有栏目类别如下:\n1.月度数据\n2.年度数据\n3.分省月度数据\n"
            "4.分省季度数据\n5.分省年度数据\n6.主要城市月度价格\n7.主要城市年度数据\n8.港澳台月度数据\n"
            "9.港澳台年度数据\n请输入栏目名称(如: 月度数据):\n").strip()
        while True:
            if self.selected_item not in self.dbcode:
                self.selected_item = input("输入错误，请重新输入:\n").strip()
                continue
            break

        self.path = [self.selected_item]  # 存储路径
        if self.dbcode[self.selected_item][0] != 'h':
            self.has_reg = True

        self.selected_time = input("\n请输入采集时间,格式举例如下:\n月: 201901\n"
            "季：2019A,2019B,2019C,2019D\n年：2019\n其它：2013-, last3\n").strip()


    def get_json_data(self, block=None, regcode=None, data_type='tree'):
        if data_type == 'tree':
            # 获取次级目录
            if block is None:
                block = {"id": "zb",
                        "dbcode": self.dbcode[self.selected_item],
                        "wdcode": "zb"}

            data = {"id": block["id"],
                    "dbcode": block["dbcode"],
                    "wdcode": block["wdcode"],
                    "m": "getTree"}
            
            response = self.session.post(self.base_url, data=data)

        elif data_type == 'detail':
            data = {"m": "QueryData",
                    "dbcode": block["dbcode"],
                    "rowcode": "zb",
                    "colcode": "sj",

                    "wds": ("[]" if not self.has_reg else '[{"wdcode":"reg",'+
                           '"valuecode":"'+regcode+'"}]'),

                    "dfwds": ('[{"wdcode":"'+block["wdcode"]+'",'+
                             '"valuecode":"'+block["id"]+'"}]'),

                    "k1": str(int(time.time()*1000))}
            
            response = self.session.get(self.base_url, params=data)

        try:
            res = json.loads(response.text)
        except:
            self.save_dup()
            leak_data = {"data": data, "path": self.path}
            with open('err.log', 'a', encoding='utf-8') as f:
                f.write(str(leak_data)+'\n')
            time.sleep(self.load_error_wait_time)
            print('--------------JsonError---------------')
            raise
        return res


    def clean(self):
        """退出时的清理工作"""
        self.save_dup()
        self.sv.close()
        # 删除日志文件
        logfile = os.path.join(os.getcwd(), 'err.log')
        os.remove(logfile)

    def regather(self):
        """补采数据"""
        with open("err.log", "r", encoding='utf-8') as f:
            for i in f:
                data_block = i.strip().replace("'", '"')
                # print(data_block)
                data_block = json.loads(data_block)
                self.path = data_block['path']
                self.data = data_block['data']
                res = self.get_json_data(self.data)
                self.dfs(res)



    def get_reg_code_list(self):
        data = {
            "m": "getOtherWds",
            "dbcode": self.dbcode[self.selected_item],
            "rowcode": "zb",
            "colcode": "sj",
            "wds": "[]",
            "k1": str(int(time.time()*1000)),
            }

        reg_code_list = []

        response = self.session.get(self.base_url, params=data)
        res = json.loads(response.text)
        regs = jsonpath(res, "$.returndata..nodes")[0]

        for reg in regs:
            reg_code_list.append(reg["code"])

        return reg_code_list


    def select_time(self, regcode=None):
        regcode = '110000'  # 先写死，实验可不可以

        data_detail = {"m": "QueryData",
                      "dbcode": self.dbcode[self.selected_item],
                      "rowcode": "zb",
                      "colcode": "sj",
                      "wds": ("[]" if not self.has_reg else '[{"wdcode":"reg",'
                             '"valuecode":"'+regcode+'"}]'),
                      "dfwds": '[{"wdcode":"sj","valuecode":"'+
                            self.selected_time+'"}]',
                      "k1": str(int(time.time()*1000))}

        # 会出错，可以重构
        response = self.session.get(self.base_url, params=data_detail)
        res = json.loads(response.text)

        if res['returndata'] == '对不起，未能找到符合查询条件的信息。':
            print("未找到相应时间，请重新输入:")
            self.selected_time = input("\n请输入采集时间,格式举例如下:\n月: 201901\n"
            "季：2019A,2019B,2019C,2019D\n年：2019\n其它：2013-, last3\n").strip()
            self.select_time()


    def dfs(self, res):

        print(f'enter{self.path}')
        for block in res:
            # 如果是目录
            if block["isParent"]:

                try:
                    res = self.get_json_data(block)
                except:
                    time.sleep(self.load_error_wait_time)
                    continue

                self.path.append(block['name'])
                # 如果短时间内请求过多可能返回错误页面
                time.sleep(self.delay_time)

                self.dfs(res)

                self.path.pop()

            # 如果是细缆页
            else:
                self.path.append(block['name'])
                # print(self.path)
                time.sleep(self.delay_time)

                # 如果存在地区信息
                if self.has_reg:
                    for regcode in self.reg_code_list:
                        time.sleep(self.delay_time)
                        self.get_data(block, regcode)
                else:
                    self.get_data(block)
                self.path.pop()


    def is_duplicated(self, code):
        """判断数据是否已采集"""

        if code in self.dup_keys:
            return True
        self.dup_keys[code] = True
        return False


    def save_dup(self):
        """保存采集记录"""
        with open(self.dbcode[self.selected_item]+".din", 
                 'w', encoding='utf-8') as f:
            json.dump(self.dup_keys, f, ensure_ascii=False)


    def load_dup(self):
        """加载采集记录"""
        filename = self.dbcode[self.selected_item]+".din"
        try:
            f = open(filename, 'r')
        except FileNotFoundError:
            f = open(filename, 'w', encoding='utf-8')
        else:
            if f.read() != '':
                f.seek(0)
                self.dup_keys = json.load(f)
            f.close()


    def get_data(self, block, regcode=None):
        path_data = self.path[:]

        try:
            res = self.get_json_data(block, regcode, data_type='detail')
        except json.decoder.JSONDecodeError:
            return

        # 找到名称与code的映射 需加入unit
        # 包含名称、地区(可能没有)、时间等信息
        nodes = jsonpath(res, '$.returndata.wdnodes[*].nodes')

        name_code = {}
        for node in nodes:
            for _ in node:
                name_code[_['code']] = _['name'] + '^_^' + _['unit']

        # 获取当前json中全部数据
        data_nodes = jsonpath(res, "$.returndata.datanodes")[0]

        for data_node in data_nodes:

            if self.is_duplicated(data_node['code']):
                print('--------duplicated----------')
                continue

            exc_data = []
            exc_data.append(path_data[0])

            catelogs = "、".join(path_data[1:])
            exc_data.append(catelogs)

            name, unit, reg, sj = self.get_data_from_code(name_code, 
                data_node['code'])
            
            exact_data = data_node['data']['data']
            normal_data = data_node['data']['strdata']

            exc_data.append(name)
            exc_data.append(sj)
            exc_data.append(time.strftime('%Y-%m-%d %H:%M:%S'))
            exc_data.append(normal_data)
            exc_data.append(exact_data)
            exc_data.append(unit)
            exc_data.append(reg)

            self.save_data(exc_data)
            del exc_data


    def save_data(self, data_list):
        # with open(self.selected_item+self.selected_time+, 
        #          'a', encoding='utf-8') as f:
        #     f.write(str(data_list)+'\n')
        self.sv.insert(data_list)


    def load_setting(self):
        self.delay_time = setting.delay_time
        self.load_error_wait_time = setting.load_error_wait_time


    def get_data_from_code(self, name_code, code):
        """
        根据给出的代码解析出名称、单位、地点、时间等信息并返回
        code形式: zb.A03010101_reg.110000_sj.201906 ；其中reg可能不存在
        """
        name, unit, reg, sj = "", "", "", ""
        n = code.split('_')

        for _ in n:
            if 'zb' in _:
                uan = name_code[_.split('.')[1]]
                name = uan.split('^_^')[0]
                unit = uan.split('^_^')[1]
                if unit == "":
                    unit = "-"
            elif 'reg' in _:
                reg = name_code[_.split('.')[1]].split('^_^')[0]
            elif 'sj' in _:
                sj = name_code[_.split('.')[1]].split('^_^')[0]

        return (name, unit, reg, sj)


if __name__ == '__main__':
    crawl = Crawl()
    crawl.run()