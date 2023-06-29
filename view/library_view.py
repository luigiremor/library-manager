# LibraryView.py
import customtkinter
from controller.library_controller import LibraryController
from view.menu_auth_view import MenuAuth
from view.menu_collection_view import MenuCollection
from view.menu_main import MenuMain
from view.menu_register import MenuRegister
from view.menu_students_view import MenuStudents
from view.menu_lend_view import MenuLend


class LibraryView(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.controller = LibraryController('library.db')
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.title("Library - System")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.views = {}

        self.show_view('menu_auth')

    def get_view(self, view_name):
        if view_name not in self.views:
            if view_name == 'menu_auth':
                self.views[view_name] = MenuAuth(self, self.controller)
            elif view_name == 'menu_register':
                self.views[view_name] = MenuRegister(self, self.controller)
            elif view_name == 'menu_main':
                self.views[view_name] = MenuMain(self, self.controller)
            elif view_name == 'menu_students':
                self.views[view_name] = MenuStudents(self, self.controller)
            elif view_name == 'menu_collection':
                self.views[view_name] = MenuCollection(self, self.controller)
            elif view_name == 'menu_lend':
                self.views[view_name] = MenuLend(self, self.controller)
            else:
                raise ValueError(f'No such view: {view_name}')

        return self.views[view_name]

    def show_view(self, view_name):

        if hasattr(self, 'current_view'):
            self.current_view.grid_forget()

        self.current_view = self.get_view(view_name)
        if view_name == 'menu_auth' or view_name == 'menu_register':
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            # Coloca o widget no centro da célula da grade
            self.current_view.grid(sticky="nsew")

            # Centraliza a célula da grade na janela
            self.update_idletasks()
            window_width = self.winfo_width()
            window_height = self.winfo_height()
            self.current_view_width = self.current_view.winfo_reqwidth()
            self.current_view_height = self.current_view.winfo_reqheight()
            x_offset = abs((window_width - self.current_view_width)) // 2
            y_offset = abs((window_height - self.current_view_height)) // 2
            self.current_view.grid_configure(padx=x_offset, pady=y_offset)

        else:
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.current_view.grid(sticky="nsew")

    def destroy(self):
        self.controller.close_connection()
        super().destroy()
