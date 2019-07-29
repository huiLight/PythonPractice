from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton,QLineEdit,
                            QGridLayout, QApplication)

import sys
import pyperclip
import time


class FormatString(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def product_value(self):
        l = self.t1.text()
        t = l.replace('/','-')
        t = t + '-' + str(int(time.strftime('%m%d')))
        self.t2.setText(t+'-l.js')
        self.t3.setText(t+'-c.js')
        self.t4.setText(t+'-y.js')
        self.t5.setText(t+'-m')

    def initUI(self):

        pre = QLabel('待处理')
        format1 = QLabel('链接')
        format2 = QLabel('内容')
        format3 = QLabel('源码')
        format4 = QLabel('模板')

        self.t1 = QLineEdit()
        # 按下回车时触发事件
        self.t1.returnPressed.connect(self.product_value)

        self.t2 = QLineEdit()
        self.t3 = QLineEdit()
        self.t4 = QLineEdit()
        self.t5 = QLineEdit()

        b1 = QPushButton('生成')
        b2 = QPushButton('复制')
        b3 = QPushButton('复制')
        b4 = QPushButton('复制')
        b5 = QPushButton('复制')
        b1.clicked.connect(self.product_value)
        b2.clicked.connect(lambda : pyperclip.copy(self.t2.text()))
        b3.clicked.connect(lambda : pyperclip.copy(self.t3.text()))
        b4.clicked.connect(lambda : pyperclip.copy(self.t4.text()))
        b5.clicked.connect(lambda : pyperclip.copy(self.t5.text()))



        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(pre, 1, 0)
        grid.addWidget(self.t1, 1, 1)
        grid.addWidget(b1, 1, 2)

        grid.addWidget(format1, 2, 0)
        grid.addWidget(self.t2, 2, 1)
        grid.addWidget(b2, 2, 2)

        grid.addWidget(format2, 3, 0)
        grid.addWidget(self.t3, 3, 1)
        grid.addWidget(b3, 3, 2)

        grid.addWidget(format3, 4, 0)
        grid.addWidget(self.t4, 4, 1)
        grid.addWidget(b4, 4, 2)

        grid.addWidget(format4, 5, 0)
        grid.addWidget(self.t5, 5, 1)
        grid.addWidget(b5, 5, 2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 380, 220)
        self.setWindowTitle('FormatString')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FormatString()
    sys.exit(app.exec_())