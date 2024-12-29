import tkinter as tk
from tkinter import ttk

from tools_db import get_tools, delete_tool
from tool_form import open_add_tool_window
from tool_form import open_update_tool_window
from user_db import get_user, delete_user, save_user
from types_db import get_types, delete_type, save_type
from user_form import open_single_user_window, open_update_user_window
from types_form import open_single_type_window, open_update_type_window
from graph import ToolDataVisualizer
from config import DATABASE_URL


def refresh_three_view_tool(tree, tools_dict):
    tree.delete(*tree.get_children())
    tools_dict.clear()

    tools = get_tools()

    for tool in tools:
        item_id = tree.insert("", "end", values=(tool.user.name, tool.name_tool, tool.types.name, tool.added_year))
        tools_dict[item_id] = tool


def delete_single_tool(tree, tools_dict):
    selected_item = tree.selection()[0]
    tool = tools_dict[selected_item]

    delete_tool(tool)

    refresh_three_view_tool(tree, tools_dict)


def update_single_tool(root, tree, tools_dict):
    selected_item = tree.selection()[0]
    tool = tools_dict[selected_item]

    open_update_tool_window(root, tool, lambda: refresh_three_view_tool(tree, tools_dict))


def refresh_three_view_user(tree, user_dict):
    tree.delete(*tree.get_children())
    user_dict.clear()

    users = get_user()

    for user in users:
        item_id = tree.insert("", "end", values=user.name)
        user_dict[item_id] = user

def add_single_user( tree, user_dict):
    selected_item = tree.selection()[0]
    user = user_dict[selected_item]

    save_user(user)

    refresh_three_view_user(tree, user_dict)
    open_single_user_window(tree, refresh_three_view_user(tree, user_dict))


def delete_single_user(tree, user_dict):
    selected_item = tree.selection()[0]
    user = user_dict[selected_item]

    delete_user(user)

    refresh_three_view_user(tree, user_dict)

def update_single_user(root,tree, user_dict):
    selected_item = tree.selection()[0]
    user = user_dict[selected_item]

    open_update_user_window(root, user, lambda: refresh_three_view_user(tree, user_dict))

def refresh_three_view_type(tree, types_dict):
    tree.delete(*tree.get_children())
    types_dict.clear()

    types = get_types()

    for type in types:
        item_id = tree.insert("", "end", values=type.name)
        types_dict[item_id] = type

def add_single_type( tree, types_dict):
    selected_item = tree.selection()[0]
    type = types_dict[selected_item]

    save_type(type)

    refresh_three_view_type(tree, types_dict)
    open_single_type_window(tree, refresh_three_view_type(tree, types_dict))


def delete_single_type(tree, types_dict):
    selected_item = tree.selection()[0]
    type = types_dict[selected_item]

    delete_type(type)

    refresh_three_view_type(tree, types_dict)

def update_single_type(root, tree, types_dict):
    selected_item = tree.selection()[0]
    type = types_dict[selected_item]

    open_update_type_window(root, type, lambda: refresh_three_view_type(tree, types_dict))


