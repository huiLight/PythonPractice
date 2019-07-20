"""
7月20号练习
爬取知乎首页问题链接
"""

from urllib.parse import urljoin

import re
import requests

# re.match(pattern, string) 返回一个列表，第一项为匹配到的字符串

def main():
    headers = {'user-agent':'Baiduspider'}
    proxies = {'http': 'http://122.114.31.177:808'}

    base_url = 'https://www.zhihu.com'
    seed_url = urljoin(base_url, 'explore')
    content = requests.get(seed_url, headers=headers, proxies=proxies)


    results = {}
    urllist = re.findall(r'<a class="question_link" href=".*?".*?>[\s\S]*?</a>', content.text)
    for u in urllist:
        link = re.sub('<a .*? href="(.*?)"[\\s\\S]*?</a>', lambda m: m.group(1), u)
        link = urljoin(base_url, link)

        title = re.sub('<a .*?>\\s*(.*?)\\s*</a>', lambda m: m.group(1), u)
        results[title] = link

    for k, v in results.items():
        print(k, v)
    print('-'*20)
    print('Total %d question pages found.'%len(results))

if __name__ == '__main__':
    main()
