from PyQt5.QtWidgets import QHBoxLayout, QTableWidgetItem, QFrame
from PyQt5.QtCore import QPoint, Qt, QSize
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent

from ...common.icon import Icon
from qfluentwidgets import ImageLabel, BodyLabel, SubtitleLabel, Action, CommandBar, FluentIcon, TransparentDropDownPushButton, setFont, RoundMenu
from ...components import BigDialog, TableView

class StudentDialog(BigDialog):
    
    def __init__(self, parent=None):
        super().__init__('', parent)
        
        self.hBoxLayout = QHBoxLayout()
        self.commandBar = CommandBar(self)
        self.hBoxLayout.addWidget(self.commandBar, 0)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.addWidget(self.exportButton())
        
        self.contentLayout.addLayout(self.hBoxLayout)
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
        self.yesBtn.setVisible(False)
        #self.cancelBtn.setVisible(False)
        
        self.contentLayout.setAlignment(Qt.AlignTop)
    

    def exportButton(self):
        self.exportWord = Action(FluentIcon.DOCUMENT, 'Word')
        self.exportExcel = Action(Icon.GRID, 'Excel')
        button = TransparentDropDownPushButton('Exporter', self, FluentIcon.SHARE)
        button.setFixedHeight(34)
        setFont(button, 12)

        menu = RoundMenu(parent=self)
        menu.addActions([
            self.exportWord,
            self.exportExcel
        ])
        button.setMenu(menu)
        return button