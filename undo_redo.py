import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Undo/Redo Example')
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Undo action
        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.text_edit.undo)

        # Redo action
        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.text_edit.redo)

        # Menu bar
        menubar = self.menuBar()
        edit_menu = menubar.addMenu('Edit')
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
