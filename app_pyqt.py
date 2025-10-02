import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox
)
from repository import Repository
from models import Student, Instructor, Course
from csv_utils import export_to_csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("school management system")
        self.repo=Repository()
        self.tabs=QTabWidget()
        self.setCentralWidget(self.tabs)
        self._init_students_tab()
        self._init_instructors_tab()
        self._init_courses_tab()
        self._init_manage_tab()
        self._refresh_all()

    def _init_students_tab(self):
        w=QWidget(); layout=QVBoxLayout(w)
        form=QHBoxLayout()
        self.s_id=QLineEdit(); self.s_name=QLineEdit(); self.s_age=QLineEdit(); self.s_email=QLineEdit()
        for label,widget in (("id",self.s_id),("name",self.s_name),("age",self.s_age),("email",self.s_email)):
            form.addWidget(QLabel(label)); form.addWidget(widget)
        save_btn=QPushButton("save"); del_btn=QPushButton("delete")
        save_btn.clicked.connect(self._save_student); del_btn.clicked.connect(self._delete_student)
        form.addWidget(save_btn); form.addWidget(del_btn)
        layout.addLayout(form)
        search_row=QHBoxLayout(); self.s_query=QLineEdit();
        search_row.addWidget(QLabel("search")); search_row.addWidget(self.s_query)
        filter_btn=QPushButton("filter"); filter_btn.clicked.connect(self._refresh_students)
        search_row.addWidget(filter_btn)
        layout.addLayout(search_row)
        self.s_table=QTableWidget(0, 5); self.s_table.setHorizontalHeaderLabels(["id","name","age","email","courses"])
        self.s_table.cellClicked.connect(self._on_student_row)
        layout.addWidget(self.s_table)
        self.tabs.addTab(w, "students")

    def _init_instructors_tab(self):
        w=QWidget(); layout=QVBoxLayout(w)
        form=QHBoxLayout()
        self.i_id=QLineEdit(); self.i_name=QLineEdit(); self.i_age=QLineEdit(); self.i_email=QLineEdit()
        for label,widget in (("id",self.i_id),("name",self.i_name),("age",self.i_age),("email",self.i_email)):
            form.addWidget(QLabel(label)); form.addWidget(widget)
        save_btn=QPushButton("save"); del_btn=QPushButton("delete")
        save_btn.clicked.connect(self._save_instructor); del_btn.clicked.connect(self._delete_instructor)
        form.addWidget(save_btn); form.addWidget(del_btn)
        layout.addLayout(form)
        search_row=QHBoxLayout(); self.i_query=QLineEdit();
        search_row.addWidget(QLabel("search")); search_row.addWidget(self.i_query)
        filter_btn=QPushButton("filter"); filter_btn.clicked.connect(self._refresh_instructors)
        search_row.addWidget(filter_btn)
        layout.addLayout(search_row)
        self.i_table=QTableWidget(0, 5); self.i_table.setHorizontalHeaderLabels(["id","name","age","email","courses"])
        self.i_table.cellClicked.connect(self._on_instructor_row)
        layout.addWidget(self.i_table)
        self.tabs.addTab(w, "instructors")

    def _init_courses_tab(self):
        w=QWidget(); layout=QVBoxLayout(w)
        form=QHBoxLayout()
        self.c_id=QLineEdit(); self.c_name=QLineEdit(); self.c_instructor=QComboBox()
        form.addWidget(QLabel("id")); form.addWidget(self.c_id)
        form.addWidget(QLabel("name")); form.addWidget(self.c_name)
        form.addWidget(QLabel("instructor")); form.addWidget(self.c_instructor)
        save_btn=QPushButton("save"); del_btn=QPushButton("delete")
        save_btn.clicked.connect(self._save_course); del_btn.clicked.connect(self._delete_course)
        form.addWidget(save_btn); form.addWidget(del_btn)
        layout.addLayout(form)
        reg_row=QHBoxLayout()
        self.reg_course=QComboBox(); self.reg_student=QComboBox()
        reg_row.addWidget(QLabel("course")); reg_row.addWidget(self.reg_course)
        reg_row.addWidget(QLabel("student")); reg_row.addWidget(self.reg_student)
        reg_btn=QPushButton("register"); reg_btn.clicked.connect(self._register_student)
        reg_row.addWidget(reg_btn)
        layout.addLayout(reg_row)
        assign_row=QHBoxLayout()
        self.assign_course=QComboBox(); self.assign_instructor=QComboBox()
        assign_row.addWidget(QLabel("course")); assign_row.addWidget(self.assign_course)
        assign_row.addWidget(QLabel("instructor")); assign_row.addWidget(self.assign_instructor)
        assign_btn=QPushButton("assign"); assign_btn.clicked.connect(self._assign_instructor)
        assign_row.addWidget(assign_btn)
        layout.addLayout(assign_row)
        self.c_table=QTableWidget(0, 4); self.c_table.setHorizontalHeaderLabels(["id","name","instructor","students"])
        self.c_table.cellClicked.connect(self._on_course_row)
        layout.addWidget(self.c_table)
        self.tabs.addTab(w, "courses")

    def _init_manage_tab(self):
        w=QWidget(); layout=QHBoxLayout(w)
        btns=[
            ("save json", self._save_json),
            ("load json", self._load_json),
            ("sync to sqlite", self._sync_sqlite),
            ("load from sqlite", self._load_sqlite),
            ("export csv", self._export_csv),
            ("backup db", self._backup_db),
        ]
        for label,slot in btns:
            b=QPushButton(label); b.clicked.connect(slot); layout.addWidget(b)
        self.tabs.addTab(w, "manage")

    def _refresh_all(self):
        self._refresh_students(); self._refresh_instructors(); self._refresh_courses(); self._refresh_combos()

    def _refresh_students(self):
        q=self.s_query.text().strip().lower()
        rows=[s for s in self.repo.students.values() if not q or q in s.student_id.lower() or q in s.name.lower() or q in s.email.lower()]
        self.s_table.setRowCount(0)
        for s in rows:
            r=self.s_table.rowCount(); self.s_table.insertRow(r)
            self.s_table.setItem(r, 0, QTableWidgetItem(s.student_id))
            self.s_table.setItem(r, 1, QTableWidgetItem(s.name))
            self.s_table.setItem(r, 2, QTableWidgetItem(str(s.age)))
            self.s_table.setItem(r, 3, QTableWidgetItem(s.email))
            self.s_table.setItem(r, 4, QTableWidgetItem(",".join(s.registered_course_ids)))
        self._refresh_combos()

    def _refresh_instructors(self):
        q=self.i_query.text().strip().lower()
        rows=[i for i in self.repo.instructors.values() if not q or q in i.instructor_id.lower() or q in i.name.lower() or q in i.email.lower()]
        self.i_table.setRowCount(0)
        for ins in rows:
            r=self.i_table.rowCount(); self.i_table.insertRow(r)
            self.i_table.setItem(r, 0, QTableWidgetItem(ins.instructor_id))
            self.i_table.setItem(r, 1, QTableWidgetItem(ins.name))
            self.i_table.setItem(r, 2, QTableWidgetItem(str(ins.age)))
            self.i_table.setItem(r, 3, QTableWidgetItem(ins.email))
            self.i_table.setItem(r, 4, QTableWidgetItem(",".join(ins.assigned_course_ids)))
        self._refresh_combos()

    def _refresh_courses(self):
        self.c_table.setRowCount(0)
        for c in self.repo.courses.values():
            r=self.c_table.rowCount(); self.c_table.insertRow(r)
            self.c_table.setItem(r, 0, QTableWidgetItem(c.course_id))
            self.c_table.setItem(r, 1, QTableWidgetItem(c.course_name))
            self.c_table.setItem(r, 2, QTableWidgetItem(c.instructor_id or ""))
            self.c_table.setItem(r, 3, QTableWidgetItem(",".join(c.enrolled_student_ids)))
        self._refresh_combos()

    def _refresh_combos(self):
        self.c_instructor.clear(); self.c_instructor.addItems(sorted(self.repo.instructors.keys()))
        self.reg_course.clear(); self.reg_course.addItems(sorted(self.repo.courses.keys()))
        self.reg_student.clear(); self.reg_student.addItems(sorted(self.repo.students.keys()))
        self.assign_course.clear(); self.assign_course.addItems(sorted(self.repo.courses.keys()))
        self.assign_instructor.clear(); self.assign_instructor.addItems(sorted(self.repo.instructors.keys()))

    def _save_student(self):
        try:
            s=Student(name=self.s_name.text().strip(), age=int(self.s_age.text()), _email=self.s_email.text().strip(), student_id=self.s_id.text().strip())
            self.repo.add_or_update_student(s)
            self._refresh_students()
        except Exception as e:
            QMessageBox.critical(self, "validation", str(e))

    def _delete_student(self):
        sid=self.s_id.text().strip()
        if not sid: return
        self.repo.delete_student(sid)
        self._refresh_students()

    def _on_student_row(self, row, _col):
        self.s_id.setText(self.s_table.item(row, 0).text())
        self.s_name.setText(self.s_table.item(row, 1).text())
        self.s_age.setText(self.s_table.item(row, 2).text())
        self.s_email.setText(self.s_table.item(row, 3).text())

    def _save_instructor(self):
        try:
            i=Instructor(name=self.i_name.text().strip(), age=int(self.i_age.text()), _email=self.i_email.text().strip(), instructor_id=self.i_id.text().strip())
            self.repo.add_or_update_instructor(i)
            self._refresh_instructors()
        except Exception as e:
            QMessageBox.critical(self, "validation", str(e))

    def _delete_instructor(self):
        iid=self.i_id.text().strip()
        if not iid: return
        self.repo.delete_instructor(iid)
        self._refresh_instructors()

    def _on_instructor_row(self, row, _col):
        self.i_id.setText(self.i_table.item(row, 0).text())
        self.i_name.setText(self.i_table.item(row, 1).text())
        self.i_age.setText(self.i_table.item(row, 2).text())
        self.i_email.setText(self.i_table.item(row, 3).text())

    def _save_course(self):
        cid=self.c_id.text().strip(); name=self.c_name.text().strip(); instr=self.c_instructor.currentText().strip() or None
        if not cid or not name:
            QMessageBox.critical(self, "validation", "course id and name are required"); return
        enrolled=self.repo.courses.get(cid, Course(cid, name)).enrolled_student_ids
        c=Course(course_id=cid, course_name=name, instructor_id=instr, enrolled_student_ids=enrolled)
        self.repo.add_or_update_course(c)
        self._refresh_courses()

    def _delete_course(self):
        cid=self.c_id.text().strip()
        if not cid: return
        self.repo.delete_course(cid)
        self._refresh_courses()

    def _register_student(self):
        cid=self.reg_course.currentText().strip(); sid=self.reg_student.currentText().strip()
        if not cid or not sid: return
        self.repo.register_student_to_course(sid, cid)
        self._refresh_courses(); self._refresh_students()

    def _assign_instructor(self):
        cid=self.assign_course.currentText().strip(); iid=self.assign_instructor.currentText().strip()
        if not cid or not iid: return
        self.repo.assign_instructor_to_course(iid, cid)
        self._refresh_courses(); self._refresh_instructors()

    def _on_course_row(self, row, _col):
        self.c_id.setText(self.c_table.item(row, 0).text())
        self.c_name.setText(self.c_table.item(row, 1).text())
        self.c_instructor.setCurrentText(self.c_table.item(row, 2).text())

    def _save_json(self):
        path,_=QFileDialog.getSaveFileName(self, "save json", filter="JSON (*.json)")
        if not path: return
        self.repo.save_json(path)
        QMessageBox.information(self, "saved", f"saved to {path}")

    def _load_json(self):
        path,_=QFileDialog.getOpenFileName(self, "load json", filter="JSON (*.json)")
        if not path: return
        self.repo.load_json(path)
        self._refresh_all()

    def _sync_sqlite(self):
        path,_=QFileDialog.getSaveFileName(self, "sync to sqlite", filter="SQLite (*.db)")
        if not path: return
        self.repo.sync_to_sqlite(path)
        QMessageBox.information(self, "synced", f"synced to {path}")

    def _load_sqlite(self):
        path,_=QFileDialog.getOpenFileName(self, "load from sqlite", filter="SQLite (*.db)")
        if not path: return
        self.repo.load_from_sqlite(path)
        self._refresh_all()

    def _export_csv(self):
        path,_=QFileDialog.getSaveFileName(self, "export csv", filter="CSV (*.csv)")
        if not path: return
        export_to_csv(path, self.repo.students.values(), self.repo.instructors.values(), self.repo.courses.values())
        QMessageBox.information(self, "exported", f"exported csv starting with {path}")

    def _backup_db(self):
        src,_=QFileDialog.getOpenFileName(self, "select db to backup", filter="SQLite (*.db)")
        if not src: return
        dst,_=QFileDialog.getSaveFileName(self, "backup to", filter="SQLite (*.db)")
        if not dst: return
        import db_sqlite
        db_sqlite.backup_database(src, dst)
        QMessageBox.information(self, "backup", f"database backed up to {dst}")


def main():
    app=QApplication(sys.argv)
    w=MainWindow(); w.resize(1000, 600); w.show()
    sys.exit(app.exec_())


if __name__=="__main__":
    main() 