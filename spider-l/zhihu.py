"""
 根据关键字搜索
 爬取问题标题，url， 回答数目
"""
from urllib.parse import urljoin
from jsonpath import jsonpath
import requests
import json
import re

def get_question(key_word):
    headers = {'user-agent':'Baiduspider'}
    proxies = {'http': 'http://122.114.31.177:808'}
    
    seed_url = ('https://www.zhihu.com/api/v4/search_v3?t=general&q='
                + key_word
                + '&correction=1&offset=0'
                + '&limit=20&lc_idx=6'
                + '&show_all_topics=0&search_hash_id=6f18e0b24a1649bb96c89526e3616adf&vertical_info=0%2C1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C1'
                )

    results = {}

    # https验证错误，简单的处理办法是在get方法中加入verify参数，并设为false。
    content = requests.get(seed_url, headers=headers, proxies=proxies, verify=False)

    # content.text返回为字符串，需要先转化为json才能用jsonpath
    content = json.loads(content.text)

    # jsonpath返回一个list，哪怕结果只有一个
    while not jsonpath(content, '$.paging.is_end')[0]:

        title = jsonpath(content, '$..question.name')
        id = jsonpath(content, '$..question.id')
        if title:
            for i in range(len(title)):
                t = title[i].replace('<em>', '').replace('</em>', '')
                results[t] = urljoin('https://www.zhihu.com/question/', id[i])

        # 加载并格式化下一页内容
        seed_url = jsonpath(content, '$.paging.next')[0]
        content = requests.get(seed_url, headers=headers, proxies=proxies, verify=False)
        content = json.loads(content.text)


    return results
    

if __name__ == '__main__':

    # 直接取消所有urllib3的警告
    requests.packages.urllib3.disable_warnings()
    key_word = '幽默'
    results = get_question(key_word)
    for k, v in results.items():
        print(k, v)
    print('-'*20)
    print('Total %d question pages.'%len(results))