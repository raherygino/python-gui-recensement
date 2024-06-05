# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Mouvement(Entity):
    id: int = 0
    idStudent: str = None
    promotion_id: int = 0
    level: str = ""
    matricule: str = ""
    company: int = 0
    section: int = 0
    student: str = ""
    gender: str = ""
    type: str = None
    subType: str = None
    motif: str = ""
    date_start: str = None
    date_end: str = None
    day: str = None