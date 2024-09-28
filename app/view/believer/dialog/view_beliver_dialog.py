from PyQt5.QtWidgets import QHBoxLayout, QWidget, QGridLayout, QAbstractItemView, QVBoxLayout
from qfluentwidgets import SubtitleLabel
from ....components import BigDialog, LabelValue, TableView
from ....models import Believer
from ....common import Function

class ViewBelieverDialog(BigDialog):
    
    def __init__(self, parent=None):
        super().__init__("Loha-mpianakaviana", parent)
        
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(14)
        self.contentLayout.addLayout(self.gridLayout)
        self.row = QVBoxLayout()
        self.contentLayout.addLayout(self.row)
        self.contentLayout.addWidget(SubtitleLabel("Fianakaviana"))
        self.table = TableView(self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setMinimumHeight(200)
        self.contentLayout.addWidget(self.table)
        
    def addLayout(self, layout):
        self.row.addLayout(layout)
        
    def addNewLabelValue(self, label:str, value:str):
        self.row.addLayout(LabelValue(label, value))
    
    def addLabelValue(self, label:str, value:str, row:int, column:int):
        self.gridLayout.addLayout(LabelValue(label, value), row, column) 