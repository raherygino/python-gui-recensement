from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ProgressBar, Theme
from ....components import TableView
from ....common.config import OptionsConfigItem, cfg

class StudentTab(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.__initTableView(parent)
        self.parent = parent
        self.parent.nParent.settingInterface.themeCard.optionChanged.connect(self.themeChanged)
        self.parent.nParent.settingInterface.themeColorCard.colorChanged.connect(self.colorChanged)
        #optionChanged
        
    def colorChanged(self, color):
        self.tableView.setQss(cfg.get(cfg.theme))
        
    def themeChanged(self, item: OptionsConfigItem):
        #colorChanged
        self.tableView.setQss(str(item.value).replace('Theme.', ''))
        
    def __initTableView(self, parent):
        self.progressBar = ProgressBar(self)
        self.progressBar.setVisible(False)
        self.tableView = TableView(self)
        self.tableView.isIncrement = True
        self.tableView.setColumnNoEditable(0,7)
        self.vBoxLayout.addWidget(self.progressBar)
        self.vBoxLayout.addWidget(self.tableView)