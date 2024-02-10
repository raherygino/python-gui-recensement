from qfluentwidgets import FluentIcon
from ..view import BelieverNewDialog

class BelieverPresenter:
    TEXT_NEW = "Ajouter"

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.menuWidget()

    def menuWidget(self):
        self.view.addButton(FluentIcon.ADD, self.TEXT_NEW)
        for action in self.view.commandBar.actions():
            if action.text() == self.TEXT_NEW:
                action.triggered.connect(lambda: self.showDialogNew())


    def showDialogNew(self):
        w = BelieverNewDialog(self.view)
        w.exec()