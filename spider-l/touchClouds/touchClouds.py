import time
from selenium import webdriver

# from abc import abstractmethod, ABCMeta


class TouchClouds(object):
    


    def __init__(self, test_mode=False):
        self.retry_times = 5
        # The page load timeout seconds.
        # Todo:: move the items of setting to setting.py and load them from it.
        self.load_timeout = 8
        if test_mode:
            from tcTestDriver import TcTestDriver
            self.driver = TcTestDriver()
        else:
            self.driver = webdriver.Chrome()

        self.driver.set_page_load_timeout(self.load_timeout)
        # self.open()


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
            self.url = url
            self.execute(self.driver.get, url)
            self.init()


    def click(self, xpath):
        """
        接受一个xpath作为参数，
        点击该元素
        """
        self.execute(self.driver.find_element_by_xpath, xpath).click()


    def input(self, xpath, strings):

        element = self.execute(self.driver.find_element_by_xpath, xpath)
        element.clear()
        element.send_keys(strings)


    def get_text(self, xpath):
        element = self.execute(self.driver.find_element_by_xpath, xpath, retry_times=1)
        return element.text.strip()


    def extracted(self, kw):
        """
        接收一个要获取数据的字典，字典的key是字段名，value是相应的xpath
        """
        if not isinstance(kw, dict):
            raise Exception("kw must is a dict.")
        results = {}
        for k, v in kw.items():
            result[k] = self.get_text(v)


        return results

    def execute(self, fun, *args, retry_times=None):
        """
        将重试提取出来，接收函数和参数列表
        当超过重试次数后，将错误信息写入日志，并将异常抛出
        args:: fun 要执行的函数名
        args:: args 传递给function的参数
        return:: function执行结果
        """
        if retry_times is None:
            retry_times = self.retry_times

        for _ in range(retry_times):
            try:
                result = fun(*args)
            except Exception as e:
                if _ == self.retry_times-1:
                    # TODO:: write the error message into log
                    log_file_name = getattr(self, "name", 'touchClouds') + '.log'
                    with open(log_file_name, 'a', encoding='utf-8') as f:
                        f.write("{}, {}, {}\n".format(self.url, str(e).replace('\n', '\t'),time.strftime('%Y-%m-%d %H:%M:%S')))
                    raise e
                time.sleep(0.3)
            else:
                return result

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    # TouchClouds()
    tc = TouchClouds(test_mode = True)
    # tc.click(True)
    tc.urls = ['www.baidu.com', 'google.com']
    tc.open()
    tc.input(True, "Hello")