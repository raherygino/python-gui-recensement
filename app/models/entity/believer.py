 # coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Believer(Entity):
    """Believer information """
    id: int = 0
    id_conjoint: int = 0
    is_leader: int = 0
    lastname: str = ""
    firstname: str = ""
    gender: str = ""
    pos_family: str = ""
    address: str = ""
    region: str = ""
    diacon: str = ""
    birthday: str = ""
    birthplace: str = ""
    name_father: str = ""
    id_father: int = 0
    name_mother: str = ""
    id_mother: int = 0
    date_of_baptism: str = ""
    place_of_baptism: str = ""
    date_of_recipient: str = ""
    place_of_recipient: str = ""
    number_recipient: str = ""
    phone: str = ""
    dept_work: str = ""
    responsibility: str = ""