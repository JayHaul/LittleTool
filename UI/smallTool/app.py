# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QTranslator
from PyQt6.QtWidgets import QApplication

from view.main_window import MainWindow


# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
    app.setStyle("fusion")



galleryTranslator = QTranslator()

app.installTranslator(galleryTranslator)

w = MainWindow()
w.show()

app.exec()