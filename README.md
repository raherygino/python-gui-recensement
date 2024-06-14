## Logiciel de gestion d'ecole

### TODO
- Hide menu eleves if no promotion
- Show year promotion
- Set spin box rank promotion
- Set Label form promotion
- Show add subject in eap & eap tab, hide in another tab
- Show subject added in the dialog of subject
- Update subject
- Delete subject


```SQL
SELECT students.id, students.lastname, marks.value as new_col FROM students JOIN marks ON students.id = marks.student_id

SELECT students.id, students.firstname, 
(SELECT
(SELECT subjects.abrv FROM subjects WHERE marks.subject_id = subjects.id) as subj
 FROM marks WHERE marks.student_id = students.id AND subj='SP') as SP,
(SELECT marks.value FROM marks WHERE marks.student_id = students.id) as vla
FROM students

SELECT lastname, SUM(CASE WHEN abrv = 'DPG' THEN value ELSE 0 END) as DPG, SUM(CASE WHEN abrv = 'SP' THEN value ELSE 0 END) as SP FROM 
(SELECT students.lastname, subjects.abrv, marks.value FROM students JOIN marks ON students.id = marks.student_id JOIN subjects ON marks.subject_id = subjects.id) as sTable 

```

