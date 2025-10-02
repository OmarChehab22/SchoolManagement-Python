import csv
from pathlib import Path


def export_to_csv(base_path, students, instructors, courses):
    base=Path(base_path)
    base.parent.mkdir(parents=True, exist_ok=True)
    with open(base.with_suffix('').as_posix()+"_students.csv", "w", newline='', encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["student_id","name","age","email","registered_course_ids"])
        for s in students:
            w.writerow([s.student_id, s.name, s.age, s.email, ";".join(s.registered_course_ids)])
    with open(base.with_suffix('').as_posix()+"_instructors.csv", "w", newline='', encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["instructor_id","name","age","email","assigned_course_ids"])
        for i in instructors:
            w.writerow([i.instructor_id, i.name, i.age, i.email, ";".join(i.assigned_course_ids)])
    with open(base.with_suffix('').as_posix()+"_courses.csv", "w", newline='', encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["course_id","course_name","instructor_id","enrolled_student_ids"])
        for c in courses:
            w.writerow([c.course_id, c.course_name, c.instructor_id or "", ";".join(c.enrolled_student_ids)]) 