from PyQt5.QtWidgets import QHBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ComboBox, PrimaryToolButton, FluentIcon
from ....common.functions import Function
from ....components.table_view import TableView

class NewComportementDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.func = Function()
        self.titleLabel = SubtitleLabel('Comportement', self)
        
        self.row = QHBoxLayout()
        self.nameLineEdit = LineEdit(self)
        self.nameLineEdit.setPlaceholderText('Titre')
        self.nameLineEdit.setClearButtonEnabled(True)
        self.nameLineEdit.textChanged.connect(self.__onChangeName)
        
        self.abrLineEdit = LineEdit(self)
        self.abrLineEdit.setPlaceholderText('Abréviation')
        self.abrLineEdit.setFixedWidth(100)
        self.abrLineEdit.setClearButtonEnabled(True)
        self.abrLineEdit.setVisible(False)
        
        self.row_2 = QHBoxLayout()
        self.typeCombox = ComboBox(self)
        self.btnAdd = PrimaryToolButton(FluentIcon.ACCEPT, self)
        
        self.table = TableView(self)
        self.table.setHorizontalHeaderLabels(["Observations", "Types d'observation"])
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.row.addWidget(self.nameLineEdit)
        self.row.addWidget(self.abrLineEdit)
        self.row_2.addWidget(self.typeCombox)
        self.row_2.addWidget(self.btnAdd)
        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row_2)
        self.viewLayout.addWidget(self.table)

        # change the text of button
        self.yesButton.setText('Ajouter')
        self.cancelButton.setText('Annuler')
        self.btnAdd.setEnabled(False)
        self.widget.setMinimumWidth(450)

        # self.hideYesButton()
    def __onChangeName(self, text):
        if text != "":
            self.btnAdd.setEnabled(True)
            abrs = text.split(" ")
            abre = ""
            for abr in abrs:
                if len(abr) != 0:
                    abre += abr[0].upper()
                if len(abrs) == 1:
                    abre = abrs[0][0:4].upper()
            self.abrLineEdit.setText(abre)
        else:
            self.btnAdd.setEnabled(False)
            