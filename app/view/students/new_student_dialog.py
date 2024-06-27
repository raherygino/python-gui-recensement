from PyQt5.QtWidgets import QHBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, PrimaryPushButton, PushButton

from ...components import LineEditWithLabel, ComboxEditWithLabel

class NewStudentDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Ajouter un élève', self)

        self.row = QHBoxLayout()
        self.matriculeEdit = LineEditWithLabel("Matricule")
        self.matriculeEdit.lineEdit.textChanged.connect(lambda: self.__isValid(None))
        self.lastnameEdit = LineEditWithLabel("Nom")
        self.lastnameEdit.lineEdit.textChanged.connect(lambda: self.__isValid(None))
        self.firstnameEdit = LineEditWithLabel("Prénoms")
        self.row.addLayout(self.matriculeEdit)
        self.row.addLayout(self.lastnameEdit)
        self.row.addLayout(self.firstnameEdit)
        
        self.row_2 = QHBoxLayout()
        self.genderEdit = ComboxEditWithLabel("Genre", ['M','F'])
        self.gradeEdit = ComboxEditWithLabel("Grade", ["EIP", "EAP"])
        self.row_2.addLayout(self.genderEdit)
        self.row_2.addLayout(self.gradeEdit)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row_2)

        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        
        self.yesBtn = PrimaryPushButton("Ok")
        self.cancelBtn = PushButton('Annuler')
        self.cancelBtn.clicked.connect(self.__cancel)
        
        self.buttonLayout.addWidget(self.yesBtn)
        self.buttonLayout.addWidget(self.cancelBtn)

        self.widget.setMinimumWidth(650)
    
    def __isValid(self, text):
        name = self.lastnameEdit.lineEdit.text()
        matricule = self.matriculeEdit.lineEdit.text()
        self.yesBtn.setEnabled(len(name) > 2 and len(matricule) == 4)
        
    def __cancel(self):
        self.reject()
