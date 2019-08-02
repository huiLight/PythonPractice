from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

import re
import time
import xlwt
from progress import pros



# chrome_options = Options()

# chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
# chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
# chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
# chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
# chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
# (?# chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #手动指定使用的浏览器位置)

def get_page(url):
    for _ in range(82):
        # insure the page is open
        try:
            driver.get(url)
            time.sleep(0.1)
        except:
            if _ == 80:
                with open('contentd.log', 'a') as f:
                    f.write(f"{r},{url}\n")
                break
            time.sleep(3)
            continue
        
        try:
            driver.find_element_by_xpath("//center[1]/h1[contains(text(),'403')]")
        except:
            pass
        else:
            time.sleep(100)
            continue
        
        # insure the data load over
        for __ in range(31):
            try:
                driver.find_element_by_xpath(text1+"许可证编号"+text3)
            except Exception as e:
                print(f'retry {__}', end='\r')
                if _ == 80 and __ == 30:
                    raise e
                time.sleep(__*2)
            else:
                return

    else:
        with open('contentd.log', 'a') as f:
            f.write(f"{r},{url}\n")

def main(urls):
    global r
    filename = 'data'+str(int(start_time))+'.csv'


    urls = urls[r-1 : ]#r+count-1]

    for url in urls:
        # seed_url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=136&tableName=TABLE136&tableView=%E5%8C%BB%E7%96%97%E5%99%A8%E6%A2%B0%E7%BB%8F%E8%90%A5%E4%BC%81%E4%B8%9A%EF%BC%88%E8%AE%B8%E5%8F%AF%EF%BC%89&Id=94195'

        if r % 5000 == 0:
            filename = 'dataa'+str(int(start_time))+'.csv'
            
        get_page(url)

        info = {}
        for title in titles:
            try:
                info[title] = driver.find_element_by_xpath(text1+title+text3)
            except:
                pass

        temp = '{}'.format(r)
        for i in range(len(titles)):
            # 写入excel
            # 参数对应 行, 列, 值
            temp = temp + ',' + info[titles[i]].text.replace('\n', '')
            # worksheet.write(r,i,label=info[titles[i]].text)
            #workbook.save(bookname)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(temp+'\n')
        pros(r, count, start_time, start_num)
        r += 1

def get_start_num():
    # 从文件中获取开始页码，如果文件不存在或文件为空，则返回1
    try:
        with open('content_log.ini', 'r') as f:
            n = f.read().strip()
    except:
        return 1

    if n:
        return int(n)
    return 1

if __name__ == '__main__':

    #禁用图片
    fp = webdriver.FirefoxProfile()
    fp.set_preference('permissions.default.image', 2)#某些firefox只需要这个
    fp.set_preference('browser.migration.version', 9001)#部分需要加上这个
    #禁用css
    # fp = webdriver.FirefoxProfile()
    fp.set_preference('permissions.default.stylesheet', 2)
    #禁用flash
    # fp = webdriver.FirefoxProfile()
    fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    #禁用js
    # fp = webdriver.FirefoxProfile()
    fp.set_preference('javascript.enabled', 'false')
    driver = webdriver.Firefox(firefox_profile=fp)

    time.sleep(3)
    start_time = time.time()

    # bookname = 'ylqxjyxk'+str(int(start_time))+'.xls'
    # sheetname = '医疗器械经营许可'
    r =  get_start_num()
    start_num = r
    count = 98138
    # 创建一个workbook 设置编码
    # workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    # worksheet = workbook.add_sheet(sheetname)



    # driver=webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.Firefox()
    driver.set_page_load_timeout(8)
    titles = [
    '许可证编号','企业名称','法定代表人','企业负责人','住所',
    '经营场所','经营方式','经营范围(2002分类)','经营范围(2017分类)',
    '库房地址','发证部门','发证日期','有效期限','注',]
    text1="//div[@class='listmain']/div/table[1]/tbody/tr/td[text()='"
    text3="']/following-sibling::td"

    # for i in range(len(titles)):
    #    worksheet.write(0,i,label=titles[i])



    with open('ylqxjyxk.txt', 'r') as f:
        urls = f.readlines()

    try:
        main(urls)
    except Exception as e:
        with open('content_log.ini', 'w') as f:
            f.write(str(r))
     #   workbook.save(bookname)
        raise e


    # 保存
    # workbook.save(bookname)
    # content = driver.find_element_by_xpath("//div[@class='listmain']/div/table[1]/tbody/tr/td[text()='许可证编号']/following-sibling::td").text
    # content2 = driver.find_element_by_xpath("//div[@class='listmain']/div/table[1]/tbody/tr/td[text()='企业名称']/following-sibling::td").text



    driver.close()
    input('Press any key to quite.')

    #10 80
