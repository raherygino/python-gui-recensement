from PyQt5.QtWidgets import QHBoxLayout, QWidget, QGridLayout, QAbstractItemView, QVBoxLayout
from qfluentwidgets import SubtitleLabel
from ....components import BigDialog, ComboBox
from ....models import Believer
from ....common import Function

class WithFamilyDialog(BigDialog):
    
    def __init__(self, parent=None):
        super().__init__("Asina finakaviana", parent)
        self.combox = ComboBox(self)
        self.combox.addItems(['Tsia', 'Eny'])
        self.contentLayout.addWidget(self.combox)
        self.setFixedHeight(120)
        self.yesBtn.setText("Avoaka")
        self.cancelBtn.setText("Miverina")