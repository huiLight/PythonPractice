import time
from selenium import webdriver

# from abc import abstractmethod, ABCMeta


class TouchClouds(object):
    
    driver = webdriver.Chrome()


    def __init__(self):
        self.retry_times = 5
        self.open()


    def init(self):
        """
        抽象方法，由用户实现
        """
        pass


    def open(self):
        """
        接收一个url列表，依次打开，可设置超时时间，重试次数，可重写该方法
        """
        urls = getattr(self, "urls", None)

        if not urls:
            raise Exception('urls not exist.')
        for url in urls:
            self.driver.get(url)
            self.init()


    def click(self, xpath):
        """
        接受一个xpath作为参数，
        点击该元素
        """
        for _ in range(self.retry_times):
            try:
                self.driver.find_element_by_xpath(xpath).click()
            except:
                if _ == self.retry_times-1:
                    raise e
                time.sleep(0.3)


    def input(self, xpath, strings):

        for _ in range(self.retry_times):
            try:
                element = self.driver.find_element_by_xpath(xpath)
            except Exception as e:
                if _ == self.retry_times-1:
                    raise e

                time.sleep(0.3)
            else:
                element.clear()
                element.send_keys(strings)



    def extracted(self, **kw):
        """
        接收一个要获取数据的字典，字典的key是字段名，value是相应的xpath
        """
        pass

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    TouchClouds()