from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from ...components import ComboxEditWithLabel, DateEditWithLabel, LineEditWithLabel
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, BodyLabel

class editWithLabel(QVBoxLayout):
    def __init__(self, label:str,parent=None, **kwargs):
        super().__init__(None)
        self.parent = parent
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(5)
        self.label = BodyLabel(parent)
        self.label.setText(label)
        self.addWidget(self.label)
        self.args = kwargs
        self.lineEdits = []
        self.LineEdit()

    def LineEdit(self):
        self.hBoxLayout = QHBoxLayout()
        self.lineEdits.clear()
        placeholders = self.args.get("placeholders")
        for placeholder in placeholders:
            lineEdit = LineEdit(self.parent)
            lineEdit.setClearButtonEnabled(True)
            lineEdit.setPlaceholderText(placeholder)
            self.hBoxLayout.addWidget(lineEdit)
            self.lineEdits.append(lineEdit)
        self.addLayout(self.hBoxLayout)
        
    def text(self, pos:int):
        return self.lineEdits[pos].text()
        


class AddBelieverDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Mampiditra', self)

        self.row = QHBoxLayout()
        self.lastnameEdit = editWithLabel("Anarana", self, placeholders=["Anarana"])
        self.firstnameEdit = editWithLabel("Fanampiny", self, placeholders=["Fanampiny"])
        self.posFamilyCombox = ComboxEditWithLabel("Amin'ny finakaviana", ["Zanaka", "Vady"])
        self.posFamilyCombox.combox.currentTextChanged.connect(self.posFamilyChanged)
        self.genderCombox = ComboxEditWithLabel("Lahy / Vavy", ["Lahy", "Vavy"])
        self.row.addLayout(self.lastnameEdit)
        self.row.addLayout(self.firstnameEdit)
        self.row.addLayout(self.posFamilyCombox)
        self.row.addLayout(self.genderCombox)
        self.row_2 = QHBoxLayout()
        self.addressEdit = editWithLabel("Adiresy", self, placeholders=["Adiresy"])
        self.regionEdit = editWithLabel("Faritra", self, placeholders=["Faritra"])
        self.row_2.addLayout(self.addressEdit)
        self.row_2.addLayout(self.regionEdit)
        
        self.row_3 = QHBoxLayout()
        self.diaconEdit = editWithLabel("Diakonina miandraikitra", self, placeholders=["Diakonina miandraikitra"])
        #self.birthdayEdit = editWithLabel("Daty sy toerana nahaterahana", self, placeholders=["Daty", "Toerana"])
        self.birthdayEdit = DateEditWithLabel("Daty nahaterahana")
        self.birthplaceEdit = LineEditWithLabel("Toerana nahaterahana")
        self.row_3.addLayout(self.diaconEdit)
        self.row_3.addLayout(self.birthdayEdit)
        self.row_3.addLayout(self.birthplaceEdit)
        
        '''self.row_4 = QHBoxLayout()
        self.nameFatherEdit = editWithLabel("Anaran'i Ray", self, placeholders=["Anaran'i Ray"])
        self.nameMotherEdit = editWithLabel("Anaran'i Reny", self, placeholders=["Anaran'i Reny"])
        self.row_4.addLayout(self.nameFatherEdit)
        self.row_4.addLayout(self.nameMotherEdit)'''
        
        self.row_5 = QHBoxLayout()
        self.baptismEdit = editWithLabel("Daty sy toerana batisa", self, placeholders=["Daty", "Toerana"])
        self.row_5.addLayout(self.baptismEdit)

        self.row_6 = QHBoxLayout()
        self.recipientEdit = editWithLabel("Daty, toerana, laharana mpandray", self, placeholders=["Daty", "Toerana", "Laharana"])
        self.row_6.addLayout(self.recipientEdit)

        self.row_7 = QHBoxLayout()
        self.phoneEdit = editWithLabel("Laharan'ny finday", self, placeholders=["Laharan'ny finday"])
        self.deptWorkEdit = editWithLabel("Sampana na/sy sampan'asa", self, placeholders=["Sampana na/sy sampan'asa"])
        self.responsibilityEdit = editWithLabel("Andraikitra", self, placeholders=["Andraikitra"])
        self.row_7.addLayout(self.phoneEdit)
        self.row_7.addLayout(self.deptWorkEdit)
        self.row_7.addLayout(self.responsibilityEdit)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row_2)
        self.viewLayout.addLayout(self.row_3)
        #self.viewLayout.addLayout(self.row_4)
        self.viewLayout.addLayout(self.row_5)
        self.viewLayout.addLayout(self.row_6)
        self.viewLayout.addLayout(self.row_7)

        # change the text of button
        self.yesButton.setText('Ampidirina')
        self.cancelButton.setText('Asorina')

        self.widget.setMinimumWidth(650)

    def posFamilyChanged(self, text):
        if text == "Vady":
            self.genderCombox.combox.setCurrentIndex(1)