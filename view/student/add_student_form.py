
import customtkinter as ctk
import tkinter as tk
from components.ctk_listbox import CTkListbox

from controller.library_controller import LibraryController
from tkinter import messagebox

from view.student.menu_students_view import MenuStudents


class AddStudentForm(ctk.CTkToplevel):
    def __init__(self, parent: MenuStudents):
        super().__init__(parent)
        self.parent = parent
        self.title('Add Student')
        self.controller: LibraryController = parent.controller
        self.create_widgets()

    def create_widgets(self):
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

        self.submit_button = ctk.CTkButton(
            self.button_frame, text="Add", command=self.create_student)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ctk.CTkButton(
            self.button_frame, text="Cancel", command=self.destroy)
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
