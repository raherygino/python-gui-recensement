from app.models.entity.base_entity import Entity
from ..entity import Mouvement, Student
from .base_model import Model

class MouvementModel(Model):
    def __init__(self):
        self.table = "mouvements"
        super().__init__(self.table, Mouvement())
        self.student_model = StudentModel()
        
    def get_student(self, **kwargs):
        return super().fetch_all(**kwargs)[0]
        
    def create(self, mouvement: Mouvement):
        self.student_update_day(mouvement,"+")
        return super().create(mouvement)
    
    def student_update_day(self, mouvement, sing):
        student = self.student_model.fetch_item_by_id(mouvement.idStudent)
        if student != None:
            day = eval(f'{int(student.day)} {sing} {int(mouvement.day)}')
            self.student_model.update_item(student.id, day=str(day))
        
    def delete_by(self, **kwargs):
        items = super().fetch_all(**kwargs)
        if len(items) != 0:
            self.student_update_day(items[0],"-")
            return super().delete_by(**kwargs)
        
    def delete_mutlitple(self, items):
        conds = []
        values = []
        for item in items:
            conds.append({'promotion_id':item['promotion_id'], 'matricule': item['matricule']})
            values.append({"day": int(item['day'])})
            
        self.student_model.update_multiple_int(conds, values)
        return super().delete_mutlitple(items)
            
    def sumDay(self, *args): 
        cond = args[0] if len(args) != 0 else ""
        have = args[1] if len(args) > 1 else ""
        query = f'SELECT matricule, level, student, sum(day) as new_col FROM {self.table} {cond} GROUP BY matricule {f'HAVING sum(day) = {have}' if have != "" else ""}'
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
class StudentModel(Model):
    def __init__(self):
        super().__init__("students", Student())