import os
import datetime
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

import modules.config as config
from modules.config import SCRIPT_DIR, BACKUP_DIR
from modules.languages import LANGUAGES

class WindowBackupMixin:
    def open_backup_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("backup_title"))
        win.geometry("720x500")
        win.grab_set()
        ctk.CTkLabel(win, text=self.tr("backup_title"), font=("Arial", 16, "bold")).pack(pady=12)
        listbox = tk.Listbox(win, bg="#202020", fg="white", selectbackground="#2980b9", height=15)
        listbox.pack(fill="both", expand=True, padx=15, pady=8)
        os.makedirs(BACKUP_DIR, exist_ok=True)

        def refresh():
            listbox.delete(0, "end")
            for filename in sorted(os.listdir(BACKUP_DIR), reverse=True):
                if filename.lower().endswith(".zip"):
                    listbox.insert("end", filename)

        def restore():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("Válassz mentést", "Jelölj ki egy ZIP mentést.", parent=win)
                return
            archive_path = os.path.join(BACKUP_DIR, listbox.get(selected[0]))
            if not messagebox.askyesno("Visszaállítás", "A mentés felülírhat meglévő JSON, DB és data fájlokat. Folytatod?", parent=win):
                return
            try:
                with zipfile.ZipFile(archive_path, "r") as archive:
                    for member in archive.infolist():
                        target = os.path.abspath(os.path.join(SCRIPT_DIR, member.filename))
                        if not target.startswith(os.path.abspath(SCRIPT_DIR) + os.sep):
                            raise ValueError("Érvénytelen mentésútvonal")
                        if member.filename in ("bots.json", "settings.json"):
                            archive.extract(member, SCRIPT_DIR)
                        elif member.filename.startswith("bots/"):
                            archive.extract(member, SCRIPT_DIR)
                messagebox.showinfo("Visszaállítás", "A mentés visszaállt. A teljes alkalmazás újraindítása javasolt.", parent=win)
            except (OSError, zipfile.BadZipFile, ValueError) as error:
                messagebox.showerror("Visszaállítási hiba", str(error), parent=win)

        buttons = ctk.CTkFrame(win, fg_color="transparent")
        buttons.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(buttons, text=self.tr("backup_new"), command=lambda: (self.create_backup(), refresh())).pack(side="left", padx=4)
        ctk.CTkButton(buttons, text=self.tr("backup_restore"), fg_color="#d35400", command=restore).pack(side="left", padx=4)
        ctk.CTkButton(buttons, text=self.tr("refresh"), command=refresh).pack(side="right", padx=4)
        refresh()