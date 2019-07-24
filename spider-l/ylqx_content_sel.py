from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re
import time
import xlwt
from progress import pros



chrome_options = Options()

chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错
# chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
# (?# chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #手动指定使用的浏览器位置)



def main(urls):
    global r

    urls = urls[start_num:]

    for url in urls:
        # seed_url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=136&tableName=TABLE136&tableView=%E5%8C%BB%E7%96%97%E5%99%A8%E6%A2%B0%E7%BB%8F%E8%90%A5%E4%BC%81%E4%B8%9A%EF%BC%88%E8%AE%B8%E5%8F%AF%EF%BC%89&Id=94195'

        driver.get(url)

        # 确保网页已加载完成
        for _ in range(10):
            try:
                driver.find_element_by_xpath(text1+"许可证编号']")
            except:
                time.sleep(3)
                driver.get(url)
            else:
                break
        else:
            with open('content.log', 'a') as f:
                f.write(f"{r},{url}\n")

        info = {}
        for title in titles:
            try:
                info[title] = driver.find_element_by_xpath(text1+title+text3)
            except:
                pass
            
        for i in range(len(titles)):
            # 写入excel
            # 参数对应 行, 列, 值
            worksheet.write(r,i,label=info[titles[i]].text)
            workbook.save(bookname)
        pros(r, 98138)
        r += 1

def get_start_num():
    with open('content_log.ini', 'r') as f:
        n = f.read().strip()
    return int(n)

if __name__ == '__main__':

    bookname = 'ylqxjyxk.xls'
    sheetname = '医疗器械经营许可'
    r = get_start_num()

    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet(sheetname)



    driver=webdriver.Chrome(chrome_options=chrome_options)


    titles = [
    '许可证编号','企业名称','法定代表人','企业负责人','住所',
    '经营场所','经营方式','经营范围(2002分类)','经营范围(2017分类)',
    '库房地址','发证部门','发证日期','有效期限','注',]
    text1="//div[@class='listmain']/div/table[1]/tbody/tr/td[text()='"
    text3="']/following-sibling::td"

    for i in range(len(titles)):
        worksheet.write(0,i,label=titles[i])



    with open('ylqxjyxk.txt', 'r') as f:
        urls = f.readlines()

    try:
        main(urls)
    except Exception as e:
        with open('content_log.ini', 'w') as f:
            f.write(str(r))
        workbook.save(bookname)
        raise e


    # 保存
    workbook.save(bookname)
    # content = driver.find_element_by_xpath("//div[@class='listmain']/div/table[1]/tbody/tr/td[text()='许可证编号']/following-sibling::td").text
    # content2 = driver.find_element_by_xpath("//div[@class='listmain']/div/table[1]/tbody/tr/td[text()='企业名称']/following-sibling::td").text



    driver.close()
