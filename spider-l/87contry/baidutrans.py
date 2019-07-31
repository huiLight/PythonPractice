import xlrd
import time
import pyperclip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

bkname = '20181120.xlsx'

src = xlrd.open_workbook(bkname)
table = src.sheets()[0]

l = table.col_values(4, start_rowx=7280, end_rowx=14400)   #返回由该列中所有单元格的数据组成的列表
surl = 'https://fanyi.baidu.com/#en/zh/Local%20news%20on%20the%20Far%20South%20Coast%20of%20NSW.%20Country%20of%20origin%3A%20Australia'
driver = webdriver.Firefox()
driver.get(surl)
time.sleep(10)

r = 7281
for a in l:
    if not a:
        with open('ok.csv', 'a', encoding='utf-8') as f:
            f.write(str(r)+',\n')
        r += 1
        continue
    te = driver.find_element_by_xpath("//textarea[@id='baidu_translate_input']")
    te.clear()
    te.send_keys(a)
    time.sleep(2)
    trans = driver.find_element_by_xpath("//a[@id='translate-button']")
    trans.click()

    for _ in range(10):
        try:
            co = driver.find_element_by_xpath("//a[@class='operate-btn op-copy data-hover-tip']")
            co.click()
        except:
            time.sleep(5)
        else:
            break


    with open('ok.csv', 'a', encoding='utf-8') as f:
        f.write(str(r)+','+pyperclip.paste()+'\n')
    r += 1