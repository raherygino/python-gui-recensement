from PyQt5.QtWidgets import QTableWidgetItem
from .base_student_presenter import BaseStudentPresenter
#from .students_presenter import StudentsPresenter
from ...models import StudentModel
from ...view import EipTab
from ...common.constants import *

class EipPresenter:
    
    def __init__(self, parent):
        self.view:EipTab = parent.view.eipInterface
        self.model:StudentModel = parent.model
        self.modelSubject = parent.modelSubject
        self.sPresenter = parent
        self.labels = [
            LABEL.MATRICULE, LABEL.GRADE, LABEL.COMPANY, LABEL.SECTION, 
            LABEL.LASTNAME,LABEL.FIRSTNAME, LABEL.GENDER]
        self.tableWidget = self.view.tableView
        self.tableWidget.doubleClicked.connect(self.reset_table)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(len(self.labels))
        self.tableWidget.setHorizontalHeaderLabels(self.labels)
        data = self.model.fetch_all(level="EIP")
        listData = []
        listData.clear()
        for student in data:
            listData.append([
                student.matricule,student.level,
                self.setLabelValue(student.company, "Compagnie"), 
                self.setLabelValue(student.section, "Section"),
                 student.lastname, student.firstname, student.gender
            ])
            
        self.view.tableView.setData(listData)
        
    def setLabelValue(self, index, label):
        key = "ère" if index == 1 else "ème"
        return f'{index}{key} {label}'
    
    def reset_table(self):
        self.tableWidget.clear()  # Clear all data
        self.tableWidget.setRowCount(2)  # Reset row count
        self.tableWidget.setColumnCount(0)  # Reset column count
        #newHeaders = [item for sublist in zip(self.labels, ['New Header 1', 'New Header 2']) for item in sublist]  # New headers
        labels = [label for label in self.labels]
        newHeaders =  [subject.abrv for subject in self.modelSubject.fetch_all(promotion_id=self.sPresenter.promotionId, level=self.sPresenter.getLevel())]
        labels.extend(newHeaders)
        self.tableWidget.setColumnCount(len(labels))
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('John'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('30'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem('Alice'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('25'))