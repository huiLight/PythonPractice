from selenium import webdriver


class CatchClouds(object):

    driver = webdriver.Firefox()

    def __init__(self):
        pass


    def init(self):
        """
        抽象方法，由用户实现
        """
        pass


    @classmethod
    def open(cls, urls):
        """
        接收一个url列表，依次打开，可设置超时时间，重试次数，可重写该方法
        """
        pass


    @classmethod
    def click(cls, xpath):
        """
        接受一个xpath作为参数，
        点击该元素
        """
        driver.find_element_by_xpath(xpath).click()


    @classmethod
    def input(cls, xpath, strings):

        element = driver.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(strings)


    @classmethod
    def extracted(cls, **kw):
        """
        接收一个要获取数据的字典，字典的key是字段名，value是相应的xpath
        """
        pass