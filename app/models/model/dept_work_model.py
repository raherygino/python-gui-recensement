from ..entity import DeptWork
from .base_model import Model

class DeptWorkModel(Model):
    def __init__(self):
        super().__init__("dept_works", DeptWork())