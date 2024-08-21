from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem
from PyQt5.QtCore import QUrl, Qt, QThread, pyqtSignal
from PyQt5 import QtCore, QtWidgets, QtPrintSupport
from qfluentwidgets import CommandBar, FluentIcon, Action, isDarkTheme, InfoBar, InfoBarIcon, InfoBarPosition
from ...components import ConfirmDialog
import os

class ViewStudentDialog(QDialog):
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Elève")
        self.resize(800, 850)
        theme = 'ViewStudentDialog {background: '+f'{'#454545' if isDarkTheme() else '#f4f4f4'}'+'}'
        self.setStyleSheet(theme)
        # Create layout
        self.layout = QVBoxLayout()
        # Create QWebEngineView
        self.browser = QWebEngineView()
        self.commandBar = CommandBar(self)

        self.layout.addWidget(self.commandBar, 0)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.commandBar.setMenuDropDown(False)
        # self.commandBar.setButtonTight(True)
        # setFont(self.commandBar, 14)

        self.actionPrint = Action(FluentIcon.PRINT, 'Imprimer', self)
        self.actionPrint.triggered.connect(lambda: self.show_print_dialog())
        self.commandBar.addAction(self.actionPrint)
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # Create a QWebEnginePage and set its content
        self.html_content = ''
        with open('app/resource/public/template.html', 'r', encoding='utf-8') as file:
            self.html_content = file.read()
        
        with open('app/resource/public/img/eniap.base64', 'r', encoding='utf-8') as file:
            self.html_content = self.html_content.replace('img/eniap.png', file.read())
            
        with open('app/resource/public/img/pn.base64', 'r', encoding='utf-8') as file:
            self.html_content = self.html_content.replace('img/logo_pn.png', file.read())

        # Show the preview
        #self.browser.show()
        # Download file
        self.browser.page().profile().downloadRequested.connect(self.download_file)
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)
    
    def download_file(self, download_item: QWebEngineDownloadItem):
        # Set a download path
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", download_item.suggestedFileName())
        if save_path:
            ext = '.doc'
            save_path += ext if save_path.find(ext) == -1 else ''
            download_item.stateChanged.connect(self.on_download_state_changed)
            download_item.setPath(save_path)
            download_item.accept()
            
    def on_download_state_changed(self, state):
        if state == QWebEngineDownloadItem.DownloadRequested:
            content = "Exportation en cours"
            w = InfoBar(
                icon=InfoBarIcon.INFORMATION,
                title='Progression',
                content=content,
                orient=Qt.Vertical,    # vertical layout
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            w.show()
        elif state == QWebEngineDownloadItem.DownloadCompleted:
            dialog = ConfirmDialog('Réussi', 'Exportation avec succès', self)
            dialog.cancelBtn.setVisible(False)
            dialog.yesBtn.setText('Ok')
            dialog.exec()
        
    def show_print_dialog(self):
        # Configure the printer
        self._printer = QtPrintSupport.QPrinter()
        self._printer.setPaperSize(QtCore.QSizeF(80, 297), QtPrintSupport.QPrinter.Millimeter)
        self._printer.setResolution(600)

        # Create and show the print dialog
        print_dialog = QtPrintSupport.QPrintDialog(self._printer, self)
        if print_dialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:
            self.browser.page().print(self._printer, self.print_completed)

    def print_completed(self, result):
        if result:
            QtWidgets.QMessageBox.information(self, 'Print', 'Print job completed successfully.')
        else:
            QtWidgets.QMessageBox.warning(self, 'Print', 'Print job failed.')
            
    def rowMark(self, label, value, valueCoef):
        return f'''
                <tr>
                    <td style="border: solid 1px #000000; border-collapse: collapse;">{label}</td>
                    <td style="border: solid 1px #000000; border-collapse: collapse;" align="right">{value}</td>
                    <td style="border: solid 1px #000000; border-collapse: collapse;" align="right">{valueCoef}</td>
                </tr>'''