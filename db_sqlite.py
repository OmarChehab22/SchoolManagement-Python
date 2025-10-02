import sqlite3
from pathlib import Path
from models import Student, Instructor, Course


def get_connection(db_path):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn=sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL CHECK (age >= 0),
            email TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL CHECK (age >= 0),
            email TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            instructor_id TEXT,
            FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS registrations (
            student_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()


def upsert_student(conn, s):
    conn.execute(
        """
        INSERT INTO students (student_id, name, age, email)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET name=excluded.name, age=excluded.age, email=excluded.email
        """,
        (s.student_id, s.name, int(s.age), s.email),
    )
    conn.commit()


def delete_student(conn, student_id):
    conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()


def upsert_instructor(conn, i):
    conn.execute(
        """
        INSERT INTO instructors (instructor_id, name, age, email)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(instructor_id) DO UPDATE SET name=excluded.name, age=excluded.age, email=excluded.email
        """,
        (i.instructor_id, i.name, int(i.age), i.email),
    )
    conn.commit()


def delete_instructor(conn, instructor_id):
    conn.execute("DELETE FROM instructors WHERE instructor_id = ?", (instructor_id,))
    conn.commit()


def upsert_course(conn, c):
    conn.execute(
        """
        INSERT INTO courses (course_id, course_name, instructor_id)
        VALUES (?, ?, ?)
        ON CONFLICT(course_id) DO UPDATE SET course_name=excluded.course_name, instructor_id=excluded.instructor_id
        """,
        (c.course_id, c.course_name, c.instructor_id),
    )
    conn.execute("DELETE FROM registrations WHERE course_id = ?", (c.course_id,))
    if c.enrolled_student_ids:
        conn.executemany(
            "INSERT OR IGNORE INTO registrations (student_id, course_id) VALUES (?, ?)",
            [(sid, c.course_id) for sid in c.enrolled_student_ids],
        )
    conn.commit()


def delete_course(conn, course_id):
    conn.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
    conn.commit()


def list_students(conn):
    cur=conn.execute("SELECT student_id, name, age, email FROM students ORDER BY student_id")
    rows=cur.fetchall()
    return [Student(name=r[1], age=int(r[2]), _email=r[3], student_id=r[0]) for r in rows]


def list_instructors(conn):
    cur=conn.execute("SELECT instructor_id, name, age, email FROM instructors ORDER BY instructor_id")
    rows=cur.fetchall()
    return [Instructor(name=r[1], age=int(r[2]), _email=r[3], instructor_id=r[0]) for r in rows]


def list_courses(conn):
    cur=conn.execute("SELECT course_id, course_name, instructor_id FROM courses ORDER BY course_id")
    rows=cur.fetchall()
    courses=[Course(course_id=r[0], course_name=r[1], instructor_id=r[2]) for r in rows]
    for c in courses:
        cur=conn.execute("SELECT student_id FROM registrations WHERE course_id = ? ORDER BY student_id", (c.course_id,))
        c.enrolled_student_ids=[r[0] for r in cur.fetchall()]
    return courses


def backup_database(db_path, backup_path):
    src=Path(db_path)
    dst=Path(backup_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(f"file:{src}?mode=ro", uri=True) as src_conn:
        with sqlite3.connect(str(dst)) as dst_conn:
            src_conn.backup(dst_conn) 