# LibraryView.py
import customtkinter
from controller.library_controller import LibraryController
from view.menu_auth_view import MenuAuth
from view.menu_collection_view import MenuCollection
from view.menu_main import MenuMain
from view.menu_register import MenuRegister
from view.menu_students_view import MenuStudents
from view.menu_lend_view import MenuLend
from view.menu_reservation_view import MenuReservation


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
            elif view_name == 'menu_reservation':
                self.views[view_name] = MenuReservation(self, self.controller)
            else:
                raise ValueError(f'No such view: {view_name}')

        return self.views[view_name]

    def show_view(self, view_name):
        if hasattr(self, 'current_view'):
            self.current_view.pack_forget()

        self.current_view = self.get_view(view_name)
        self.current_view.pack()

    def destroy(self):
        self.controller.close_connection()
        super().destroy()
