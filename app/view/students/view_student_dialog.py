from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

class ViewStudentDialog(QDialog):
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Web View Dialog")
        self.setGeometry(100, 100, 800, 600)  # Set the initial size of the dialog
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create QWebEngineView
        self.web_view = QWebEngineView()
        
        layout.addWidget(self.web_view)
        self.setLayout(layout)