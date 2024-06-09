from PyQt5.QtWidgets import QHBoxLayout

from qfluentwidgets import Dialog, SubtitleLabel, LineEdit, ComboBox, PrimaryPushButton, PushButton, FluentIcon
from ....common.functions import Function
from ....components.table_view import TableView
from ....components import SpinBoxEditWithLabel

class NewSubjectDialog(Dialog):

    def __init__(self, parent=None):
        super().__init__("Matières", "", parent)
        self.setTitleBarVisible(False)
        self.contentLabel.setVisible(False)
        
        self.row = QHBoxLayout()
        self.count = SpinBoxEditWithLabel("Nombre de matières")
        self.count.spinbox.setValue(1)
        self.count.spinbox.textChanged.connect(self.__countChange)
        
        self.table = TableView(self)
        self.table.setHorizontalHeaderLabels(["Abréviation", "Rubrique", "Coeff"])
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        self.table.setMinimumHeight(300)
        
        self.yesBtn = PrimaryPushButton("Ok")
        #self.yesBtn.clicked.connect(self.yesBtnClicked)
        self.cancelBtn = PushButton("Annuler")
        self.cancelBtn.clicked.connect(self.yesBtnClicked)
        
        self.textLayout.addLayout(self.count)
        self.textLayout.addWidget(self.table)
        
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        
        self.buttonLayout.addWidget(self.yesBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        
        self.setFixedWidth(450)

    def __countChange(self, value):
        self.table.setRowCount(int(value))

    def yesBtnClicked(self):
        self.close()

        