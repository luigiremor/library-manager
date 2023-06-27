import tkinter as tk
import customtkinter as ctk
from controller.library_controller import LibraryController
from components.ctk_listbox import CTkListbox


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
            self.buttons_frame, text='Update Student', command=None)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ctk.CTkButton(
            self.buttons_frame, text='Delete Student', command=None)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.students_listbox = CTkListbox(
            self, width=200, height=300, command=None)
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

        self.submit_button = ctk.CTkButton(self.button_frame, text="Submit", command=None)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
    