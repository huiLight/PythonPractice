import requests
import time
import json
from save import Save
from jsonpath import jsonpath


has_reg = False  # 参数是否包含地区

# 加载栏目
dbcode = {
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

# id = {"指标":"zb", "地区":"reg"}

base_url = "http://data.stats.gov.cn/easyquery.htm"

selected_item = input("请输入采集栏目类别:\n").strip()
if dbcode[selected_item][0] != 'h':
    has_reg = True

selected_time = input("请输入采集时间():\n").strip()

path = [selected_item]  # 存储路径

def get_json_data(block=None, data_type='tree'):
    if data_type == 'tree':
        # 获取次级目录
        if block is None:
            block = {"id": "zb",
                    "dbcode": dbcode[selected_item],
                    "wdcode": "zb"}

        data = {"id": block["id"],
                "dbcode": block["dbcode"],
                "wdcode": block["wdcode"],
                "m": "getTree"}
        
        response = session.post(base_url, data=data)

    elif data_type == 'detail':
        data = {"m": "QueryData",
                "dbcode": block["dbcode"],
                "rowcode": "zb",
                "colcode": "sj",

                "wds": ("[]" if not has_reg else '[{"wdcode":"reg",'+
                       '"valuecode":"'+regcode+'"}]'),

                "dfwds": ('[{"wdcode":"'+block["wdcode"]+'",'+
                         '"valuecode":"'+block["id"]+'"}]'),

                "k1": str(int(time.time()*1000))}
        
        response = session.get(base_url, params=data)

    # session = requests.session()
    try:
        res = json.loads(response.text)
    except:
        save_dup()
        sv.close()
        raise

    return res


def start():
    """获取次级目录信息"""

    data = {
            "id": 'zb',
            "dbcode": dbcode[selected_item],
            "wdcode": 'zb',
            "m": "getTree",
            }

    # session = requests.session()

    response = session.post(base_url, data=data)
    res = json.loads(response.text)

    return res


def get_reg_code_list():
    data = {
        "m": "getOtherWds",
        "dbcode": dbcode[selected_item],
        "rowcode": "zb",
        "colcode": "sj",
        "wds": "[]",
        "k1": str(int(time.time()*1000)),
        }

    reg_code_list = []

    response = session.get(base_url, params=data)
    res = json.loads(response.text)
    regs = jsonpath(res, "$.returndata..nodes")[0]

    for reg in regs:
        yield reg["code"]
        # reg_code_list.append(reg["code"])

    # return reg_code_list


def select_time(regcode=None):
    regcode = '110000'  # 先写死，实验可不可以

    data_detail = {"m": "QueryData",
                  "dbcode": dbcode[selected_item],
                  "rowcode": "zb",
                  "colcode": "sj",
                  "wds": "[]" if not has_reg else '[{"wdcode":"reg",\
                         "valuecode":"'+regcode+'"}]',
                  "dfwds": '[{"wdcode":"sj","valuecode":"'+selected_time+'"}]',
                  "k1": str(int(time.time()*1000))}

    # 会出错，可以重构
    response = session.get(base_url, params=data_detail)
    res = json.loads(response.text)

    if res['returndata'] == '对不起，未能找到符合查询条件的信息。':
        raise Exception("未找到相应时间，请核准后再查询")


def dfs(res):

    # print(f'enter{path}')
    for block in res:
        # 如果是目录
        # print(type(block))
        if block["isParent"]:

            res = get_json_data(block)

            path.append(block['name'])

            # 如果短时间内请求过多可能返回错误页面
            # time.sleep(1)
            # try:
            dfs(res)
            # except:
            #   with open("e.txt", 'a') as f:
            #       f.write(str(res))
            path.pop()

        # 如果是细缆页
        else:
            # time.sleep(1)
            path.append(block['name'])
            # print(path)

            # 如果存在地区信息
            if has_reg:
                for regcode in get_reg_code_list():
                    # time.sleep(0.5)
                    get_data(block, path, regcode)
            else:
                get_data(block, path)
            path.pop()


dup_keys = {}  # 对比函数
def is_duplicated(code):
    print(code)
    if code in dup_keys:
        return True
    dup_keys[code] = True
    return False


def save_dup():
    with open("dup_keys.info", 'w', encoding='utf-8') as f:
        json.dump(dup_keys, f, ensure_ascii=False)

def load_dup():
    global dup_keys
    try:
        f = open("dup_keys.info", 'r')
    except FileNotFoundError:
        f = open("dup_keys.info", 'w', encoding='utf-8')
    else:
        if f.read() != '':
            f.seek(0)
            dup_keys = json.load(f)
        f.close()


def get_data(block, path, regcode=None):
    path_data = path[:]

    try:
        res = get_json_data(block, data_type='detail')
    except json.decoder.JSONDecodeError:
        # TODO(huilight@outlook.com): 保存错误日志
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
        
        if is_duplicated(data_node['code']):
            continue

        exc_data = []
        exc_data.append(path_data[0])

        catelogs = "、".join(path_data[1:])
        exc_data.append(catelogs)

        name, unit, reg, sj = get_data_from_code(name_code, data_node['code'])
        
        exact_data = data_node['data']['data']
        normal_data = data_node['data']['strdata']

        exc_data.append(name)
        exc_data.append(sj)
        exc_data.append(time.strftime('%Y-%m-%d %H:%M:%S'))
        exc_data.append(normal_data)
        exc_data.append(exact_data)
        exc_data.append(unit)
        exc_data.append(reg)

        save_data(exc_data)

        del exc_data


def save_data(data_list):
    with open(selected_item+selected_time, 'a', encoding='utf-8') as f:
        f.write(str(data_list)+'\n')
    # sv.insert(data_list)


def get_data_from_code(name_code, code):
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
    session = requests.session()
    sv = Save()

    # res = start()
    load_dup()
    res = get_json_data()
    select_time()
    dfs(res)

    # sv.close()
