import tkinter as tk
import customtkinter as ctk
from controller.library_controller import LibraryController
from components.ctk_listbox import CTkListbox
from tkinter import messagebox


class MenuStudents(ctk.CTkFrame):
    def __init__(self, parent, controller: LibraryController):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.grid(sticky="nsew")

        # configure grid to fill window
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 0, weight=1)

        self.create_widgets()
        self.refresh_students()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text='Student List')
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.go_back_button = ctk.CTkButton(
            self.buttons_frame, text='Go Back', command=lambda: self.parent.show_view('menu_main'))
        self.go_back_button.pack(side=tk.LEFT, padx=5)

        self.refresh_button = ctk.CTkButton(
            self.buttons_frame, text='Refresh', command=self.refresh_students)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.new_button = ctk.CTkButton(
            self.buttons_frame, text='Add Student', command=self.add_student)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ctk.CTkButton(
            self.buttons_frame, text='Update Student', command=self.update_student)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ctk.CTkButton(
            self.buttons_frame, text='Delete Student', command=self.delete_student)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.students_listbox = CTkListbox(
            self, width=200, height=300, command=self.show_details)
        self.students_listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_students(self):
        students = self.controller.get_all_students()
        self.students_listbox.clear()
        if students:
            for i, student in enumerate(students):
                title = student['registration'] + ' - ' + student['name']
                self.students_listbox.insert(i, title)

    def add_student(self):
        from view.student.add_student_form import AddStudentForm
        AddStudentForm(self)

    def update_student(self):
        registration_selected = self.students_listbox.get().split(' - ')[0]

        student = self.controller.get_student_by_registration(
            registration_selected)

        if student:
            from view.student.update_student_form import UpdateStudentForm
            UpdateStudentForm(self, student=student)

    def delete_student(self):
        selected = self.students_listbox.get()
        if selected:
            registration = selected.split(' - ')[0]
            self.controller.delete_student_by_registration(registration)
            self.refresh_students()

    def show_details(self, event=None):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected = self.students_listbox.get()
        registration = selected.split(' - ')[0]

        if registration:
            details = self.controller.get_student_by_registration(registration)
            for key, value in details.items():
                label = ctk.CTkLabel(self.details_frame,
                                     text=f"{key}: {value}")
                label.pack()
