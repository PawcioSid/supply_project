import tkinter as tk

from models import Types
from types_db import save_type, update_type


class TypesForm:
    def __init__(self, parent, refresh_treeview, types=None, name=None):
        self.types = types
        self.name = name
        self.name_types_entry = None
        self.refresh_treeview = refresh_treeview

        # Tworzenie okna
        self.window = tk.Toplevel(parent)
        self.window.geometry('400x200')
        self.window.grab_set()
        self.window.transient(parent)

        # Tworzenie formularza

        if types:
            self.window.title("Edytuj materiał obróbki")
        else:
            self.window.title("Dodaj materiał obróbki")
        save_button = tk.Button(self.window, text="Zapisz", command=self.save)
        save_button.grid(row=4, column=0, columnspan=2)

        self.create_form()

    def create_form(self):
        # Etykiety
        tk.Label(self.window, text="Materiał obróbki:").grid(row=0, column=0, sticky='w')

        # Tworzenie pól formularza
        self.name_types_entry = tk.Entry(self.window)
        # Rozmieszczenie elementów w siatce
        self.name_types_entry.grid(row=0, column=1, sticky='w')

    def save(self):
        # Pobieranie danych z formularza
        name = self.name_types_entry.get()

        # Sprawdzamy, czy aktualizujemy materiał obróbki, czy dodajemy nowy materiał obróbki
        if self.types:
            self.types.name = name
            update_type(self.types)  # Aktualizacja albumu
        else:
            new_type = Types(name=name)
            save_type(new_type)  # Zapis nowego materiału obróbki

        # Odświeżenie widoku drzewa, jeśli przekazano funkcję
        if self.refresh_treeview:
            self.refresh_treeview()

        # Zamykanie okna
        self.window.destroy()


def open_single_type_window(parent, refresh_treeview):
    TypesForm(parent=parent, refresh_treeview=refresh_treeview)


def open_update_type_window(parent, user, refresh_treeview):
    TypesForm(parent=parent, types=user, refresh_treeview=refresh_treeview)