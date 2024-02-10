from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QTableWidgetItem
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
        self.dropDownButton = self.createDropDownButton()

        self.vBoxLayout.addWidget(self.commandBar, 0)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.commandBar.setMenuDropDown(False)
        # self.commandBar.setButtonTight(True)
        # setFont(self.commandBar, 14)

        self.addButton(FluentIcon.ADD, 'Add')
        self.commandBar.addSeparator()

        self.commandBar.addAction(Action(FluentIcon.EDIT, 'Edit', triggered=self.onEdit, checkable=True))
        self.addButton(FluentIcon.COPY, 'Copy')
        self.addButton(FluentIcon.SHARE, 'Share')

        # add custom widget
        self.commandBar.addWidget(self.dropDownButton)

        # add hidden actions
        self.commandBar.addHiddenAction(Action(FluentIcon.SCROLL, 'Sort', triggered=lambda: print('排序')))
        self.commandBar.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))

        self.tableView = TableWidget(self)

        # NOTE: use custom item delegate
        # self.tableView.setItemDelegate(CustomTableItemDelegate(self.tableView))

        # select row on right-click
        # self.tableView.setSelectRightClickedRow(True)

        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)

        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(6)
        self.tableView.setColumnCount(5)
        songInfos = [
            ['かばん', 'aiko', 'かばん', '2004', '5:04'],
            ['爱你', '王心凌', '爱你', '2004', '3:39'],
            ['星のない世界', 'aiko', '星のない世界/横顔', '2007', '5:30'],
            ['横顔', 'aiko', '星のない世界/横顔', '2007', '5:06'],
            ['秘密', 'aiko', '秘密', '2008', '6:27'],
            ['シアワセ', 'aiko', '秘密', '2008', '5:25'],
        ]
        songInfos += songInfos
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.tableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(['Title', 'Artist', 'Album', 'Year', 'Duration'])
        self.tableView.resizeColumnsToContents()
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.setSortingEnabled(True)

        self.setStyleSheet("Demo{background: rgb(255, 255, 255)} ")
        #self.hBoxLayout.setContentsMargins(50, 30, 50, 30)
        self.vBoxLayout.addWidget(self.tableView)


        self.setObjectName("believerInterface")

    def addButton(self, icon, text):
        action = Action(icon, text, self)
        action.triggered.connect(lambda: print(text))
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