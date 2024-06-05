from .base_student_presenter import BaseStudentPresenter

class StudentDbPresenter(BaseStudentPresenter):
    
    def __init__(self, parent):
        super().__init__(parent.view.dbInterface, parent)