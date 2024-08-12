# coding: utf-8
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationItemPosition, FluentWindow,
                            SplashScreen)

from UI.smallTool.common.signal_bus import signalBus
from UI.smallTool.common.translator import Translator
from UI.smallTool.view.data_deal_interface import DataDealInterface
from UI.smallTool.view.setting_interface import SettingInterface
from UI.smallTool.view.scatters_interface import ScattersInterface


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        
        #Create sub interface
        self.data_deal_interface = DataDealInterface()
        self.setting_interface = SettingInterface()
        self.scatters_interface = ScattersInterface()

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowTitle('小工具')


        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        # signalBus.switchToSampleCard.connect(self.switchToSample)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        # self.addSubInterface(self.data_deal_interface, FIF.HOME, 'Home')
        self.addSubInterface(self.data_deal_interface, FIF.PENCIL_INK, '数据处理')
        # self.addSubInterface(self.data_deal_interface, FIF.PENCIL_INK, '视频管理')
        self.addSubInterface(self.scatters_interface, FIF.PENCIL_INK, '散点图')
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL

        # add custom widget to bottom
        self.addSubInterface(
            self.setting_interface, FIF.SETTING, self.tr('设置'), NavigationItemPosition.BOTTOM)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    # def switchToSample(self, routeKey, index):
    #     """ switch to sample """
    #     interfaces = self.findChildren(DataDealInterface)
    #     for w in interfaces:
    #         if w.objectName() == routeKey:
    #             self.stackedWidget.setCurrentWidget(w, False)
    #             w.scrollToCard(index)