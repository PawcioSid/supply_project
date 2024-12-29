import tkinter as tk
from tkinter import ttk
from user_db import get_user
from types_db import get_types
from tools_db import save_tool, update_tool
from models import Tool


# Klasa odpowiedzialna za formularz albumu (zarówno dodawanie, jak i edycja)
class ToolForm:
    def __init__(self, parent, refresh_treeview, tool=None):
        self.added_year_entry = None
        self.types_combobox = None
        self.name_tool_entry = None
        self.user_combobox = None
        self.tool = tool
        self.refresh_treeview = refresh_treeview

        # Tworzenie okna
        self.window = tk.Toplevel(parent)
        self.window.geometry('400x200')
        self.window.grab_set()
        self.window.transient(parent)

        # Ustawianie tytułu okna w zależności od akcji
        if tool:
            self.window.title("Edytuj narzędzie")
        else:
            self.window.title("Dodaj nowe narzędzie")

        # Pobieranie użytkowników i typów narzędzia
        self.user_dict, self.types_dict = self.get_user_and_types()

        # Tworzenie formularza
        self.create_form()

    @staticmethod
    def get_user_and_types():
        user_dict = {user.name: user for user in get_user()}
        types_dict = {types.name: types for types in get_types()}
        return user_dict, types_dict

    def create_form(self):
        # Etykiety
        tk.Label(self.window, text="Użytkownik:").grid(row=0, column=0, sticky='w')
        tk.Label(self.window, text="Nazwa narzędzia:").grid(row=1, column=0, sticky='w')
        tk.Label(self.window, text="Rodzaj narzędzia:").grid(row=2, column=0, sticky='w')
        tk.Label(self.window, text="Rok dodania:").grid(row=3, column=0, sticky='w')

        # Tworzenie pól formularza
        self.user_combobox = ttk.Combobox(self.window, values=list(self.user_dict.keys()), state='readonly')
        self.name_tool_entry = tk.Entry(self.window)
        self.types_combobox = ttk.Combobox(self.window, values=list(self.types_dict.keys()), state='readonly')
        self.added_year_entry = tk.Entry(self.window)

        # Jeśli edytujemy album, wypełniamy formularz
        if self.tool:
            self.user_combobox.set(self.tool.user.name)
            self.name_tool_entry.insert(0, self.tool.name_tool)
            self.types_combobox.set(self.tool.types.name)
            self.added_year_entry.insert(0, str(self.tool.added_year))

        # Rozmieszczenie elementów w siatce
        self.user_combobox.grid(row=0, column=1, sticky='w')
        self.name_tool_entry.grid(row=1, column=1, sticky='w')
        self.types_combobox.grid(row=2, column=1, sticky='w')
        self.added_year_entry.grid(row=3, column=1, sticky='w')

        # Przycisk "Zapisz" z odpowiednią funkcją w zależności od akcji
        save_button = tk.Button(self.window, text="Zapisz", command=self.save)
        save_button.grid(row=4, column=0, columnspan=2)

    def save(self):
        # Pobieranie danych z formularza
        user = self.user_dict.get(self.user_combobox.get())
        name_tool = self.name_tool_entry.get()
        types = self.types_dict.get(self.types_combobox.get())
        added_year = self.added_year_entry.get()

        # Sprawdzamy, czy aktualizujemy album, czy dodajemy nowy
        if self.tool:
            self.tool.user = user
            self.tool.name_tool = name_tool
            self.tool.types = types
            self.tool.added_year = added_year
            update_tool(self.tool)  # Aktualizacja albumu
        else:
            new_tool = Tool(user=user, name_tool=name_tool, types=types, added_year=added_year)
            save_tool(new_tool)  # Zapis nowego albumu

        # Odświeżenie widoku drzewa, jeśli przekazano funkcję
        if self.refresh_treeview:
            self.refresh_treeview()

        # Zamykanie okna
        self.window.destroy()


# Funkcje do otwierania okna dodawania i edycji albumów
def open_add_tool_window(parent, refresh_treeview):
    ToolForm(parent=parent, refresh_treeview=refresh_treeview)


def open_update_tool_window(parent, tool, refresh_treeview):
    ToolForm(parent=parent, tool=tool, refresh_treeview=refresh_treeview)
