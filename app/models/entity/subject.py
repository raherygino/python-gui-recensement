# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Subject(Entity):
    """Subject information """
    id: int = 0
    promotion_id: int = 0
    title: str = ""
    abrv: str = ""
    coef: int = 1
    level: str = ""