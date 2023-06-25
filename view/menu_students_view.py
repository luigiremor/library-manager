import tkinter as tk
import customtkinter 


class MenuStudents(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=650, width=1000)
        self.parent = parent
        self.listbox_students = tk.Listbox(self)
        self.listbox_students.pack()
    

    def show_students(self, students):
        self.listbox_students.delete(0, tk.END)
        for student in students:
            self.listbox_students.insert(tk.END, student)
        
        
        