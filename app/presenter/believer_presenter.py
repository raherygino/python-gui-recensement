from qfluentwidgets import FluentIcon
from ..view import BelieverNewDialog
from ..models import Believer, Model
class BelieverPresenter:
    TEXT_NEW = "Ajouter"

    def __init__(self, view, model: Model):
        self.view = view
        self.model = model
        self.menuWidget()
        '''for i in range(80):
            model.create(Believer(firstname=f"FirstName {i}", lastname=f"LastName {i}"))'''
        
        self.view.populateTable(self.model.fetch_all_items())

    def menuWidget(self):
        self.view.addButton(FluentIcon.ADD, self.TEXT_NEW)
        for action in self.view.commandBar.actions():
            if action.text() == self.TEXT_NEW:
                action.triggered.connect(lambda: self.showDialogNew())

    def showDialogNew(self):
        w = BelieverNewDialog(self.view)
        if w.exec():
            lastname = w.lastnameEdit.text(0)
            firstname = w.firstnameEdit.text(0)
            address = w.addressEdit.text(0)
            region = w.regionEdit.text(0)
            diacon = w.diaconEdit.text(0)
            birthday = w.birthdayEdit.text(0)
            birthplace = w.birthdayEdit.text(1)
            nameFather = w.nameFatherEdit.text(0)
            nameMother = w.nameMotherEdit.text(0)
            dateBaptism = w.baptismEdit.text(0)
            placeBaptism = w.baptismEdit.text(1)
            dateRecipient = w.recipientEdit.text(0)
            placeRecipient = w.recipientEdit.text(1)
            numberRecipient = w.recipientEdit.text(2)
            phone = w.phoneEdit.text(0)
            deptWork = w.deptWorkEdit.text(0)
            responsability = w.responsibilityEdit.text(0)
            
            believer = Believer(
                lastname=lastname,
                firstname=firstname,
                address=address,
                region=region,
                diacon=diacon,
                birthday=birthday,
                birthplace=birthplace,
                name_father=nameFather,
                name_mother=nameMother,
                date_of_baptism=dateBaptism,
                place_of_baptism=placeBaptism,
                date_of_recipient=dateRecipient,
                place_of_recipient=placeRecipient,
                number_recipient=numberRecipient,
                phone=phone,
                dept_work=deptWork,
                responsibility=responsability
            )
            
            self.model.create(believer)
            self.view.populateTable(self.model.fetch_all_items())