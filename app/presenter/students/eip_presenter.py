from .base_grades_presenter import BaseGradesPresenter

class EipPresenter(BaseGradesPresenter):
    def __init__(self, parent):
        super().__init__(parent.view.eipInterface, parent)