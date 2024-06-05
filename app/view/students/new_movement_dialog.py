from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QCompleter
from PyQt5.QtCore import QDate, Qt
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel
from ...components import EditWithLabel
from datetime import datetime, timedelta

class NewMouvementDialog(MessageBoxBase):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isDay = False
        self.vBoxLayout = QVBoxLayout()
        self.title = SubtitleLabel("Mouvement", self)
        self.subTitle = BodyLabel("Elève Agent de Police")
        
        self.row = QHBoxLayout()
        self.typeEdit = EditWithLabel("Type d'observation", self, combox=[])
        self.subTypeEdit = EditWithLabel("Observation", self, combox=[])
        self.motifEdit = EditWithLabel("Motif", self, placeholders=["Motif"])
        
        
        self.row.addLayout(self.typeEdit)
        self.row.addLayout(self.subTypeEdit)
        
        current_date = datetime.now().date()
        self.row_2 = QHBoxLayout()
        self.dateEdit = EditWithLabel("Date début", self, date="Date début")
        self.dateEdit.date.setDate(QDate(current_date.year, current_date.month, current_date.day))
        self.dateEdit.date.dateChanged.connect(self.daysBetweenDates)
        
        self.dateEdit2 = EditWithLabel("Date fin", self, date="Date fin")
        self.dateEdit2.date.setDate(QDate(current_date.year, current_date.month, current_date.day))
        self.dateEdit2.date.dateChanged.connect(self.daysBetweenDates)
        
        self.dayEdit = EditWithLabel("Nombre de jour", self, placeholders=["Nombre de jour"])
        self.dayMove = self.dayEdit.lineEdit(0)
        self.dayEdit.lineEdit(0).setText("1")
        self.dayMove.textChanged.connect(self.validate_input)
        
        self.row_2.addLayout(self.dateEdit)
        self.row_2.addLayout(self.dateEdit2)
        self.row_2.addLayout(self.dayEdit)
        
        self.vBoxLayout.addWidget(self.title)
        self.vBoxLayout.addWidget(self.subTitle)
        self.vBoxLayout.addLayout(self.row)
        self.vBoxLayout.addLayout(self.motifEdit)
        self.vBoxLayout.addLayout(self.row_2)
        self.viewLayout.addLayout(self.vBoxLayout)
        
    def setMotifAutoComplete(self, data:list):
        self.completer = QCompleter(data, self.motifEdit.lineEdit(0))
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.motifEdit.lineEdit(0).setCompleter(self.completer)
        
    
    def unityChanged(self, text):
        is_day = text == "Jour"
        self.dateEdit2.date.setEnabled(is_day)
        self.dateEdit3.date.setEnabled(is_day)
        self.dayMove.setEnabled(is_day)
        self.isDay = is_day
            
    def validate_input(self, text):
        numeric_text = ''.join(filter(str.isdigit, text))
        self.dayMove.setText(numeric_text)
        
        
    def add_days_to_date(self, date_str, days_to_add):
        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, "%d/%m/%Y")
    
        # Add the specified number of days
        result_date = date + timedelta(days=float(days_to_add))
    
        # Format the result date as a string
        result_date_str = result_date.strftime("%d/%m/%Y")
    
        return result_date_str
        
    def daysBetweenDates(self, date):
        start_date = self.dateEdit.date.text()
        end_date = self.dateEdit2.date.text()
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        end_date = datetime.strptime(end_date, "%d/%m/%Y")
        delta = end_date - start_date
        if delta.days < 0:
            self.dayMove.setText("")
        else:
            self.dayMove.setText(str(delta.days + 1))