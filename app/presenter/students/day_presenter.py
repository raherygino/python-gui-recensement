from .base_student_presenter import BaseStudentPresenter
from ...view.students.tab.day_student_tab import DayStudentTab
from ...common.constants import *

class StudentDayPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.dayInterface, parent)
        self.view : DayStudentTab = parent.view.dayInterface
        self.labels.append(LABEL.NB_DAY)
        self.view.tableView.setHorizontalHeaderLabels(self.labels)
        self.actions()
    
    def actions(self):
        self.view.parent.nParent.refresh.connect(self.refresh)
        
    def refresh(self, val):
        if "mouvement" in val:
            self.fetchData(self.model.fetch_all(**self.query))
            
    def handleResult(self, data: list):
        self.view.progressBar.setVisible(False)
        listData = []
        listData.clear()
        for student in data:
            listData.append([
                student.matricule,student.level,
                self.setLabelValue(student.company, LABEL.COMPANY), 
                self.setLabelValue(student.section, LABEL.SECTION),
                student.lastname, student.firstname, student.gender, student.day
            ])
            
        self.view.tableView.setData(listData)
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        self.view.parent.valueCount.setText(str(len(data)))
    
