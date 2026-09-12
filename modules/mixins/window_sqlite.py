import os
import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import customtkinter as ctk

import modules.config as config
from modules.languages import LANGUAGES



class WindowsqliteMixin:
    def open_sqlite_viewer(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("sqlite_title"))
        win.geometry("1000x650")
        win.grab_set()
        top = ctk.CTkFrame(win, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=10)
        path_entry = ctk.CTkEntry(top, placeholder_text=self.tr("sqlite_file"))
        path_entry.pack(side="left", fill="x", expand=True, padx=4)
        table_var = ctk.StringVar()
        table_box = ctk.CTkComboBox(top, variable=table_var, values=[] , width=180)
        table_box.pack(side="left", padx=4)
        tree_frame = ctk.CTkFrame(win)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=4)
        tree = ttk.Treeview(tree_frame, show="headings")
        tree.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview).pack(side="right", fill="y")
        sql_entry = ctk.CTkEntry(win, placeholder_text=self.tr("quick_sql") + ": SELECT * FROM users LIMIT 100")
        sql_entry.pack(fill="x", padx=10, pady=6)
        state = {"connection": None}

        def render_query(query):
            try:
                cursor = state["connection"].execute(query)
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description or []]
                tree.delete(*tree.get_children())
                tree["columns"] = columns
                for column in columns:
                    tree.heading(column, text=column)
                    tree.column(column, width=140, anchor="w")
                for row in rows:
                    tree.insert("", "end", values=tuple(row))
            except (sqlite3.Error, AttributeError) as error:
                messagebox.showerror("SQLite hiba", str(error), parent=win)

        def load_database(path=None):
            selected_path = path or filedialog.askopenfilename(parent=win, filetypes=[("SQLite adatbázis", "*.db *.sqlite *.sqlite3"), ("Minden fájl", "*.*")])
            if not selected_path:
                return
            try:
                if state["connection"]:
                    state["connection"].close()
                state["connection"] = sqlite3.connect("file:%s?mode=ro" % os.path.abspath(selected_path).replace("\\", "/"), uri=True)
                path_entry.delete(0, "end")
                path_entry.insert(0, selected_path)
                tables = [row[0] for row in state["connection"].execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
                table_box.configure(values=tables)
                if tables:
                    table_var.set(tables[0])
                    render_query('SELECT * FROM "%s" LIMIT 200' % tables[0].replace('"', '""'))
            except sqlite3.Error as error:
                messagebox.showerror("SQLite hiba", str(error), parent=win)

        ctk.CTkButton(top, text=self.tr("browse"), width=85, command=load_database).pack(side="left", padx=4)
        ctk.CTkButton(win, text=self.tr("open_table"), command=lambda: render_query('SELECT * FROM "%s" LIMIT 200' % table_var.get().replace('"', '""'))).pack(side="left", padx=10, pady=4)
        ctk.CTkButton(win, text=self.tr("run_sql"), command=lambda: render_query(sql_entry.get().strip())).pack(side="left", padx=4, pady=4)
        win.protocol("WM_DELETE_WINDOW", lambda: (state["connection"] and state["connection"].close(), win.destroy()))
