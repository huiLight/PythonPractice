"""
为提升测试效率，采用该模块代替selenium库
"""

class Element(object):

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


    def find_element_by_xpath(self, raise_exception):
        """
        若参数为
        """
        if raise_exception:
            raise Exception('Xpath error!')
        else:
            return Element()