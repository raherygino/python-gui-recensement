from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ToolButton, FluentIcon, InfoBarIcon, Flyout
from ....common import Function
from ....components import SpinBoxEditWithLabel, LineEditWithLabel

class NewPromotionDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.func = Function()
        self.titleLabel = SubtitleLabel('Promotion', self)
        
        self.rankLineEdit = SpinBoxEditWithLabel("Rang")
        self.rankLineEdit.spinbox.textChanged.connect(self.__onChangeName)
        
        self.nameLineEdit = LineEditWithLabel("Nom de la promotion")
        self.nameLineEdit.lineEdit.setClearButtonEnabled(True)
        
        self.row = QHBoxLayout()
        self.logoLineEdit = LineEditWithLabel("Logo")
        self.logoLineEdit.lineEdit.setReadOnly(True)
        self.logoLineEdit.lineEdit.setClearButtonEnabled(True)
        self.logoBtn = ToolButton(FluentIcon.IMAGE_EXPORT)
        self.logoBtn.clicked.connect(lambda e : self.fetchLogo(e))
        
        self.row.addLayout(self.logoLineEdit)
        self.row.addWidget(self.logoBtn,0, Qt.AlignBottom)
        
        self.yearLineEdit = LineEditWithLabel("Année")
        self.yearLineEdit.lineEdit.setInputMask("9999-9999")
        
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(self.rankLineEdit)
        self.viewLayout.addLayout(self.nameLineEdit)
        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.yearLineEdit)

        # change the text of button
        self.yesButton.setText('Ajouter')
        self.cancelButton.setText('Annuler')
        self.yesButton.setEnabled(False)
        self.widget.setMinimumWidth(450)

        

    def __onChangeName(self, text):
        if text != "" and int(text) != 0:
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)
            
    def fetchLogo(self, event):
        fileName = self.func.importFile(self, "Import image", "PNG File (*.png);;JPG File (*.jpg);;GIF File (*.gif)")
        if fileName:
            self.logoLineEdit.lineEdit.setText(fileName)
        else:
            self.logoLineEdit.lineEdit.setText("")
