from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from qframelesswindow import FramelessDialog
from qfluentwidgets import Dialog, StrongBodyLabel, BodyLabel, \
                           PrimaryPushButton, PushButton, LineEdit, \
                           ComboBox, SubtitleLabel, FluentStyleSheet
from .button import ButtonClose, PrimaryButton, Button

class ConfirmDialog(Dialog):
    def __init__(self, title:str, content:str, parent=None):
        super().__init__(title, content, parent)
        self.hideDefaultWidget()
        self.nTitleBar = QHBoxLayout()
        self.nTitleBar.setContentsMargins(12,0,0,0)
        self.btnClose = ButtonClose()
        self.btnClose.clicked.connect(self.close)
        self.nTitleBar.addWidget(StrongBodyLabel(title))
        self.nTitleBar.addWidget(self.btnClose,0, Qt.AlignRight)
        self.textLayout.addWidget(BodyLabel(content))
        self.textLayout.setContentsMargins(12,5,12,0)
        self.btnLayout = QHBoxLayout()
        self.btnLayout.setContentsMargins(0,5,0,8)
        self.yesBtn = PrimaryButton("Oui")
        self.yesBtn.clicked.connect(self.accept)
        self.cancelBtn = Button("Non")
        self.cancelBtn.clicked.connect(self.close)
        self.btnLayout.addWidget(self.yesBtn)
        self.btnLayout.addWidget(self.cancelBtn)
        self.textLayout.addLayout(self.btnLayout)
        self.removeLayout()
        self.addLayout()
        self.setFixedHeight(90)
        self.setMinimumWidth(350)
        
    def removeLayout(self):
        while self.vBoxLayout.count():
            item = self.vBoxLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
    def addLayout(self):
        self.vBoxLayout.addLayout(self.nTitleBar)
        self.vBoxLayout.addLayout(self.textLayout)
          
    def hideDefaultWidget(self):
          self.setTitleBarVisible(False)
          self.titleLabel.setVisible(False)
          self.contentLabel.setVisible(False)
          self.yesButton.setVisible(False)
          self.cancelButton.setVisible(False)
          self.buttonGroup.setVisible(False)

class ImportDialog(Dialog):
    def __init__(self, data:list, columns:list, parent=None):
        super().__init__('', '', parent)
        self.setTitleBarVisible(False)
        self.titleLabel.setVisible(False)
        self.contentLabel.setVisible(False)
        columns.insert(0, "-")
        self.textLayout.addWidget(SubtitleLabel('Importer', self))
        self.setFixedWidth(400)
        self.data =  data
        row = QHBoxLayout()
        row.addWidget(BodyLabel("Valeur"))
        row.addWidget(BodyLabel("Colonne"), 0, Qt.AlignRight)
        self.textLayout.addLayout(row)
        self.items = []
        firstData = data[0]
        for i, item in enumerate(firstData):
            row = QHBoxLayout()
            lineEdit = LineEdit(self)
            lineEdit.setText(item)
            lineEdit.setReadOnly(True)
            comboBox =  ComboBox(self)
            comboBox.addItems(columns)
            comboBox.setCurrentIndex(i+1 if i+1 < len(columns) else 0)
            row.addWidget(lineEdit)
            row.addWidget(comboBox)
            self.items.append(comboBox)
            self.textLayout.addLayout(row)
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        self.yesBtn = PrimaryPushButton("Ok")
        self.cancelBtn = PushButton('Annuler')
        self.cancelBtn.clicked.connect(self.reject)
        self.buttonLayout.addWidget(self.yesBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        
    def getData(self):
        data = [item.currentIndex()-1 for item in self.items]
        nData = []
        for nItem in self.data:
            newItem = [None] * len(data)
            for i, n in enumerate(data):
                if n != -1:
                    newItem[n] = nItem[i]
            nData.append(newItem)
        return nData
    
class BigDialog(FramelessDialog):
    def __init__(self, parent=None):
        super().__init__(parent)# add a label to dialog
        self.mainLayout = QVBoxLayout()
        self.contentLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.yesBtn = PrimaryButton("Ok")
        self.cancelBtn = Button('Annuler')
        self.buttonLayout.addWidget(self.yesBtn)
        self.buttonLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.contentLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        self.buttonLayout.setAlignment(Qt.AlignBottom)
        self.setLayout(self.mainLayout)
        # raise title bar
        self.titleBar.raise_()
        FluentStyleSheet.DIALOG.apply(self)
    