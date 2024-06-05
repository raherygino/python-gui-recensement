from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ProgressBar
from ....components import TableView

class StudentTab(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.__initTableView(parent)
        self.parent = parent
        
    def __initTableView(self, parent):
        self.progressBar = ProgressBar(self)
        self.progressBar.setVisible(False)
        self.tableView = TableView(self)
        
        self.vBoxLayout.addWidget(self.progressBar)
        self.vBoxLayout.addWidget(self.tableView)