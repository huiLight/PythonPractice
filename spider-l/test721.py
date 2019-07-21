from hashlib import sha1
from urllib.parse import urljoin

import pickle
import re
import requests
import zlib

from redis import Redis

def main():
    # 指定种子页面
    base_url = 'https://www.zhihu.com/'
    seed_url = urljoin(base_url, 'explore')

    # 创建Redis客户端
    client = Redis(host='1.2.3.4', port=6379, password='1qaz2wsx')
    # 设置用户代理(否则访问会被拒绝)
    headers = {'user-agent': 'Baiduspider'}
    # 通过requests模块发送GET请求并指定用户代理
    resp = requests.get(seed_url, headers=headers)
    #

    urllist = re.findall(r'<a class="question_link" href=".*?".*?>[\s\S]*?</a>', resp.text)
    # 将URL处理成SHA1摘要(长度固定更简短)
    hasher_proto = sha1()
    for a_tag in urllist:
        link = re.sub('<a .*? href="(.*?)"[\\s\\S]*?</a>', lambda m: m.group(1), a_tag)
        full_url = urljoin(base_url, link)

        # 传入URL生成SHA1摘要
        hasher = hasher_proto.copy()
        hasher.update(full_url.encode('utf-8'))
        field_key = hasher.hexdigest()
        # 如果Redis
        if not client.hexists('zhihu', field_key):
            html_page = requests.get(full_url, headers=headers).text
            # 对页面进行序列化和压缩
            zipped_page = zlib.compress(pickle.dumps(html_page))
            # 使用hash数据类型保存URL摘要及对应的页面代码
            client.hset('zhihu', field_key, zipped_page)

        # 显示总共缓存了多少页面
        print('Total %d question pages found.'%client.hlen('zhihu'))

if __name__ == '__main__':
    main()

