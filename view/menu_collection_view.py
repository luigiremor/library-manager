import tkinter
import customtkinter


class MenuCollection(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=650, width=1000)
        self.parent = parent
      