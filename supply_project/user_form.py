import tkinter as tk

from user_db import save_user, update_user
from models import User

class UserForm:
    def __init__(self, parent, refresh_treeview, user = None, name = None):
        self.user = user
        self.name = name
        self.name_user_entry = None
        self.refresh_treeview = refresh_treeview

        # Tworzenie okna
        self.window = tk.Toplevel(parent)
        self.window.geometry('400x200')
        self.window.grab_set()
        self.window.transient(parent)

        # Tworzenie formularza

        if user:
            self.window.title("Edytuj użytkownika")
        else:
            self.window.title("Dodaj użytkownika")
        save_button = tk.Button(self.window, text="Zapisz", command=self.save)
        save_button.grid(row=4, column=0, columnspan=2)
        
        self.create_form()

        
    def create_form(self):
        # Etykiety
        tk.Label(self.window, text="Użytkownik:").grid(row=0, column=0, sticky='w')

        # Tworzenie pól formularza
        self.name_user_entry = tk.Entry(self.window)
        # Rozmieszczenie elementów w siatce
        self.name_user_entry.grid(row=0, column=1, sticky='w')


    def save(self):
        # Pobieranie danych z formularza
        name = self.name_user_entry.get()
        

        # Sprawdzamy, czy aktualizujemy użytkownika, czy dodajemy nowego użytkownika
        if self.user:
            self.user.name = name
            update_user(self.user)  # Aktualizacja albumu
        else:
            new_user = User(name=name)
            save_user(new_user)  # Zapis nowego użytkonika

        # Odświeżenie widoku drzewa, jeśli przekazano funkcję
        if self.refresh_treeview:
            self.refresh_treeview()

        # Zamykanie okna
        self.window.destroy()

def open_single_user_window(parent, refresh_treeview):
    UserForm(parent=parent, refresh_treeview=refresh_treeview)

def open_update_user_window(parent, user, refresh_treeview):
    UserForm(parent=parent, user=user, refresh_treeview=refresh_treeview)

