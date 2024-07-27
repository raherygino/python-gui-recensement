from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from ..common.config import cfg
import darkdetect

class Theme:
    
    def __init__(self):
        newTheme = cfg.get(cfg.theme)
        theme = newTheme.lower()
        self.color = f'rgba{str(cfg.get(cfg.themeColor).getRgb())}'.replace('255)', '1)')
        if theme == "auto":
            theme = "light" if darkdetect.isLight() else "dark"
        if theme == "light":
            self.color = self.color.replace('1)','0.8)')
        self.option = theme
        
    def getQss(self, name:str):
        qss = ''
        with open(f'app/resource/qss/{self.option}/{name}.qss', encoding='utf-8') as f:
            qss = f.read().replace('nColor', self.color)
        return qss
        

class ButtonIcon(QPushButton):
    
    def __init__(self, icon:str):
        theme = Theme()
        if theme.option == 'dark':
            icon = icon.replace('black', 'white')
        super().__init__(QIcon(icon), '')
        self.setFixedSize(40,32)
        self.setStyle()
        
    def setStyle(self):
        self.setStyleSheet('''
            QPushButton {
                border: none;
                background: transparent
            }
            QPushButton:hover {
                background: #ff5555;
            }
        ''')
        
class PrimaryButton(QPushButton):
    
    def __init__(self, text):
        super().__init__(text=text)
        self.setFixedHeight(30)
        self.setQss()
        
    def setQss(self):
        theme = Theme()
        hover = theme.color.replace('1)', '0.8)')
        if theme.option == 'light':
            hover = theme.color.replace('0.8)', '1)')
        self.setStyleSheet(theme.getQss('button').replace('hColor', hover))
        
class Button(QPushButton):
    
    def __init__(self, text):
        super().__init__(text=text)
        self.setFixedHeight(30)
        self.setQss()
        
    def setQss(self):
        theme = Theme()
        self.setStyleSheet(theme.getQss('button'))