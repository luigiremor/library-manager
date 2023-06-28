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
    
    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text='Student List')
        self.title_label.pack(fill=tk.X, padx=5, pady=5)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.refresh_button = ctk.CTkButton(
            self.buttons_frame, text='Refresh', command=self.refresh_students)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.new_button = ctk.CTkButton(
            self.buttons_frame, text='New Student', command=self.new_student)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.update_button = ctk.CTkButton(
            self.buttons_frame, text='Update Student', command=self.update_student)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ctk.CTkButton(
            self.buttons_frame, text='Delete Student', command=None)
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
    
    
    def new_student(self):
        NewStudentForm(self)

    def update_student(self):
        selected = self.students_listbox.get()
        if selected:
            UpdateStudentForm(self, selected)
    

    def delete_student(self):
        pass


    def show_details(self, event=None):
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        selected = self.students_listbox.get()
        registration = selected.split(' - ')[0]

        if registration:
            details = self.controller.get_student_by_registration(registration)
            for key, value in details.items():
                label = ctk.CTkLabel(self.details_frame, text=f"{key}: {value}")
                label.pack()
    
    
    



class NewStudentForm(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title('New Student')
        self.controller: LibraryController = parent.controller
        self.select_label = ctk.CTkLabel(self, text="Student Data")
        self.select_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.name_label = ctk.CTkLabel(self, text="Name")
        self.name_label.grid(row=1, column=0, padx=10, pady=5)

        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.email_label = ctk.CTkLabel(self, text="Email")
        self.email_label.grid(row=2, column=0, padx=10, pady=5)

        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        self.cpf_label = ctk.CTkLabel(self, text="CPF")
        self.cpf_label.grid(row=3, column=0, padx=10, pady=5)

        self.cpf_entry = ctk.CTkEntry(self)
        self.cpf_entry.grid(row=3, column=1, padx=10, pady=5)

        self.tel_label = ctk.CTkLabel(self, text="Telephone")
        self.tel_label.grid(row=4, column=0, padx=10, pady=5)

        self.tel_entry = ctk.CTkEntry(self)
        self.tel_entry.grid(row=4, column=1, padx=10, pady=5)

        self.registration_label = ctk.CTkLabel(self, text="Registration")
        self.registration_label.grid(row=5, column=0, padx=10, pady=5)

        self.registration_entry = ctk.CTkEntry(self)
        self.registration_entry.grid(row=5, column=1, padx=10, pady=5)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.submit_button = ctk.CTkButton(self.button_frame, text="Add", command=self.create_student)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)


    def create_student(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        cpf = self.cpf_entry.get()
        tel = self.tel_entry.get()
        registration = self.registration_entry.get()
        if name and email and cpf and tel and registration:
            self.controller.create_student(name, email, cpf, tel, registration)
            self.parent.refresh_students()
            self.destroy()
        else:
            messagebox.showerror('Error', 'Fill all fields')



class UpdateStudentForm(ctk.CTkToplevel):
    def __init__(self, parent, student):
        super().__init__(parent)
        self.parent = parent
        self.controller = parent.controller
        self.title = 'Update Student'
        self.student = student

        self.name_label = ctk.CTkLabel(self, text="Name")
        self.name_label.grid(row=1, column=0, padx=10, pady=5)

        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.email_label = ctk.CTkLabel(self, text="Email")
        self.email_label.grid(row=2, column=0, padx=10, pady=5)

        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        self.cpf_label = ctk.CTkLabel(self, text="CPF")
        self.cpf_label.grid(row=3, column=0, padx=10, pady=5)

        self.cpf_entry = ctk.CTkEntry(self)
        self.cpf_entry.grid(row=3, column=1, padx=10, pady=5)

        self.tel_label = ctk.CTkLabel(self, text="Telephone")
        self.tel_label.grid(row=4, column=0, padx=10, pady=5)

        self.tel_entry = ctk.CTkEntry(self)
        self.tel_entry.grid(row=4, column=1, padx=10, pady=5)

        self.registration_label = ctk.CTkLabel(self, text="Registration")
        self.registration_label.grid(row=5, column=0, padx=10, pady=5)

        self.registration_entry = ctk.CTkEntry(self)
        self.registration_entry.grid(row=5, column=1, padx=10, pady=5)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.submit_button = ctk.CTkButton(self.button_frame, text="Update", command=None)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)