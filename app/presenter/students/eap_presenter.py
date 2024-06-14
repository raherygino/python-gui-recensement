from .base_student_presenter import BaseStudentPresenter

class EapPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.eapInterface, parent)
        self.mainView.subjectRefresh.connect(lambda level: self.setLabelIntoTable(self.promotionId, level))
        
    def setPromotionId(self, promotionId):
        self.setLabelIntoTable(promotionId, level="EAP")
        return super().setPromotionId(promotionId)
    
    
    
        