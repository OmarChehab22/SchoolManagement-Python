import json
from pathlib import Path
from models import Student, Instructor, Course


def save_all(file_path, students, instructors, courses):
    data={
        "students":[s.to_dict() for s in students],
        "instructors":[i.to_dict() for i in instructors],
        "courses":[c.to_dict() for c in courses],
        "version":1,
    }
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_all(file_path):
    path=Path(file_path)
    if not path.exists():
        return {"students":[], "instructors":[], "courses":[]}
    with open(file_path, "r", encoding="utf-8") as f:
        data=json.load(f)
    students=[Student.from_dict(x) for x in data.get("students", [])]
    instructors=[Instructor.from_dict(x) for x in data.get("instructors", [])]
    courses=[Course.from_dict(x) for x in data.get("courses", [])]
    return {"students":students, "instructors":instructors, "courses":courses} 