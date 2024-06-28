import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class Worker(QThread):
    progress = pyqtSignal(int)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)

    def update_progress(self, value):
        self.progress.emit(value)

def long_running_task(progress_callback):
    for i in range(100):
        time.sleep(0.1)  # Simulate a time-consuming task
        progress_callback(i + 1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Progress Bar with PyQt and Function Passing")
        self.setGeometry(300, 300, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.layout.addWidget(self.progress_bar)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_task)
        self.layout.addWidget(self.start_button)

    def start_task(self):
        self.worker = Worker(long_running_task, self.update_progress)
        self.worker.progress.connect(self.update_progress)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
