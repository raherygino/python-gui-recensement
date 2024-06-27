from .base_grades_presenter import BaseGradesPresenter

class EapPresenter(BaseGradesPresenter):
    def __init__(self, parent):
        super().__init__(parent.view.eapInterface, parent)
    
    
        