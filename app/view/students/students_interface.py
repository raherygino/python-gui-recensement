from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

from qfluentwidgets import SegmentedWidget, TransparentDropDownPushButton, Action,\
    CommandBar, RoundMenu, FluentIcon, setFont, StrongBodyLabel , SearchLineEdit,\
    BodyLabel
from .tab import DatabaseStudentTab, AbsenceStudentTab, DayStudentTab
from ...common import Function

class StudentsInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.func = Function()
        self.resize(400, 400)
        self.mainWindow = self.parent
        self.nParent = parent
        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout()

        self.dbInterface = DatabaseStudentTab(self)
        self.absInterface = AbsenceStudentTab(self)
        self.dayInterface = DayStudentTab(self)

        # add items to pivot
        self.addSubInterface(self.dbInterface, 'dbInterface', 'Base des données')
        self.addSubInterface(self.absInterface, 'absInterface', 'Grille d\'absence')
        self.addSubInterface(self.dayInterface, 'dayInterface', 'Total Nb Jours')

        self.__initCommandBar()
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.addWidget(self.pivot)
        
        self.countLayout = QHBoxLayout()
        self.countLayout.setContentsMargins(0,0,0,0)
        self.countLayout.setAlignment(Qt.AlignRight)
        self.titleCount = StrongBodyLabel("Nombre")
        self.valueCount = BodyLabel("1220")
        self.countLayout.addWidget(self.titleCount)
        self.countLayout.addWidget(self.valueCount)        
        self.vBoxLayout.addLayout(self.countLayout)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.dbInterface)
        self.pivot.setCurrentItem(self.dbInterface.objectName())
        self.setObjectName("studentsTab")
        

    def createDropDownButton(self, title, icon, children:list, parent):
        button = TransparentDropDownPushButton(title, self, icon)
        button.setFixedHeight(34)
        setFont(button, 12)
        menu = RoundMenu(parent=parent)
        menu.addActions(children)
        button.setMenu(menu)
        return button
        
    def __initCommandBar(self):
        self.commandBar = CommandBar(self)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.setButtonTight(True)
        setFont(self.commandBar, 14)
        
        self.addAction = Action(FluentIcon.PEOPLE, "Elève", self)
        self.addSubject = Action(FluentIcon.DICTIONARY, "Matière", self)
        #self.addComp = Action(FluentIcon.DICTIONARY, "Comportement", self)
        self.dropDownButtonAdd = self.createDropDownButton('Ajouter', 
                                                        FluentIcon.ADD,[self.addAction, self.addSubject], self)
        
        self.refreshAction = Action(FluentIcon.SYNC, "Actualiser", self)
        self.importAction = Action(FluentIcon.FOLDER_ADD, "Importer", self)
        self.exportActionCsv = Action(FluentIcon.QUICK_NOTE, "CSV", self)
        self.exportAction = Action(FluentIcon.DOCUMENT, "Excel", self)
        self.dropDownButtonExp = self.createDropDownButton('Exporter', 
                                                        FluentIcon.SHARE,[self.exportAction, self.exportActionCsv], self)
        self.deleteAction = Action(FluentIcon.DELETE, "Supprimer tous", self)   
        
        self.commandBar.addWidget(self.dropDownButtonAdd)

        self.commandBar.addAction(self.refreshAction)
        self.commandBar.addAction(self.importAction)
        self.commandBar.addWidget(self.dropDownButtonExp)
        self.commandBar.addSeparator()
        self.commandBar.addAction(self.deleteAction)
        
        self.titleLabel = StrongBodyLabel("Base des données")
        
        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText("Recherche")
        self.searchLineEdit.setFixedWidth(200)
        
        self.hBoxLayout.addWidget(self.commandBar)
        self.hBoxLayout.addWidget(self.titleLabel)
        self.hBoxLayout.addWidget(self.searchLineEdit)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        
    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.titleLabel.setText(self.pivot.currentItem().text())
        self.pivot.setCurrentItem(widget.objectName())
        self.valueCount.setText(str(len(self.func.getTableData(widget.tableView))))