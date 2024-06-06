
from ..entity.subject import Subject
from .base_model import Model

class SubjectModel(Model):
    def __init__(self):
        super().__init__("subjects", Subject())