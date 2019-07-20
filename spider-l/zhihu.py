"""
 根据关键字搜索
 爬取问题标题，url， 回答数目
"""
from urllib.parse import urljoin
from jsonpath import jsonpath
import requests
import ssl
import re

def get_page_countent(content):
    results = {}
    urllist = re.findall(r'<a class="question_link" href=".*?".*?>[\s\S]*?</a>', content.text)
    for u in urllist:
        link = re.sub('<a .*? href="(.*?)"[\\s\\S]*?</a>', lambda m: m.group(1), u)
        link = urljoin(base_url, link)

        title = re.sub('<a .*?>\\s*(.*?)\\s*</a>', lambda m: m.group(1), u)
        results[title] = link
    return results

def main(key_word):
    headers = {'user-agent':'Baiduspider'}
    proxies = {}#{'http': 'http://122.114.31.177:808'}
    base_url = 'https://www.zhihu.com/search?type=content&q=沟通'
    
    seed_url = ('https://www.zhihu.com/api/v4/search_v3?t=general&q='
                + key_word
                + '&correction=1&offset=20'
                + '&limit=20&lc_idx=26'
                + '&show_all_topics=0&search_hash_id=6f18e0b24a1649bb96c89526e3616adf&vertical_info=0%2C1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C1'
                )


    # 处理第一部分，首先打开网页，获取数据
    content = requests.get(base_url, headers=headers, proxies=proxies)
    results = get_page_countent(content)

    # 处理第二部分，获取json数据, https验证错误，简单的处理办法是在get方法中加入verify参数，并设为false。
    content = requests.get(seed_url, headers=headers, proxies=proxies, verify=False).text

    # 获取第二页及之后内容
    while not jsonpath(content, '$.paging.is_end'):
        title = jsonpath(content, '$..question.name')
        id = jsonpath(content, '$..question.id')
        link = urljoin('https://www.zhihu.com/question', id)
        if not title:
            continue
        for i in len(title):
            results[title[i]] = link[i]

        seed_url = josnpath(content, '$.paging.next')
        requests.get(seed_url, headers=headers, proxies=proxies, verify=False).text


    print(results)

if __name__ == '__main__':
    import urllib
    # request = urllib.request.Request(url='https://www.zhihu.com/', headers={'user-agent':'Baiduspider'}) 
    # context = ssl._create_unverified_context()
    # web_page = urllib.request.urlopen(request, context=context)
    # ssl._create_default_https_context = ssl._create_unverified_context
    # 直接取消所有urllib3的警告
    requests.packages.urllib3.disable_warnings()
    main('沟通')