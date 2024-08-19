from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent

from qfluentwidgets import Dialog, Action, RoundMenu, MenuAnimationType, FluentIcon, ToolButton, FluentStyleSheet
from ...components import BigDialog, LineEditWithLabel, ComboxEditWithLabel

class AddStudentDialog(BigDialog):
    
    def __init__(self, parent=None):
        super().__init__('Elève', parent)
        self.row = QHBoxLayout()
        self.matriculeEdit = LineEditWithLabel("Matricule")
        self.matriculeEdit.lineEdit.textChanged.connect(lambda: self.__isValid(None))
        
        self.row_2 = QHBoxLayout()
        self.lastnameEdit = LineEditWithLabel("Nom")
        self.lastnameEdit.lineEdit.textChanged.connect(lambda: self.__isValid(None))
        self.firstnameEdit = LineEditWithLabel("Prénoms")
        
        self.row.addLayout(self.matriculeEdit)
        self.row_2.addLayout(self.lastnameEdit)
        self.row_2.addLayout(self.firstnameEdit)
        
        self.row_3 = QHBoxLayout()
        self.genderEdit = ComboxEditWithLabel("Genre", ['M','F'])
        self.gradeEdit = ComboxEditWithLabel("Grade", ["EIP", "EAP"])
        self.row_3.addLayout(self.genderEdit)
        self.row_3.addLayout(self.gradeEdit)
        self.contentLayout.addLayout(self.row)
        self.contentLayout.addLayout(self.row_2)
        self.contentLayout.addLayout(self.row_3)
        self.contentLayout.setAlignment(Qt.AlignTop)
        self.resize(420, 270)
        
    def __isValid(self, text):
        name = self.lastnameEdit.lineEdit.text()
        matricule = self.matriculeEdit.lineEdit.text()
        self.yesBtn.setEnabled(len(name) > 2 and len(matricule) == 4)
        