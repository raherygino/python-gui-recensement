from .base_student_presenter import BaseStudentPresenter

class EapPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.eapInterface, parent)
        
    def setPromotionId(self, promotionId):
        self.setLabelIntoTable(promotionId, level="EAP")
        return super().setPromotionId(promotionId)
    
        