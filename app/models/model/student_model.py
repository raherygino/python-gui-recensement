from ..entity import Student, Subject
from .base_model import Model

class StudentModel(Model):
    def __init__(self):
        super().__init__("students", Student())
        
    def fetchNote(self, promotionId, items: list[Subject]):
        sql =  f'SELECT matricule, level, lastname, firstname, gender '
        sumCoef = sum([int(item.coef) for item in items])
        sql += f",{", ".join([item.abrv.replace("/","_") for item in items])}" if len(items) != 0 else ''
        sql += f",{", ".join([f'coef_{item.abrv.replace("/","_")}' for item in items])}" if len(items) != 0 else ''
        sql += f",{" + ".join([f'coef_{item.abrv.replace("/","_")}' for item in items])}" if len(items) != 0 else ''
        sql += " as total "
        sql += f",{" + ".join([f'coef_{item.abrv.replace("/","_")}' for item in items])}" if len(items) != 0 else ''
        sql += " as total2 "
        sql += f",({" + ".join([f'coef_{item.abrv.replace("/","_")}' for item in items])})/{sumCoef}" if len(items) != 0 else ''
        sql += f" FROM ({self.fetchNoteSQL(promotionId, items)})"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        all = cursor.fetchall()
        '''newResult = []
        for item in all:
            item = list(item)
            nItem = []
            for i in range(len(items)+5, (len(items)*2)+5):
                if item[i] == None:
                    nItem.append(0)
                else:
                    nItem.append(item[i])
                #nItem.append(item[i])
            item[len(item)-2] = sum(nItem)
            #newResult.append(tuple(item))
            total = item[len(item)-2]
            if total != None:
                item[len(item)-1] = total / sumCoef
            newResult.append(tuple(item))
        #print(newResult[0])'''
        return all
        #return []
    
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
    