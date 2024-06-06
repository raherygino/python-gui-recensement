from PyQt5.QtCore import QPoint, Qt
from qfluentwidgets import InfoBar, InfoBarPosition

class Utils:
    
    def __init__(self) -> None:
        self.parmsInfoBar = {
            "orient":       Qt.Horizontal,
            "isClosable":   True,
            "position":     InfoBarPosition.BOTTOM,
            "duration":     2000
        }
    
    def infoBarError(self, title, content, parent):
        self.parmsInfoBar['title'] = title
        self.parmsInfoBar['content'] = content
        self.parmsInfoBar['parent'] = parent
        InfoBar.error(**self.parmsInfoBar)
    
    def infoBarSuccess(self, title, content, parent):
        self.parmsInfoBar['title'] = title
        self.parmsInfoBar['content'] = content
        self.parmsInfoBar['parent'] = parent
        InfoBar.success(**self.parmsInfoBar)