from .base_student_presenter import BaseStudentPresenter
from ...models import Marks
from ...common.constants import LABEL
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer

class EipPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.eipInterface, parent) 
        self.labels = [LABEL.MATRICULE, LABEL.GRADE,LABEL.LASTNAME,LABEL.FIRSTNAME, LABEL.GENDER]
        self.mainView.subjectRefresh.connect(lambda level: self.setLabelIntoTable(self.promotionId, level))
        self.view.tableView.itemChanged.connect(self.itemChanged)
        self.subjects = []
        self.data = []
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.fetchAll)
        
    def fetchData(self, data):
        self.view.progressBar.setVisible(True)
        self.timer.start()
        
    def fetchAll(self):
        self.subjects = self.modelSubject.fetch_all(promotion_id=self.promotionId, level="EIP")
        #self.data = 
        self.actionWorkerThread(self.model.fetchNote(self.promotionId, self.subjects))
        self.timer.stop()
        
    def findSubjectIdByAbrv(self, abrv:str):
        subjectId = 0
        for subject in self.modelSubject.fetch_all(promotion_id=self.promotionId, level="EIP"):
            if subject.abrv == abrv:
                subjectId = subject.id
        return subjectId
            
    def findStudentIdByMatricule(self, matricule:int):
        studentId = 0
        for student in self.defaultData:
            if student.matricule == matricule:
                studentId = student.id
        return studentId
         
    def itemChanged(self, item):
        value = item.text()
        if item.column() > 4 and value != "":
            value = float(value)
            value = str("{:.2f}".format(value))
            vls = value.split('.')
            value = vls[0] if vls[1] == "00" else value
            item.setText(str(value))
            matricule = self.view.tableView.item(item.row(), 0).text()
            abrv = self.view.tableView.horizontalHeaderItem(item.column()).text()
            studentId = self.findStudentIdByMatricule(int(matricule))
            subjectId = self.findSubjectIdByAbrv(abrv)
            mark = Marks(promotion_id=self.promotionId, student_id=studentId, subject_id=subjectId, value=value)
            marks = self.modelMark.fetch_all(student_id=studentId, subject_id=subjectId)
            if len(marks) == 0:
                self.modelMark.prepareCreate(mark)
            else:
                self.modelMark.update_item(marks[0].id, value=str(mark.value))
            self.modelMark.commit()
            
    def setPromotionId(self, promotionId):
        self.setLabelIntoTable(promotionId, level="EIP")
        return super().setPromotionId(promotionId)
    
    def handleResult(self, data: list):
        self.view.progressBar.setVisible(False)
        listData = []
        lenSub = len(self.subjects)
        for item in data:
            nItem  = list(item)
            listData.append(nItem)
        self.view.tableView.setData(listData)
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        self.view.parent.valueCount.setText(str(len(listData)))
        