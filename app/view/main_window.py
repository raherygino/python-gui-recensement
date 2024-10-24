# coding: utf-8
from PyQt5.QtCore import QUrl, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QVBoxLayout

from qfluentwidgets import NavigationItemPosition, FluentWindow, FluentStyleSheet, \
                           SplashScreen, TitleLabel, Dialog, BodyLabel, FluentIcon
from qframelesswindow import TitleBar
from .setting_interface import SettingInterface
from ..common.config import ZH_SUPPORT_URL, EN_SUPPORT_URL, cfg
from ..common.signal_bus import signalBus
from ..components import ConfirmDialog

from ..models import BelieverModel
from . import ListBelieverInterface, AddBelieverInterface
from ..presenter import BelieverPresenter

class FluentTitleBar(TitleBar):
    """ Fluent title bar"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(48)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.hBoxLayout.removeWidget(self.closeBtn)

        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertWidget(0, self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.subtitleLabel = BodyLabel(self)
        self.hBoxLayout.insertWidget(1, self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.hBoxLayout.insertWidget(2, self.subtitleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.titleLabel.setObjectName('titleLabel')
        self.subtitleLabel.setObjectName('subtitleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.maxBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))
        
class MainWindow(FluentWindow):
    
    currentPromotion = pyqtSignal(int)
    refresh = pyqtSignal(list)
    subjectRefresh = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.listBelieverInterface = ListBelieverInterface(self)
        self.addBelieverInterface = AddBelieverInterface(self)
        #self.settingInterface = SettingInterface(self)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.connectSignalToSlot()

        self.believerModel = BelieverModel()
        self.believerPresenter = BelieverPresenter(self.believerModel, self.addBelieverInterface, self.listBelieverInterface)
       
        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.listBelieverInterface, FluentIcon.DOCUMENT, "Lisitra")
        self.addSubInterface(self.addBelieverInterface, FluentIcon.ADD, "Mampiditra")
        
        self.navigationInterface.addSeparator()
       
        '''self.addSubInterface(
            self.settingInterface, FluentIcon.SETTING, 'Paramètres', NavigationItemPosition.BOTTOM)'''
        

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
        self.fluentTitleBar = FluentTitleBar(self)
        self.fluentTitleBar.setIcon(QIcon('app/resource/images/icon.png'))
        self.fluentTitleBar.titleLabel.setText('Recensement')
        self.setTitleBar(self.fluentTitleBar)

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIcon(QIcon('app/resource/images/icon.png'))
        self.splashScreen.setIconSize(QSize(240, 240))
        self.splashScreen.raise_()
        
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.showMaximized()
        QApplication.processEvents()

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(ZH_SUPPORT_URL))
        else:
            QDesktopServices.openUrl(QUrl(EN_SUPPORT_URL))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())
    
    def closeEvent(self, event):
        dialog = ConfirmDialog('Akatona', 'Akatona marina ve?',self)
        dialog.yesBtn.setText("Eny")
        dialog.cancelBtn.setText("Tsia")
        if dialog.exec():
            event.accept()
        else:
            event.ignore()