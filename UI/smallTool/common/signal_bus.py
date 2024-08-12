# coding: utf-8
from qfluentwidgets import FluentIcon
from PyQt6.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ pyqtSignal bus """
    
    switchToSampleCard = pyqtSignal(str, int)
    micaEnableChanged = pyqtSignal(bool)
    supportSignal = pyqtSignal()
    
    update_button_icon_signal = pyqtSignal(int, FluentIcon)

signalBus = SignalBus()