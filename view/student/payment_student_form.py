import customtkinter as ctk
import tkinter as tk
from controller.library_controller import LibraryController
from tkinter import messagebox
from view.student.menu_students_view import MenuStudents


class PaymentStudentForm(ctk.CTkToplevel):
    def __init__(self, parent: MenuStudents, student: dict):
        super().__init__(parent)
        self.parent = parent
        self.student = student
        self.title('Payment')
        self.controller: LibraryController = parent.controller
        self.create_widgets()

    def create_widgets(self):
        self.select_label = ctk.CTkLabel(self, text="Student Payment Data")
        self.select_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.student_id_label = ctk.CTkLabel(self, text="Student ID")
        self.student_id_label.grid(row=1, column=0, padx=10, pady=5)

        self.student_id_entry = ctk.CTkEntry(self)
        self.student_id_entry.grid(row=1, column=1, padx=10, pady=5)
        self.student_id_entry.insert(0, self.student['id'])

        self.amount_label = ctk.CTkLabel(self, text="Amount")
        self.amount_label.grid(row=2, column=0, padx=10, pady=5)

        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)
        self.amount_entry.insert(0, self.student['fine_delay'])

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.submit_button = ctk.CTkButton(
            self.button_frame, text="Pay", command=self.pay_debt)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ctk.CTkButton(
            self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def pay_debt(self):
        student_id = self.student_id_entry.get()
        amount = self.amount_entry.get()

        if student_id and amount:
            try:
                amount = float(amount)  # ensure amount is a float
                self.controller.pay_student_debt(student_id, amount)
                messagebox.showinfo(
                    "Success", f"Student with id {student_id} paid successfully")
                self.parent.refresh_students()
                self.destroy()
            except ValueError as e:
                messagebox.showerror('Error', str(e))
        else:
            messagebox.showerror('Error', 'Fill all fields')
