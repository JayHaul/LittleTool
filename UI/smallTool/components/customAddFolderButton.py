# coding:utf-8
from typing import List, Union
from pathlib import Path

import qfluentwidgets
import qfluentwidgets.components.settings.folder_list_setting_card
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPainter, QIcon
from PyQt6.QtWidgets import (QPushButton, QFileDialog, QWidget, QLabel,
                             QHBoxLayout, QToolButton, QSizePolicy)
from PyQt6.QtSvg import QSvgRenderer

from qfluentwidgets.components.widgets.button import ToolButton, PushButton
from qfluentwidgets.common.config import ConfigItem, qconfig
from qfluentwidgets.common.icon import drawIcon, FluentIconBase
from qfluentwidgets.common.icon import FluentIcon as FIF
from qfluentwidgets.components.dialog_box.dialog import Dialog
from qfluentwidgets.components.settings.expand_setting_card import ExpandSettingCard


class TextItem(QWidget):
    """ Folder item """

    removed = pyqtSignal(QWidget)

    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.hBoxLayout = QHBoxLayout(self)
        self.folderLabel = QLabel(text, self)
        self.removeButton = ToolButton(FIF.CLOSE, self)

        self.removeButton.setFixedSize(39, 29)
        self.removeButton.setIconSize(QSize(12, 12))

        self.setFixedHeight(53)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.hBoxLayout.setContentsMargins(48, 0, 60, 0)
        self.hBoxLayout.addWidget(self.folderLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.removeButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.removeButton.clicked.connect(
            lambda: self.removed.emit(self))


class FolderListSettingCard(ExpandSettingCard):
    """ Folder list setting card """

    folderChanged = pyqtSignal(list)

    def __init__(self, configItem, title, content=None, directory="./", parent=None):
        """
        Parameters
        ----------
        configItem: RangeConfigItem
            configuration item operated by the card

        title: str
            the title of card

        content: str
            the content of card

        directory: str
            working directory of file dialog

        parent: QWidget
            parent widget
        """
        super().__init__(FIF.FOLDER, title, content, parent)
        self.configItem = configItem
        self._dialogDirectory = directory
        self.addFolderButton = PushButton(self.tr('添加新文件夹'), self, FIF.FOLDER_ADD)

        self.folders = qconfig.get(configItem).copy()   # type:List[str]
        self.__initWidget()

    def __initWidget(self):
        self.addWidget(self.addFolderButton)

        # initialize layout
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        for folder in self.folders:
            self.__addFolderItem(folder)

        self.addFolderButton.clicked.connect(self.__showFolderDialog)

    def __showFolderDialog(self):
        """ show folder dialog """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), self._dialogDirectory)

        if not folder or folder in self.folders:
            return

        self.__addFolderItem(folder)
        self.folders.append(folder)
        qconfig.set(self.configItem, self.folders)
        self.folderChanged.emit(self.folders)

    def __addFolderItem(self, folder):
        """ add folder item """
        item = qfluentwidgets.components.settings.folder_list_setting_card.FolderItem(folder, self.view)
        item.removed.connect(self.__showConfirmDialog)
        self.viewLayout.addWidget(item)
        item.show()
        self._adjustViewSize()

    def __showConfirmDialog(self, item):
        """ show confirm dialog """
        name = Path(item.folder).name
        title = self.tr('确认移除目录')
        content = self.tr("移除 ") + f'"{name}"' + \
                  self.tr(" 目录并不会删除该文件夹 ")
        w = Dialog(title, content, self.window())
        w.yesSignal.connect(lambda: self.__removeFolder(item))
        w.exec()

    def __removeFolder(self, item):
        """ remove folder """
        if item.folder not in self.folders:
            return

        self.folders.remove(item.folder)
        self.viewLayout.removeWidget(item)
        item.deleteLater()
        self._adjustViewSize()

        self.folderChanged.emit(self.folders)
        qconfig.set(self.configItem, self.folders)


class TextListSettingCard(ExpandSettingCard):
    """ Text list setting card """

    textChanged = pyqtSignal(list)

    def __init__(self,  configItem, title, content=None, parent=None):
        """
        Parameters
        ----------
        configItem: RangeConfigItem
            configuration item operated by the card

        title: str
            the title of card

        content: str
            the content of card

        directory: str
            working directory of file dialog

        parent: QWidget
            parent widget
        """
        super().__init__(FIF.EDIT, title, content, parent)
        self.configItem = configItem
        self.addTextButton = PushButton(self.tr('添加字符串'), self, FIF.EDIT)

        self.texts = qconfig.get(configItem).copy()   # type:List[str]
        self.__initWidget()

    def __initWidget(self):
        self.addWidget(self.addTextButton)

        # initialize layout
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        for text in self.texts:
            self.__addTextItem(text)

        self.addTextButton.clicked.connect(self.__showTextDialog)

    def __addTextItem(self, text):
        """ add folder item """
        item = TextItem(text, self.view)
        item.removed.connect(self.__showConfirmDialog)
        self.viewLayout.addWidget(item)
        item.show()
        self._adjustViewSize()
    def __showTextDialog(self):
        self.message_diag = qfluentwidgets.MessageBoxBase(self.parent().parent())
        self.message_diag.suffixLineEdit = qfluentwidgets.LineEdit(self)

        self.message_diag.suffixLineEdit.setPlaceholderText('输入文件后缀')
        self.message_diag.suffixLineEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.message_diag.viewLayout.addWidget(qfluentwidgets.SubtitleLabel('添加文件后缀', self))
        self.message_diag.viewLayout.addWidget(self.message_diag.suffixLineEdit)

        # change the text of button
        self.message_diag.yesButton.setText('添加')
        self.message_diag.cancelButton.setText('取消')

        self.message_diag.widget.setMinimumWidth(350)
        self.message_diag.yesButton.clicked.connect(lambda: self.texts.append(self.message_diag.suffixLineEdit.text()) if self.message_diag.suffixLineEdit.text() else None)
        if self.message_diag.exec():
            text = self.message_diag.suffixLineEdit.text()

            self.__addTextItem(text)
            qconfig.set(self.configItem, self.texts)
            self.textChanged.emit(self.texts)


    def __showConfirmDialog(self, item):
        """ show confirm dialog """
        name = item.text
        title = self.tr('确认移除?')
        content = self.tr("移除 ") + f'"{name}"' + \
                  self.tr(" 后缀名 ")
        w = Dialog(title, content, self.window())
        w.yesSignal.connect(lambda: self.__removeItem(item))
        w.exec()

    def __removeItem(self, item):
        if item.text not in self.texts:
            return

        self.texts.remove(item.text)
        self.viewLayout.removeWidget(item)
        item.deleteLater()
        self._adjustViewSize()

        self.textChanged.emit(self.texts)
        qconfig.set(self.configItem, self.texts)