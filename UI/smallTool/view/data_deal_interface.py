# coding:utf-8
import sys

from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout

from ..common.config import cfg
from ..common.utils import get_file_from_folders
from ..components.dataGrid import DataGrid

class DataDealInterface(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName('DateDealInterface')
        self.vBoxLayout = QVBoxLayout(self)
        data = get_file_from_folders(directorys=cfg.dataReadFolders.value, suffixes=cfg.fileSuffix.value)
        
        self.header = ['文件名', '文件路径', '文件后缀', '分组', '操作']
        
        self.tableView = DataGrid(data, self.header)
        
        
        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        self.vBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.vBoxLayout.addWidget(self.tableView)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DataDealInterface()
    w.show()
    app.exec()