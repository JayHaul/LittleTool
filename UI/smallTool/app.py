# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QTranslator
from PyQt6.QtWidgets import QApplication

from view.main_window import MainWindow
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
    app.setStyle("fusion")

def handle_exception(exc_type, exc_value, exc_traceback):
    # 这里是异常处理函数，你可以自定义打印异常信息的方式
    print("Uncaught exception:", exc_type, exc_value)
    sys.__excepthook__(exc_type, exc_value, exc_traceback)  # 调用原始的异常处理函数


galleryTranslator = QTranslator()

app.installTranslator(galleryTranslator)

w = MainWindow()
w.show()

sys.exit(app.exec())