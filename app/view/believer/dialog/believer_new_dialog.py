from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme, BodyLabel

class editWithLabel(QVBoxLayout):
    def __init__(self, label:str,size,parent=None, **kwargs):
        super().__init__(None)
        self.parent = parent
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(5)
        self.label = BodyLabel(parent)
        self.label.setText(label)
        self.addWidget(self.label)
        self.LineEdit(size)


    def LineEdit(self, size):
        self.hBoxLayout = QHBoxLayout()
        for i in range(size):
            lineEdit = LineEdit(self.parent)
            lineEdit.setClearButtonEnabled(True)
            self.hBoxLayout.addWidget(lineEdit)
        self.addLayout(self.hBoxLayout)




class BelieverNewDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Mampiditra', self)

        self.row = QHBoxLayout()
        self.lastnameEdit = editWithLabel("Anarana",1, self)
        self.firstnameEdit = editWithLabel("Fanampiny",1, self)
        self.row.addLayout(self.lastnameEdit)
        self.row.addLayout(self.firstnameEdit)
        
        self.row_2 = QHBoxLayout()
        self.addressEdit = editWithLabel("Adiresy",1, self)
        self.regionEdit = editWithLabel("Faritra",1, self)
        self.row_2.addLayout(self.addressEdit)
        self.row_2.addLayout(self.regionEdit)
        
        self.row_3 = QHBoxLayout()
        self.diaconEdit = editWithLabel("Diakonina miandraikitra",1, self)
        self.birthdayEdit = editWithLabel("Daty sy toerana nahaterahana",2, self)
        self.row_3.addLayout(self.diaconEdit)
        self.row_3.addLayout(self.birthdayEdit)
        
        self.row_4 = QHBoxLayout()
        self.nameFatherEdit = editWithLabel("Anaran'i Ray",1, self)
        self.nameMotherEdit = editWithLabel("Anaran'i Reny",1, self)
        self.row_4.addLayout(self.nameFatherEdit)
        self.row_4.addLayout(self.nameMotherEdit)

        self.row_5 = QHBoxLayout()
        self.recipientEdit = editWithLabel("Daty, toerana, laharana mpandray",3, self)
        self.row_5.addLayout(self.recipientEdit)

        self.row_6 = QHBoxLayout()
        self.phoneEdit = editWithLabel("Laharan'ny finday",1, self)
        self.deptWorkEdit = editWithLabel("Sampana na/sy sampan'asa",1, self)
        self.responsibilityEdit = editWithLabel("Andraikitra",1, self)
        self.row_6.addLayout(self.phoneEdit)
        self.row_6.addLayout(self.deptWorkEdit)
        self.row_6.addLayout(self.responsibilityEdit)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row_2)
        self.viewLayout.addLayout(self.row_3)
        self.viewLayout.addLayout(self.row_4)
        self.viewLayout.addLayout(self.row_5)
        self.viewLayout.addLayout(self.row_6)

        # change the text of button
        self.yesButton.setText('打开')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(650)
        self.yesButton.setDisabled(True)

        # self.hideYesButton()
