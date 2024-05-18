from PyQt5.QtWidgets import QFrame, QAbstractItemView, QVBoxLayout, QWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from qfluentwidgets import (CommandBar, FluentIcon, Action, TransparentDropDownPushButton,
                            setFont, RoundMenu, TableWidget, isDarkTheme, setTheme, Theme, TableView, TableItemDelegate, setCustomStyleSheet)

class BelieverInterface(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo1{background: rgb(32, 32, 32)}')

        self.vBoxLayout = QVBoxLayout(self)
        self.commandBar = CommandBar(self)
        

        self.vBoxLayout.addWidget(self.commandBar, 0)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.commandBar.setMenuDropDown(False)
        # self.commandBar.setButtonTight(True)
        # setFont(self.commandBar, 14)

        # add custom widget
        #self.commandBar.addWidget(self.dropDownButton)

        self.tableView = TableWidget(self)

        # NOTE: use custom item delegate
        # self.tableView.setItemDelegate(CustomTableItemDelegate(self.tableView))

        # select row on right-click
        # self.tableView.setSelectRightClickedRow(True)

        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.resizeColumnsToContents()
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setWordWrap(False)
        #self.tableView.setRowCount(6)
        self.tableView.setColumnCount(11)

        self.tableView.verticalHeader().hide()
        header = ['ID', 'Anarana', 'Fanampiny',
                                                  'Daty sy toerana nahaterahana', 'Asa', 
                                                  'Daty batisa', 'Daty sy toerana maha mpandray',
                                                  'Laharana karatra mpandray', 'Sampana sy/na Sampan\'asa',
                                                  'Andraikitra', 'Laharana finday']
        self.tableView.setHorizontalHeaderLabels(header)
        
        self.header = self.tableView.horizontalHeader()
        #self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableView.resizeColumnsToContents()
        #self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.setSortingEnabled(True)

        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        #self.hBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.vBoxLayout.addWidget(self.tableView)

        self.setObjectName("believerInterface")
        
    def populateTable(self, items):
        self.tableView.setRowCount(0)
        for row, item in enumerate(items):
            self.tableView.insertRow(row)
            obj = [item.id, item.lastname, item.firstname,f'{item.birthday} ,{item.birthplace}', '', 
                   item.date_of_baptism,f'{item.date_of_recipient} {item.place_of_recipient}', 
                   item.number_recipient,item.dept_work, item.responsibility, item.phone]
            for col, value in enumerate(obj):
                self.tableView.setItem(row, col, QTableWidgetItem(str(value)))


    def addButton(self, icon, text):
        action = Action(icon, text, self)
        self.commandBar.addAction(action)

    def onEdit(self, isChecked):
        print('Enter edit mode' if isChecked else 'Exit edit mode')

    def createDropDownButton(self):
        button = TransparentDropDownPushButton('Menu', self, FluentIcon.MENU)
        button.setFixedHeight(34)
        setFont(button, 12)

        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(FluentIcon.COPY, 'Copy'),
            Action(FluentIcon.CUT, 'Cut'),
            Action(FluentIcon.PASTE, 'Paste'),
            Action(FluentIcon.CANCEL, 'Cancel'),
            Action('Select all'),
        ])
        button.setMenu(menu)
        return button