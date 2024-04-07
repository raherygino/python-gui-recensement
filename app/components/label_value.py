from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import StrongBodyLabel, BodyLabel

class LabelValue(QVBoxLayout):
    
    def __init__(self,label:str, value:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.addWidget(StrongBodyLabel(label))
        self.addWidget(BodyLabel(value))
        
        