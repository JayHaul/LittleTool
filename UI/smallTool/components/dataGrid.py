import math

import asyncio
import PyQt6.QtGui
import PyQt6.QtWidgets
import qfluentwidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, \
    QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import PipsScrollButtonDisplayMode, HorizontalPipsPager

import UI.smallTool.common.utils
from ..components.customTableView import CustomTableView
from ..service.dataService.Zero import Zero
from UI.smallTool.common.utils import AsyncWorker
import logging

log = logging.getLogger(__name__)

def get_page(data, page, page_size):
    start = (page - 1) * page_size
    end = start + page_size
    return data[start:end]


class DataGrid(QWidget):
    def __init__(self, datas, header):
        super().__init__()
        self.currentPage = 1
        self.datas = datas
        self.header_length = len(header)
        self.__init_data_grid(header, datas)
    
    

    
    def show_deal_dialog(self, index):
        self.message_box = qfluentwidgets.MessageBoxBase(self)
        self.method_comboBox = qfluentwidgets.ComboBox()
        self.method_comboBox.addItems(['Zero'])
        self.method_comboBox.setCurrentIndex(1)
        self.method_comboBox.setPlaceholderText("请选择处理方案")
        self.message_box.viewLayout.addWidget(self.method_comboBox)
        self.message_box.yesButton.setText('应用')
        self.message_box.cancelButton.setText('取消')
        self.message_box.yesButton.clicked.connect(lambda: self.apply_deal_method(index, self.method_comboBox.currentIndex()))
        self.message_box.exec()

    def apply_deal_method(self, index, method_index):
        # self.method_comboBox.currentIndex()
        async def apply_Zero(index, batch_id = 0):
            await Zero(self.tableView.item(index, 1).text(), batch_id).execute()
        if method_index == 0:
            loop = asyncio.new_event_loop()
            # 创建 AsyncWorker 实例
            worker = AsyncWorker(loop)
            # 连接 finished 信号
            worker.finished.connect(lambda: self.deal_finished())
            # 执行异步函数
            worker.execute_async(apply_Zero(index))
            
            a = self.tableView.item(index, 4)
            pass 
            
    def deal_finished(self):
        log.debug("处理完成")
    def __init_data_grid(self, header, datas):
        self.vBoxLayout = QVBoxLayout(self)

        self.tableView = CustomTableView(header)

        self.hPagination = HorizontalPipsPager()
        self.hPagination.setPageNumber(math.ceil(len(datas) / 10))
        self.hPagination.setVisibleNumber(10)
        self.hPagination.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        self.hPagination.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        self.hPagination.currentItemChanged.connect(self.update_data)

        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        self.vBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.vBoxLayout.addWidget(self.tableView)
        self.vBoxLayout.setStretchFactor(self.tableView, 85)

        self.vBoxLayout.addWidget(self.hPagination)
        self.vBoxLayout.setStretchFactor(self.hPagination, 15)
        self.vBoxLayout.setAlignment(self.hPagination, Qt.AlignmentFlag.AlignHCenter)
        self.model = PyQt6.QtGui.QStandardItemModel()
        self.tableView.clearContents()
        
        for i, data in enumerate(get_page(self.datas, self.currentPage, 10)):
            # 设置分组栏
            group_box = QWidget(self)
            group_layout = QHBoxLayout(self)
            group_layout.addWidget(qfluentwidgets.EditableComboBox(self))
            group_box.setLayout(group_layout)
            
            # 设置操作栏
            operate_box = QWidget(self)
            operate_layout = QHBoxLayout(self)
            deal_button = qfluentwidgets.PrimaryToolButton(FIF.EDIT ,self)
            def make_callback(idx):
                return lambda: self.show_deal_dialog(idx)
            deal_button.clicked.connect(make_callback(i))
            
            operate_layout.addWidget(deal_button)
            operate_box.setLayout(operate_layout)
            
            self.tableView.setItem(i, 0, QTableWidgetItem(data.file_name))
            self.tableView.setItem(i, 1, QTableWidgetItem(data.full_path))
            self.tableView.setItem(i, 2, QTableWidgetItem(data.file_suffix))
            self.tableView.setCellWidget(i,3, group_box)
            self.tableView.setCellWidget(i,4, operate_box)





    def update_data(self):
        index = self.hPagination.currentRow()
        self.tableView.clearContents()
        self.currentPage = index + 1
        for i, data in enumerate(get_page(self.datas, self.currentPage, 10)):
            for j in range(self.header_length):
                self.tableView.setItem(i, j, QTableWidgetItem(data))