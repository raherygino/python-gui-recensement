from qfluentwidgets import Dialog, StrongBodyLabel, BodyLabel, PrimaryPushButton, PushButton, FluentIcon
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .btn import ButtonClose, PrimaryButton, Button

class DialogConfirm(Dialog):
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
        
          
    