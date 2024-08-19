from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem, QFrame
from PyQt5.QtCore import QPoint, Qt, QSize
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent

from qfluentwidgets import ImageLabel, BodyLabel, SubtitleLabel
from ...components import BigDialog, TableView

class StudentDialog(BigDialog):
    
    def __init__(self, parent=None):
        super().__init__('', parent)
        self.ImageLabel = ImageLabel(self)
        self.ImageLabel.setImage("app/resource/images/user.png")
        self.ImageLabel.setFixedSize(QSize(100,100))
        self.ImageLabel.setObjectName(u"ImageLabel")
        self.contentLayout.addWidget(self.ImageLabel, 0, Qt.AlignCenter)
        self.ImageLabel.setAlignment(Qt.AlignCenter)
        self.label = BodyLabel("EAP 2723\nRAHERINOMENJANAHARY Georginot Armelin", self)
        self.contentLayout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.title = SubtitleLabel("Notes", self)
        self.title.setAlignment(Qt.AlignCenter)
        
        self.contentLayout.addWidget(self.line)
        self.contentLayout.addWidget(self.title)
        
        self.table = TableView(self)
        self.table.setHorizontalHeaderLabels(["Matières","Coef", "Note", "Note\navec Coef"])
        self.table.setMinimumHeight(400)
        self.contentLayout.addWidget(self.table)
        
        self.contentLayout.setAlignment(Qt.AlignTop)
        