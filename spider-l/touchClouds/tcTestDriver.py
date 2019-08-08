"""
为提升测试效率，采用该模块代替selenium库
"""

class Element(object):

    text = "Element"

    def click(self):
        print("click")


    def clear(self):
        print("clear")


    def send_keys(self, words):
        print(f"send_keys:{words}")


class TcTestDriver(object):
    """docstring for TcTest"""
    def __init__(self):
        pass


    def get(self, url):
        print(url)


    def set_page_load_timeout(self, seconds):
        pass


    def find_element_by_xpath(self, raise_exception):
        """
        若参数为
        """
        print(raise_exception)
        if raise_exception:
            raise Exception('Xpath error!')
        else:
            return Element()