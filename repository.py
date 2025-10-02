from __future__ import annotations
from models import Student, Instructor, Course
import storage_json
import db_sqlite


class Repository:
    def __init__(self):
        self.students={}
        self.instructors={}
        self.courses={}

    def add_or_update_student(self, student):
        self.students[student.student_id]=student

    def delete_student(self, student_id):
        self.students.pop(student_id, None)
        for c in self.courses.values():
            if student_id in c.enrolled_student_ids:
                c.enrolled_student_ids.remove(student_id)

    def add_or_update_instructor(self, instructor):
        self.instructors[instructor.instructor_id]=instructor

    def delete_instructor(self, instructor_id):
        self.instructors.pop(instructor_id, None)
        for c in self.courses.values():
            if c.instructor_id==instructor_id:
                c.instructor_id=None

    def add_or_update_course(self, course):
        self.courses[course.course_id]=course

    def delete_course(self, course_id):
        self.courses.pop(course_id, None)

    def register_student_to_course(self, student_id, course_id):
        if student_id not in self.students or course_id not in self.courses:
            return
        course=self.courses[course_id]
        if student_id not in course.enrolled_student_ids:
            course.enrolled_student_ids.append(student_id)
        student=self.students[student_id]
        if course_id not in student.registered_course_ids:
            student.registered_course_ids.append(course_id)

    def assign_instructor_to_course(self, instructor_id, course_id):
        if instructor_id not in self.instructors or course_id not in self.courses:
            return
        self.courses[course_id].instructor_id=instructor_id
        instructor=self.instructors[instructor_id]
        if course_id not in instructor.assigned_course_ids:
            instructor.assigned_course_ids.append(course_id)

    def save_json(self, path):
        storage_json.save_all(path, list(self.students.values()), list(self.instructors.values()), list(self.courses.values()))

    def load_json(self, path):
        data=storage_json.load_all(path)
        self.students={s.student_id: s for s in data["students"]}
        self.instructors={i.instructor_id: i for i in data["instructors"]}
        self.courses={c.course_id: c for c in data["courses"]}

    def sync_to_sqlite(self, db_path):
        conn=db_sqlite.get_connection(db_path)
        try:
            db_sqlite.init_db(conn)
            for s in self.students.values():
                db_sqlite.upsert_student(conn, s)
            for i in self.instructors.values():
                db_sqlite.upsert_instructor(conn, i)
            for c in self.courses.values():
                db_sqlite.upsert_course(conn, c)
        finally:
            conn.close()

    def load_from_sqlite(self, db_path):
        conn=db_sqlite.get_connection(db_path)
        try:
            db_sqlite.init_db(conn)
            students=db_sqlite.list_students(conn)
            instructors=db_sqlite.list_instructors(conn)
            courses=db_sqlite.list_courses(conn)
            self.students={s.student_id: s for s in students}
            self.instructors={i.instructor_id: i for i in instructors}
            self.courses={c.course_id: c for c in courses}
        finally:
            conn.close()

    def backup_sqlite(self, db_path, backup_path):
        db_sqlite.backup_database(db_path, backup_path) 