def run_app():
    # Okno
    root = tk.Tk()
    root.title('Magazyn narzędzi')
    root.geometry('800x600')

    # Tworzenie głównej ramki
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Konfiguracja rozciągania
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)

    label = tk.Label(main_frame, text='Narzędzia w użyciu', font="bold")
    label.grid(row=0, column=0, columnspan=2, pady=10)

    # Pasek menu
    menu_bar = tk.Menu(root)

    file_menu_tool = tk.Menu(menu_bar, tearoff=0)
    file_menu_tool.add_command(label="Dodaj narzędzie", command=lambda: open_add_tool_window(root, lambda: refresh_three_view_tool(tree_tool, tools_dict)))
    file_menu_tool.add_command(label="Edytuj narzędzie", command=lambda: update_single_tool(root, tree_tool, tools_dict))
    file_menu_tool.add_command(label="Usuń narzędzie", command=lambda: delete_single_tool(tree_tool, tools_dict))

    menu_bar.add_cascade(label="Narzędzia", menu=file_menu_tool)

    file_menu_user = tk.Menu(menu_bar, tearoff=0)
    file_menu_user.add_command(label="Dodaj użytkownika", command=lambda: open_single_user_window(root, lambda: refresh_three_view_user(tree_user, user_dict)))
    file_menu_user.add_command(label="Edytuj użytkownika", command=lambda: update_single_user(root, tree_user, user_dict))
    file_menu_user.add_command(label="Usuń użytkownika", command=lambda: delete_single_user(tree_user, user_dict))

    menu_bar.add_cascade(label="Użytkownicy", menu=file_menu_user)
    root.config(menu=menu_bar)

    file_menu_types = tk.Menu(menu_bar, tearoff=0)
    file_menu_types.add_command(label="Dodaj materiał obróbki", command=lambda: open_single_type_window(root,  lambda: refresh_three_view_type( tree_types, types_dict)))
    file_menu_types.add_command(label="Edytuj materiał obróbki",
                                command=lambda: update_single_type(root, tree_types, types_dict))
    file_menu_types.add_command(label="Usuń materiał obróbki", command=lambda: delete_single_type(tree_types, types_dict))

    menu_bar.add_cascade(label="Materiał obróbki", menu=file_menu_types)
    root.config(menu=menu_bar)

    file_menu_graph = tk.Menu(menu_bar, tearoff=0)
    file_menu_graph.add_command(label="Rok dodania", command=lambda: ToolDataVisualizer(DATABASE_URL).run())
    menu_bar.add_cascade(label="Statystyka", menu=file_menu_graph)
    root.config(menu=menu_bar)

    # Drzewo widoku narzędzi z paskiem przewijania
    tree_frame_tool = ttk.Frame(main_frame)
    tree_frame_tool.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(5, 5), pady=5)

    tree_scroll_tool = ttk.Scrollbar(tree_frame_tool, orient="vertical")
    tree_scroll_tool.pack(side="right", fill="y")

    tree_tool = ttk.Treeview(tree_frame_tool, columns=("User", "Name tool", "Type", "Added Year"),
                             show="headings", selectmode="browse", yscrollcommand=tree_scroll_tool.set)
    tree_scroll_tool.config(command=tree_tool.yview)

    tree_tool.heading("User", text="Użytkownik")
    tree_tool.heading("Name tool", text="Nazwa narzędzia")
    tree_tool.heading("Type", text="Materiał obróbki")
    tree_tool.heading("Added Year", text="Rok dodania")

    tools_dict = {}
    refresh_three_view_tool(tree_tool, tools_dict)
    tree_tool.pack(fill="both", expand=True)

    # Drzewo widoku użytkowników z paskiem przewijania
    tree_frame_user = ttk.Frame(main_frame)
    tree_frame_user.grid(row=2, column=1, sticky="nsew", padx=(5, 5), pady=5)

    tree_scroll_user = ttk.Scrollbar(tree_frame_user, orient="vertical")
    tree_scroll_user.pack(side="right", fill="y")

    tree_user = ttk.Treeview(tree_frame_user, columns="User", show="headings", selectmode="browse", yscrollcommand=tree_scroll_user.set)
    tree_scroll_user.config(command=tree_user.yview)

    tree_user.heading("User", text="Użytkownik")

    user_dict = {}
    refresh_three_view_user(tree_user, user_dict)
    tree_user.pack(fill="both", expand=True)

    # Drzewo widoku materiałów obróbki z paskiem przewijania
    tree_frame_types = ttk.Frame(main_frame)
    tree_frame_types.grid(row=2, column=0, sticky="nsew", padx=(5, 5), pady=5)

    tree_scroll_types = ttk.Scrollbar(tree_frame_types, orient="vertical")
    tree_scroll_types.pack(side="right", fill="y")

    tree_types = ttk.Treeview(tree_frame_types, columns="Types", show="headings", selectmode="browse", yscrollcommand=tree_scroll_types.set)
    tree_scroll_types.config(command=tree_types.yview)

    tree_types.heading("Types", text="Materiał obróbki")

    types_dict = {}
    refresh_three_view_type(tree_types, types_dict)
    tree_types.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == '__main__':
    run_app()


