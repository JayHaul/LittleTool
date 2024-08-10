# coding:utf-8
import qfluentwidgets
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog

from ..components.customAddFolderButton import FolderListSettingCard, TextListSettingCard
from ..common.config import cfg
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet


class SettingInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        
        self.settingLabel = QLabel(self.tr("配置"), self)

        # 数据目录
        self.dataReadGroup = SettingCardGroup(
            self.tr("数据读取目录"), self.scrollWidget)
        self.dataReadFolderCard = FolderListSettingCard(
            cfg.dataReadFolders,
            self.tr("数据读取目录列表"),
            directory=QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DesktopLocation),
            parent=self.dataReadGroup
        )
        self.fileSuffixCard = TextListSettingCard(
            cfg.fileSuffix,
            self.tr("文件后缀列表"),
            parent=self.dataReadGroup
        )
        self.saveFolderCard = PushSettingCard(
            self.tr('选择目录'),
            FIF.DOWNLOAD,
            self.tr("数据保存目录"),
            cfg.get(cfg.saveFolder),
            self.dataReadGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)


        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # add cards to group
        self.dataReadGroup.addSettingCard(self.dataReadFolderCard)
        self.dataReadGroup.addSettingCard(self.fileSuffixCard)
        self.dataReadGroup.addSettingCard(self.saveFolderCard)

       

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.dataReadGroup)


    def __saveFolderCardClicked(self):
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("选择文件夹"), "./")
        if not folder or cfg.get(cfg.saveFolder) == folder:
            return

        cfg.set(cfg.saveFolder, folder)
        self.saveFolderCard.setContent(folder)

        self.saveFolderCard.clicked.connect(
            self.__saveFolderCardClicked)

    def __connectSignalToSlot(self):
        """ connect signal to slot """

        # music in the pc
        self.saveFolderCard.clicked.connect(
            self.__saveFolderCardClicked)

     

