
from ..entity import Subject
from .base_model import Model
from .mark_model import MarkModel 

class SubjectModel(Model):
    def __init__(self):
        super().__init__("subjects", Subject())
        
    def delete_item(self, item_id):
        markModel = MarkModel()
        markModel.delete_by(subject_id=item_id)
        return super().delete_item(item_id)