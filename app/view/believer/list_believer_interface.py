from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QAbstractItemView
from PyQt5.QtCore import Qt
from qfluentwidgets import ProgressBar, StrongBodyLabel, BodyLabel, TransparentDropDownPushButton,\
    setFont, RoundMenu, CommandBar, Action, FluentIcon, SearchLineEdit
from ...components import TableView

class ListBelieverInterface(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        #self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout = QHBoxLayout()
        self.nParent = parent
        self.__initCommandBar()
        
        self.__initTableView(parent)
        self.countLayout = QHBoxLayout()
        self.countLayout.setContentsMargins(0,0,0,0)
        self.countLayout.setAlignment(Qt.AlignRight)
        self.titleCount = StrongBodyLabel("")
        self.valueCount = BodyLabel("")
        self.countLayout.addWidget(self.titleCount)
        self.countLayout.addWidget(self.valueCount)        
        self.vBoxLayout.addLayout(self.countLayout)
        self.parent = parent
        self.setObjectName("listBeliverInterface")
        
    def __initTableView(self, parent):
        self.progressBar = ProgressBar(self)
        self.progressBar.setVisible(False)
        self.tableView = TableView(self)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.vBoxLayout.addWidget(self.progressBar)
        self.vBoxLayout.addWidget(self.tableView)
    
    
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
        
        self.addAction = Action(FluentIcon.ADD, "Mampiditra", self)
        self.exportAction = Action(FluentIcon.DOCUMENT, "Avoaka Excel", self)
        self.diaconAction = Action(FluentIcon.PEOPLE, "Diakona", self)
        self.deptWorkAction = Action(FluentIcon.FEEDBACK, "Sampana", self)
        '''
        self.addAction = Action(FluentIcon.APPLICATION, "Un matériel", self)
        self.addComp = Action(FluentIcon.LINK, "Options", self)
        self.dropDownButtonAdd = self.createDropDownButton('Ajouter', 
                                                        FluentIcon.ADD,[self.addAction, self.addComp], self)
        
        self.refreshAction = Action(FluentIcon.SCROLL, "Mouvement", self)
        self.importAction = Action(FluentIcon.FOLDER_ADD, "Importer", self)
        self.exportActionCsv = Action(FluentIcon.QUICK_NOTE, "CSV", self)
        self.exportAction = Action(FluentIcon.DOCUMENT, "Excel", self)
        self.dropDownButtonExp = self.createDropDownButton('Exporter', 
                                                        FluentIcon.SHARE,[self.exportAction, self.exportActionCsv], self)
        self.deleteAction = Action(FluentIcon.DELETE, "Supprimer tous", self)   
        
        self.commandBar.addWidget(self.dropDownButtonAdd)
        '''
        self.commandBar.addAction(self.addAction)
        self.commandBar.addAction(self.exportAction)
        self.commandBar.addAction(self.diaconAction)
        self.commandBar.addAction(self.deptWorkAction)
        '''self.commandBar.addAction(self.refreshAction)
        self.commandBar.addAction(self.importAction)
        self.commandBar.addWidget(self.dropDownButtonExp)
        self.commandBar.addSeparator()
        self.commandBar.addAction(self.deleteAction)'''
        
        self.titleLabel = StrongBodyLabel("Listra")
        
        '''self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText("Recherche")
        self.searchLineEdit.setFixedWidth(200)'''
        
        self.hBoxLayout.addWidget(self.commandBar)
        self.hBoxLayout.addWidget(self.titleLabel)
        #self.hBoxLayout.addWidget(self.searchLineEdit)
        self.vBoxLayout.addLayout(self.hBoxLayout)