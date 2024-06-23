from ..entity.promotion import Promotion
from .base_model import Model
from .student_model import StudentModel
from .subject_model import SubjectModel
from .mark_model  import MarkModel

class PromotionModel(Model):
    def __init__(self):
        super().__init__("promotions", Promotion())
        
    def delete_item(self, item_id):
        StudentModel().delete_with_cond(promotion_id=item_id)
        SubjectModel().delete_with_cond(promotion_id=item_id)
        MarkModel().delete_with_cond(promotion_id=item_id)
        return super().delete_item(item_id)
    
    def delete_all_student(self, item_id):
        self.model_student.delete_with_cond(promotion_id=item_id)