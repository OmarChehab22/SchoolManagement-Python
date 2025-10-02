from __future__ import annotations
from dataclasses import dataclass, field
import re


EMAIL_REGEX=re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_email(email):
    if not EMAIL_REGEX.match(email or ""):
        raise ValueError("invalid email format")


def validate_age(age):
    if age is None or int(age)<0:
        raise ValueError("age must be non-negative integer")


@dataclass
class Person:
    name: str
    age: int
    _email: str

    def __post_init__(self):
        validate_age(self.age)
        validate_email(self._email)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        validate_email(value)
        self._email=value

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old."

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            age=int(data["age"]),
            _email=data.get("email") or data.get("_email", "")
        )


@dataclass
class Course:
    course_id: str
    course_name: str
    instructor_id: str|None=None
    enrolled_student_ids: list[str]=field(default_factory=list)

    def add_student(self, student):
        if student.student_id not in self.enrolled_student_ids:
            self.enrolled_student_ids.append(student.student_id)

    def assign_instructor(self, instructor):
        self.instructor_id=instructor.instructor_id

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor_id": self.instructor_id,
            "enrolled_student_ids": list(self.enrolled_student_ids),
            "type": "Course",
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            course_id=data["course_id"],
            course_name=data["course_name"],
            instructor_id=data.get("instructor_id"),
            enrolled_student_ids=list(data.get("enrolled_student_ids", [])),
        )


@dataclass
class Student(Person):
    student_id: str=""
    registered_course_ids: list[str]=field(default_factory=list)

    def register_course(self, course):
        if course.course_id not in self.registered_course_ids:
            self.registered_course_ids.append(course.course_id)

    def to_dict(self):
        data=super().to_dict()
        data.update({
            "student_id": self.student_id,
            "registered_course_ids": list(self.registered_course_ids),
        })
        return data

    @classmethod
    def from_dict(cls, data):
        base=Person.from_dict(data)
        return cls(
            name=base.name,
            age=base.age,
            _email=base.email,
            student_id=data["student_id"],
            registered_course_ids=list(data.get("registered_course_ids", [])),
        )


@dataclass
class Instructor(Person):
    instructor_id: str=""
    assigned_course_ids: list[str]=field(default_factory=list)

    def assign_course(self, course):
        if course.course_id not in self.assigned_course_ids:
            self.assigned_course_ids.append(course.course_id)

    def to_dict(self):
        data=super().to_dict()
        data.update({
            "instructor_id": self.instructor_id,
            "assigned_course_ids": list(self.assigned_course_ids),
        })
        return data

    @classmethod
    def from_dict(cls, data):
        base=Person.from_dict(data)
        return cls(
            name=base.name,
            age=base.age,
            _email=base.email,
            instructor_id=data["instructor_id"],
            assigned_course_ids=list(data.get("assigned_course_ids", [])),
        ) 