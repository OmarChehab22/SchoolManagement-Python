import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from repository import Repository
from models import Student, Instructor, Course
from csv_utils import export_to_csv


class TkApp:
    def __init__(self, root):
        self.root=root
        self.root.title("school management system")
        self.repo=Repository()
        self._build_ui()
        self._refresh_tables()

    def _build_ui(self):
        nb=ttk.Notebook(self.root)
        nb.pack(fill=tk.BOTH, expand=True)
        self.student_frame=ttk.Frame(nb)
        self.instructor_frame=ttk.Frame(nb)
        self.course_frame=ttk.Frame(nb)
        self.manage_frame=ttk.Frame(nb)
        nb.add(self.student_frame, text="students")
        nb.add(self.instructor_frame, text="instructors")
        nb.add(self.course_frame, text="courses")
        nb.add(self.manage_frame, text="manage")
        self._build_students_tab()
        self._build_instructors_tab()
        self._build_courses_tab()
        self._build_manage_tab()

    def _build_students_tab(self):
        frm=self.student_frame
        form=ttk.LabelFrame(frm, text="add/edit student")
        form.pack(fill=tk.X, padx=8, pady=8)
        self.s_id=tk.StringVar()
        self.s_name=tk.StringVar()
        self.s_age=tk.StringVar()
        self.s_email=tk.StringVar()
        for i,(label,var) in enumerate((("id",self.s_id),("name",self.s_name),("age",self.s_age),("email",self.s_email))):
            ttk.Label(form, text=label).grid(row=0, column=i*2, padx=4, pady=4, sticky=tk.W)
            ttk.Entry(form, textvariable=var, width=24).grid(row=0, column=i*2+1, padx=4, pady=4)
        ttk.Button(form, text="save", command=self._save_student).grid(row=0, column=8, padx=4)
        ttk.Button(form, text="delete", command=self._delete_student).grid(row=0, column=9, padx=4)
        search=ttk.LabelFrame(frm, text="search")
        search.pack(fill=tk.X, padx=8, pady=4)
        self.s_query=tk.StringVar()
        ttk.Entry(search, textvariable=self.s_query).pack(side=tk.LEFT, padx=4)
        ttk.Button(search, text="filter", command=self._refresh_students).pack(side=tk.LEFT)
        self.s_tree=ttk.Treeview(frm, columns=("id","name","age","email","courses"), show="headings", height=10)
        for c in ("id","name","age","email","courses"):
            self.s_tree.heading(c, text=c)
        self.s_tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.s_tree.bind("<<TreeviewSelect>>", self._on_student_select)

    def _build_instructors_tab(self):
        frm=self.instructor_frame
        form=ttk.LabelFrame(frm, text="add/edit instructor")
        form.pack(fill=tk.X, padx=8, pady=8)
        self.i_id=tk.StringVar(); self.i_name=tk.StringVar(); self.i_age=tk.StringVar(); self.i_email=tk.StringVar()
        for i,(label,var) in enumerate((("id",self.i_id),("name",self.i_name),("age",self.i_age),("email",self.i_email))):
            ttk.Label(form, text=label).grid(row=0, column=i*2, padx=4, pady=4, sticky=tk.W)
            ttk.Entry(form, textvariable=var, width=24).grid(row=0, column=i*2+1, padx=4, pady=4)
        ttk.Button(form, text="save", command=self._save_instructor).grid(row=0, column=8, padx=4)
        ttk.Button(form, text="delete", command=self._delete_instructor).grid(row=0, column=9, padx=4)
        search=ttk.LabelFrame(frm, text="search")
        search.pack(fill=tk.X, padx=8, pady=4)
        self.i_query=tk.StringVar()
        ttk.Entry(search, textvariable=self.i_query).pack(side=tk.LEFT, padx=4)
        ttk.Button(search, text="filter", command=self._refresh_instructors).pack(side=tk.LEFT)
        self.i_tree=ttk.Treeview(frm, columns=("id","name","age","email","courses"), show="headings", height=10)
        for c in ("id","name","age","email","courses"):
            self.i_tree.heading(c, text=c)
        self.i_tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.i_tree.bind("<<TreeviewSelect>>", self._on_instructor_select)

    def _build_courses_tab(self):
        frm=self.course_frame
        form=ttk.LabelFrame(frm, text="add/edit course")
        form.pack(fill=tk.X, padx=8, pady=8)
        self.c_id=tk.StringVar(); self.c_name=tk.StringVar(); self.c_instructor=tk.StringVar()
        for i,(label,var) in enumerate((("id",self.c_id),("name",self.c_name))):
            ttk.Label(form, text=label).grid(row=0, column=i*2, padx=4, pady=4, sticky=tk.W)
            ttk.Entry(form, textvariable=var, width=24).grid(row=0, column=i*2+1, padx=4, pady=4)
        ttk.Label(form, text="instructor").grid(row=0, column=4, padx=4, pady=4)
        self.c_instructor_cb=ttk.Combobox(form, textvariable=self.c_instructor, values=[], width=22)
        self.c_instructor_cb.grid(row=0, column=5, padx=4, pady=4)
        ttk.Button(form, text="save", command=self._save_course).grid(row=0, column=6, padx=4)
        ttk.Button(form, text="delete", command=self._delete_course).grid(row=0, column=7, padx=4)
        reg=ttk.LabelFrame(frm, text="register students")
        reg.pack(fill=tk.X, padx=8, pady=4)
        self.reg_course=tk.StringVar(); self.reg_student=tk.StringVar()
        self.reg_course_cb=ttk.Combobox(reg, textvariable=self.reg_course, values=[], width=24)
        self.reg_student_cb=ttk.Combobox(reg, textvariable=self.reg_student, values=[], width=24)
        ttk.Label(reg, text="course").grid(row=0, column=0, padx=4, pady=4)
        self.reg_course_cb.grid(row=0, column=1, padx=4, pady=4)
        ttk.Label(reg, text="student").grid(row=0, column=2, padx=4, pady=4)
        self.reg_student_cb.grid(row=0, column=3, padx=4, pady=4)
        ttk.Button(reg, text="register", command=self._register_student).grid(row=0, column=4, padx=4)
        assign=ttk.LabelFrame(frm, text="assign instructor")
        assign.pack(fill=tk.X, padx=8, pady=4)
        self.assign_course=tk.StringVar(); self.assign_instructor=tk.StringVar()
        self.assign_course_cb=ttk.Combobox(assign, textvariable=self.assign_course, values=[], width=24)
        self.assign_instructor_cb=ttk.Combobox(assign, textvariable=self.assign_instructor, values=[], width=24)
        ttk.Label(assign, text="course").grid(row=0, column=0, padx=4, pady=4)
        self.assign_course_cb.grid(row=0, column=1, padx=4, pady=4)
        ttk.Label(assign, text="instructor").grid(row=0, column=2, padx=4, pady=4)
        self.assign_instructor_cb.grid(row=0, column=3, padx=4, pady=4)
        ttk.Button(assign, text="assign", command=self._assign_instructor).grid(row=0, column=4, padx=4)
        self.c_tree=ttk.Treeview(frm, columns=("id","name","instructor","students"), show="headings", height=12)
        for c in ("id","name","instructor","students"):
            self.c_tree.heading(c, text=c)
        self.c_tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.c_tree.bind("<<TreeviewSelect>>", self._on_course_select)

    def _build_manage_tab(self):
        frm=self.manage_frame
        bar=ttk.Frame(frm)
        bar.pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(bar, text="save json", command=self._save_json).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="load json", command=self._load_json).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="sync to sqlite", command=self._sync_sqlite).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="load from sqlite", command=self._load_sqlite).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="export csv", command=self._export_csv).pack(side=tk.LEFT, padx=4)
        ttk.Button(bar, text="backup db", command=self._backup_db).pack(side=tk.LEFT, padx=4)

    def _save_student(self):
        try:
            s=Student(name=self.s_name.get().strip(), age=int(self.s_age.get()), _email=self.s_email.get().strip(), student_id=self.s_id.get().strip())
            self.repo.add_or_update_student(s)
            for cid in s.registered_course_ids:
                self.repo.register_student_to_course(s.student_id, cid)
            self._refresh_students()
        except Exception as e:
            messagebox.showerror("validation", str(e))

    def _delete_student(self):
        sid=self.s_id.get().strip()
        if not sid:
            return
        self.repo.delete_student(sid)
        self._refresh_students()

    def _on_student_select(self, _evt=None):
        sel=self.s_tree.selection()
        if not sel: return
        sid=self.s_tree.item(sel[0], 'values')[0]
        s=self.repo.students.get(sid)
        if s:
            self.s_id.set(s.student_id); self.s_name.set(s.name); self.s_age.set(str(s.age)); self.s_email.set(s.email)

    def _refresh_students(self):
        q=self.s_query.get().strip().lower()
        for i in self.s_tree.get_children(): self.s_tree.delete(i)
        for s in self.repo.students.values():
            if q and q not in s.student_id.lower() and q not in s.name.lower() and q not in s.email.lower():
                continue
            self.s_tree.insert('', tk.END, values=(s.student_id, s.name, s.age, s.email, ",".join(s.registered_course_ids)))
        self._refresh_comboboxes()

    def _save_instructor(self):
        try:
            i=Instructor(name=self.i_name.get().strip(), age=int(self.i_age.get()), _email=self.i_email.get().strip(), instructor_id=self.i_id.get().strip())
            self.repo.add_or_update_instructor(i)
            self._refresh_instructors()
        except Exception as e:
            messagebox.showerror("validation", str(e))

    def _delete_instructor(self):
        iid=self.i_id.get().strip()
        if not iid: return
        self.repo.delete_instructor(iid)
        self._refresh_instructors()

    def _on_instructor_select(self, _evt=None):
        sel=self.i_tree.selection()
        if not sel: return
        iid=self.i_tree.item(sel[0], 'values')[0]
        i=self.repo.instructors.get(iid)
        if i:
            self.i_id.set(i.instructor_id); self.i_name.set(i.name); self.i_age.set(str(i.age)); self.i_email.set(i.email)

    def _refresh_instructors(self):
        q=self.i_query.get().strip().lower()
        for i in self.i_tree.get_children(): self.i_tree.delete(i)
        for ins in self.repo.instructors.values():
            if q and q not in ins.instructor_id.lower() and q not in ins.name.lower() and q not in ins.email.lower():
                continue
            self.i_tree.insert('', tk.END, values=(ins.instructor_id, ins.name, ins.age, ins.email, ",".join(ins.assigned_course_ids)))
        self._refresh_comboboxes()

    def _save_course(self):
        cid=self.c_id.get().strip()
        name=self.c_name.get().strip()
        instr=self.c_instructor.get().strip() or None
        if not cid or not name:
            messagebox.showerror("validation", "course id and name are required")
            return
        c=Course(course_id=cid, course_name=name, instructor_id=instr, enrolled_student_ids=self.repo.courses.get(cid, Course(cid, name)).enrolled_student_ids)
        self.repo.add_or_update_course(c)
        self._refresh_courses()

    def _delete_course(self):
        cid=self.c_id.get().strip()
        if not cid: return
        self.repo.delete_course(cid)
        self._refresh_courses()

    def _register_student(self):
        cid=self.reg_course.get().strip(); sid=self.reg_student.get().strip()
        if not cid or not sid: return
        self.repo.register_student_to_course(sid, cid)
        self._refresh_courses(); self._refresh_students()

    def _assign_instructor(self):
        cid=self.assign_course.get().strip(); iid=self.assign_instructor.get().strip()
        if not cid or not iid: return
        self.repo.assign_instructor_to_course(iid, cid)
        self._refresh_courses(); self._refresh_instructors()

    def _on_course_select(self, _evt=None):
        sel=self.c_tree.selection()
        if not sel: return
        cid=self.c_tree.item(sel[0], 'values')[0]
        c=self.repo.courses.get(cid)
        if c:
            self.c_id.set(c.course_id); self.c_name.set(c.course_name); self.c_instructor.set(c.instructor_id or "")

    def _refresh_courses(self):
        for i in self.c_tree.get_children(): self.c_tree.delete(i)
        for c in self.repo.courses.values():
            self.c_tree.insert('', tk.END, values=(c.course_id, c.course_name, c.instructor_id or "", ",".join(c.enrolled_student_ids)))
        self._refresh_comboboxes()

    def _refresh_tables(self):
        self._refresh_students(); self._refresh_instructors(); self._refresh_courses()

    def _refresh_comboboxes(self):
        self.c_instructor_cb["values"]=sorted(self.repo.instructors.keys())
        self.reg_course_cb["values"]=sorted(self.repo.courses.keys())
        self.reg_student_cb["values"]=sorted(self.repo.students.keys())
        self.assign_course_cb["values"]=sorted(self.repo.courses.keys())
        self.assign_instructor_cb["values"]=sorted(self.repo.instructors.keys())

    def _save_json(self):
        path=filedialog.asksaveasfilename(defaultextension=".json", filetypes=[["JSON","*.json"]])
        if not path: return
        self.repo.save_json(path)
        messagebox.showinfo("saved", f"saved data to {path}")

    def _load_json(self):
        path=filedialog.askopenfilename(filetypes=[["JSON","*.json"]])
        if not path: return
        self.repo.load_json(path)
        self._refresh_tables()

    def _sync_sqlite(self):
        path=filedialog.asksaveasfilename(defaultextension=".db", filetypes=[["SQLite","*.db"]])
        if not path: return
        self.repo.sync_to_sqlite(path)
        messagebox.showinfo("synced", f"synced to {path}")

    def _load_sqlite(self):
        path=filedialog.askopenfilename(filetypes=[["SQLite","*.db"]])
        if not path: return
        self.repo.load_from_sqlite(path)
        self._refresh_tables()

    def _export_csv(self):
        path=filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[["CSV","*.csv"]])
        if not path: return
        export_to_csv(path, self.repo.students.values(), self.repo.instructors.values(), self.repo.courses.values())
        messagebox.showinfo("exported", f"exported csvs starting with {path}")

    def _backup_db(self):
        src=filedialog.askopenfilename(filetypes=[["SQLite","*.db"]])
        if not src: return
        dst=filedialog.asksaveasfilename(defaultextension=".db", filetypes=[["SQLite","*.db"]])
        if not dst: return
        from repository import db_sqlite
        db_sqlite.backup_database(src, dst)
        messagebox.showinfo("backup", f"database backed up to {dst}")


def main():
    root=tk.Tk()
    TkApp(root)
    root.mainloop()


if __name__=="__main__":
    main() 