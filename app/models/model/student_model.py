from ..entity import Student, Subject
from .base_model import Model

class StudentModel(Model):
    def __init__(self):
        super().__init__("students", Student())
        
        
    def fetchNote(self, promotionId, items: list[Subject]):
        #sql = ",".join([str(item.abrv) for item in items])
        sql =  f'SELECT {self.TABLE}.matricule, {self.TABLE}.level, {self.TABLE}.lastname,' 
        sql += f'{self.TABLE}.firstname, {self.TABLE}.gender '
        sql += f",{",".join([self.markValue(item) for item in items])}" if len(items) != 0 else ''
        sql += f' FROM {self.TABLE} WHERE {self.TABLE}.promotion_id = {promotionId}'
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
        
    def markValue(self, item:Subject) -> str:
        return f'(SELECT marks.value FROM marks WHERE marks.student_id = students.id AND marks.subject_id = {item.id}) as {item.abrv.replace("/","_")}'
    