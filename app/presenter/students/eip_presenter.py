from .base_student_presenter import BaseStudentPresenter

class EipPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.eipInterface, parent) 
        self.mainView.subjectRefresh.connect(lambda level: self.setLabelIntoTable(self.promotionId, level))
        
    def fetchData(self, data):
        return super().fetchData(self.model.fetch_all(level="EIP"))
    
    def setPromotionId(self, promotionId):
        self.setLabelIntoTable(promotionId, level="EIP")
        return super().setPromotionId(promotionId)
    
    def handleResult(self, data: list):
        self.view.progressBar.setVisible(False)
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
        self.view.progressBar.setValue(0)
        self.workerThread.quit()
        self.view.parent.valueCount.setText(str(len(data)))
        