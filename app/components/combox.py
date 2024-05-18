from qfluentwidgets import ComboBox, BodyLabel
from PyQt5.QtWidgets import QVBoxLayout

class ComboBoxWithLabel(ComboBox):
    
    def __init__(self,label:str, parent=None):
        super().__init__(parent)
        
        self.label = BodyLabel(label)
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self)
        