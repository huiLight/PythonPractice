from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import re
import time
from progress import pros
import random

def main():

    time.sleep(10)

    # 如果未加载重试3次
    for i in range(3):
        try:
            driver.find_element_by_xpath("//td[contains(text(), '医疗器械经营企业（备案）')]").click()
        except:
            time.sleep(10)
            driver.find_element_by_xpath("//td[text()='医疗器械经营企业（备案）']").click()
        else:
            break

def write_current_page(page):
    with open('error.ini', 'w') as f:
        f.write(str(page))

def reopen_the_page(page_num):
    write_current_page(page_num)
    # 发现该元素，重新打开该页面
    driver.find_element_by_xpath("//td[contains(text(), '医疗器械经营企业（备案）')]").click()
    for k in range(5):
        try:
            input_page = driver.find_element_by_xpath('//*[@id="goInt"]')
            input_page.clear()
            input_page.send_keys(str(page_num))
            driver.find_element_by_xpath("//input[@src='images/dataanniu_11.gif']").click()
        except:
            driver.find_element_by_xpath("//td[contains(text(), '医疗器械经营企业（备案）')]").click()
            time.sleep(10)
        else:
            break

def get_urls(c):
    c.send(None)
    time.sleep(10)
    # 循环点击下一页
    page_num = 14157

    # 进入第一页
    for _ in range(3):
        try:
            input_page = driver.find_element_by_xpath('//*[@id="goInt"]')
            input_page.clear()
            input_page.send_keys(str(start_page))
            driver.find_element_by_xpath("//input[@src='images/dataanniu_11.gif']").click()
        except:
            driver.find_element_by_xpath("//td[contains(text(), '医疗器械经营企业（备案）')]").click()
            time.sleep(10)
        else:
            break

    for i in range(start_page, page_num+1):

        results = []
        tt = random.random()
        time.sleep(tt if tt > 0.3 else 0.3)

        # 获取页面中的链接
        # 尝试，如果加载不出来则退出
        for j in range(1, 200):
            url_list = driver.find_elements_by_xpath("//div[@id='content']/table[2]/tbody/tr/td/p/a")
            if url_list:
                break
            else:
                print(f'\rinpage {i} retry times: {j}')
                time.sleep(5)

                try:
                    driver.find_element_by_xpath('//span[text()="服务器未返回数据"]')
                except:
                    time.sleep(1)
                else:
                    reopen_the_page(i)

                if j % 20 == 0:
                    reopen_the_page(i)
        else:
            write_current_page(i)
            with open('error.log', 'a') as f:
                f.write(f'医疗器械经营企业（备案） Error in page {i}. {time.ctime()}')
            raise Exception('Page Load Error')

        for url in url_list:
            # 将获取的链接格式化为可用链接
            link = re.sub(r'javas.*?backC,[\'"](.*?)["\'],null\)', lambda m: m.group(1), url.get_attribute('href'))
            link = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/' + link
            results.append(link)

        pros(i, page_num)
        
        # 点击下一页
        try:
            driver.find_element_by_xpath("//img[@src='images/dataanniu_07.gif']").click()
        except Exception as e:
            write_current_page(page)
            raise e

        r = c.send(results)

    c.close()

def save():
    r = ''
    while True:
        results = yield r
        with open('ylba.txt', 'a') as f:
            for i in results:
                f.write(i+'\n')

if __name__ == '__main__':
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    seed_url = ('http://qy1.sfda.gov.cn/datasearchcnda/face3/base.jsp?tableId=132&tableName=TABLE132&title=%D2%BD%C1%C6%C6%F7%D0%B5%C9%FA%B2%FA%C6%F3%D2%B5%A3%A8%D0%ED%BF%C9%A3%A9&bcId=154209313929078698414236686309')

    # profile = FirefoxProfile()
    # 激活手动代理配置（对应着在 profile（配置文件）中设置首选项）
    # profile.set_preference("network.proxy.type", 1)
    # ip及其端口号配置为 http 协议代理

    # profile.set_preference("network.proxy.http", "115.28.148.192")
    # profile.set_preference("network.proxy.http_port", 8118)

    # 所有协议共用一种 ip 及端口，如果单独配置，不必设置该项，因为其默认为 False
    # profile.set_preference("network.proxy.share_proxy_settings", True)

    # 默认本地地址（localhost）不使用代理，如果有些域名在访问时不想使用代理可以使用类似下面的参数设置
    # profile.set_preference("network.proxy.no_proxies_on", "localhost")

    # 以代理方式启动 firefox
    # driver  = webdriver.Firefox(profile)
    with open('error.ini', 'r') as f:
        start_page = int(f.read().strip())

    driver = webdriver.Firefox()
    driver.get(seed_url)
    main()
    c = save()
    get_urls(c)
    driver.close()

    #2214页可能需要补采