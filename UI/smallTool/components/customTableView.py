import PIL.DdsImagePlugin
import PyQt6.QtGui
from qfluentwidgets import TableWidget
import math
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import PyQt6.QtWidgets
import qfluentwidgets
from qfluentwidgets import TableWidget, HorizontalPipsPager, PipsScrollButtonDisplayMode, HorizontalPipsPager, RoundMenu, setTheme, Theme, Action, MenuAnimationType, MenuItemDelegate, CheckableMenu, MenuIndicatorType
from PyQt6.QtWidgets import QTableWidgetItem, \
    QHeaderView, QWidget, QVBoxLayout
from qfluentwidgets import FluentIcon as FIF




class CustomTableView(TableWidget):
    subMenu = False
    
    def item_clicked(self, item):
        # 在这里处理单击事件
        print(f"Item clicked: {self.item(item.row(), 0).text()}")

        print(f"Item clicked: {item.row()}")
   
    def mousePressEvent(self, event):
        if self.subMenu:
            return
        self.subMenu = not self.subMenu
        if event.button() == Qt.MouseButton.LeftButton:
            item = self.itemAt(event.pos())
            
            if item:
                
                print(f"Item clicked: {self.item(item.row(), 0).text()}")
                print(f"Item clicked: {item.row()}")
            self.subMenu = not self.subMenu
            
        elif event.button() == Qt.MouseButton.RightButton:
            item = self.itemAt(event.pos())
            if item:
                self.deal_action.setData(item)
                # show menu
                self.menu.exec(self.mapToGlobal(event.pos()), aniType=MenuAnimationType.DROP_DOWN)
                print("Right mouse button pressed")
            self.subMenu = not self.subMenu
                
        elif event.button() == Qt.MouseButton.MiddleButton:
            print("Middle mouse button pressed")
            self.subMenu = not self.subMenu
        else:
            print("Unknown mouse button pressed")
            self.subMenu = not self.subMenu
        super().mousePressEvent(event)

    def operate_event(self):
        item = self.deal_action.data()
        print(f"Item right clicked: {self.item(item.row(), 0).text()}")
        
        self.deal_action.setData(None)

    def copy_event(self):
        import pandas.io.clipboard as cb
        item = self.deal_action.data()
        cb.copy(item.text())

        self.copy_action.setData(None)
        
    def __init__(self, header):
        super().__init__()
        self.copy_action = Action(FIF.COPY, '复制')
        self.deal_action = Action(FIF.DEVELOPER_TOOLS, '处理')
        self.view_action = Action(FIF.VIEW, '查看')
        self.menu = RoundMenu(parent=self)
        self.deal_action.triggered.connect(self.operate_event)
        self.copy_action.triggered.connect(self.copy_event)
        # add actions
        
        self.menu.addAction(self.copy_action)
        self.menu.addAction(self.deal_action)
        
        self.menu.addAction(Action(FIF.DELETE, '删除'))

        
        self.setBorderVisible(True)
        self.setBorderRadius(8)
    
        self.setWordWrap(True)
        self.setRowCount(10)
        self.setColumnCount(len(header))
    
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
        self.setHorizontalHeaderLabels(header)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setSortingEnabled(True)