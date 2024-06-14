from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget
from qfluentwidgets import ProgressBar
from ....components import TableWidget

class BaseTab(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.__initTableView(parent)
        self.parent = parent
        
    def __initTableView(self, parent):
        self.progressBar = ProgressBar(self)
        self.progressBar.setVisible(False)
        self.tableView = TableWidget(self)
        '''self.tableView.isIncrement = True
        self.tableView.setColumnNoEditable(0,7)'''
        self.vBoxLayout.addWidget(self.progressBar)
        self.vBoxLayout.addWidget(self.tableView)