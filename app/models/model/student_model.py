from ..entity import Student, Subject
from .base_model import Model

class StudentModel(Model):
    def __init__(self):
        super().__init__("students", Student())
        
    def fetchNote(self, promotionId, items: list[Subject], level):
        sql =  f'SELECT matricule, level, lastname, firstname, gender '
        sumCoef = sum([int(item.coef) for item in items])
        sql += f",{", ".join([item.abrv.replace("/","_") for item in items])}" if len(items) != 0 else ''
        sql += f",{", ".join([f'coef_{item.abrv.replace("/","_")}' for item in items])}" if len(items) != 0 else ''
        sql += f",{" + ".join([f'coef_{item.abrv.replace("/","_")}' for item in items])}" if len(items) != 0 else ''
        sql += f" as total " if len(items) != 0 else ''
        sql += f",{" + ".join([f'coef_{item.abrv.replace("/","_")}' for item in items])}" if len(items) != 0 else ''
        sql += f" as total2 " if len(items) != 0 else ''
        sql += f",({" + ".join([f'coef_{item.abrv.replace("/","_")}' for item in items])})/{sumCoef}" if len(items) != 0 else ''
        sql += f" FROM ({self.fetchNoteSQL(promotionId, items)}) WHERE level = '{level}'"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        all = cursor.fetchall()
        return all
    
    def fetchNoteSQL(self, promotionId, items: list[Subject]) -> str:
        sql =  f'SELECT {self.TABLE}.matricule, {self.TABLE}.level, {self.TABLE}.lastname,' 
        sql += f'{self.TABLE}.firstname, {self.TABLE}.gender '
        sql += f",{",".join([self.markValue(item) for item in items])}" if len(items) != 0 else ''
        sql += f",{",".join([self.markValueWithCoef(item) for item in items])}" if len(items) != 0 else ''
        sql += f", {self.markValueTotal()}"
        sql += f' FROM {self.TABLE} WHERE {self.TABLE}.promotion_id = {promotionId}'
        return sql
        
    def markValue(self, item:Subject) -> str:
        return f'(SELECT marks.value FROM marks WHERE marks.student_id = students.id AND marks.subject_id = {item.id}) as {item.abrv.replace("/","_")}'
        
    def markValueTotal(self) -> str:
        return f'(SELECT sum(marks.value) FROM marks WHERE marks.student_id = students.id) as total'
    
    def markValueWithCoef(self, item:Subject) -> str:
        return f'(SELECT marks.value * {item.coef} FROM marks WHERE marks.student_id = students.id AND marks.subject_id = {item.id}) as coef_{item.abrv.replace("/","_")}'
    