# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Marks(Entity):
    """Marks information """
    id: int = 0
    promotion_id: int = 0
    student_id: int = 0
    subject_id: int = 0
    value: int = 0