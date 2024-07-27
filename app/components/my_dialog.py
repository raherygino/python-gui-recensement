from qfluentwidgets import Dialog, StrongBodyLabel, BodyLabel, PrimaryPushButton, PushButton
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QPushButton

class MyDialog(Dialog):
    def __init__(self, parent=None):
        super().__init__("title", "content", parent)
        self.hideDefaultWidget()
        
        self.textLayout.addWidget(StrongBodyLabel('Hello'))
        self.textLayout.addWidget(BodyLabel('World'))
        
        self.btnLayout = QHBoxLayout()
        self.yesBtn = PrimaryPushButton("Ok")
        self.cancelBtn = PushButton("Annuler")
        
        self.btnLayout.addWidget(self.yesBtn)
        self.btnLayout.addWidget(self.cancelBtn)
        self.textLayout.addLayout(self.btnLayout)
        self.setFixedHeight(90)
          
    def hideDefaultWidget(self):
          self.setTitleBarVisible(False)
          self.titleLabel.setVisible(False)
          self.contentLabel.setVisible(False)
          self.yesButton.setVisible(False)
          self.cancelButton.setVisible(False)
          self.buttonGroup.setVisible(False)
        
          
    