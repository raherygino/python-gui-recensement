
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase, BodyLabel, SubtitleLabel, Dialog
from ...components import LabelValue, TableView

class ShowBelieverDialog(Dialog):

    def __init__(self, parent=None):
        super().__init__("Loha-mpianakaviana", "", parent)
        self.setTitleBarVisible(False)
        self.textLayout.removeWidget(self.contentLabel)
        self.gridLayout = QGridLayout()
        self.textLayout.addLayout(self.gridLayout)
        self.textLayout.addWidget(SubtitleLabel("Fianakaviana"))
        self.table = TableView(self)
        self.table.setMinimumHeight(200)
        self.textLayout.addWidget(self.table)
        
    def addLabelValue(self, label:str, value:str, row:int, column:int):
        self.gridLayout.addLayout(LabelValue(label, value), row, column) 
        