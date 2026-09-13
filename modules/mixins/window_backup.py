import os
import datetime
import zipfile
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

import modules.config as config
from modules.config import SCRIPT_DIR, BACKUP_DIR
from modules.languages import LANGUAGES


class WindowBackupMixin:
    """Backup kezelő mixin."""

    def create_backup(self, show_message=True):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = os.path.join(BACKUP_DIR, "bot_backup_%s.zip" % stamp)
        try:
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as archive:
                for panel_file in (config.BOTS_FILE, config.SETTINGS_FILE):
                    if os.path.isfile(panel_file):
                        archive.write(panel_file, os.path.basename(panel_file))
                for key, bot in self.bots.items():
                    script_path = bot.get("path", "")
                    bot_dir = os.path.dirname(script_path) if script_path else ""
                    if not bot_dir or not os.path.isdir(bot_dir):
                        continue
                    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)
                    for root, _, files in os.walk(bot_dir):
                        for filename in files:
                            full_path = os.path.join(root, filename)
                            relative = os.path.relpath(full_path, bot_dir).replace(os.sep, "/")
                            if (relative in ("bot_stats.json", "bot_config.json")
                                    or relative.startswith("data/")
                                    or filename.lower().endswith((".json", ".db", ".sqlite", ".sqlite3"))):
                                archive.write(full_path, "bots/%s/%s" % (safe_name, relative))
            self.backup_last_run = datetime.datetime.now().isoformat(timespec="seconds")
            self.save_config()
            if show_message:
                messagebox.showinfo("Biztonsági mentés", "A mentés elkészült:\n%s" % backup_path)
            return backup_path
        except OSError as error:
            if show_message:
                messagebox.showerror("Mentési hiba", str(error))
            return ""

    def check_scheduled_backup(self):
        should_run = False
        if self.backup_enabled:
            if self.backup_on_start and not getattr(self, "startup_backup_done", False):
                self.startup_backup_done = True
                should_run = True
            elif self.backup_last_run:
                try:
                    last_run = datetime.datetime.fromisoformat(self.backup_last_run)
                    should_run = (datetime.datetime.now() - last_run).total_seconds() >= self.backup_interval_hours * 3600
                except ValueError:
                    should_run = True
            elif self.backup_interval_hours > 0:
                self.backup_last_run = datetime.datetime.now().isoformat(timespec="seconds")
                self.save_config()
        if should_run:
            self.create_backup(show_message=False)
        self.after(60000, self.check_scheduled_backup)

    def open_backup_manager(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("backup_title"))
        win.geometry("720x500")
        win.grab_set()

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 720) // 2
        y = (win.winfo_screenheight() - 500) // 2
        win.geometry(f"720x500+{x}+{y}")

        ctk.CTkLabel(win, text=self.tr("backup_title"),
                     font=("Arial", 16, "bold")).pack(pady=12)

        listbox = tk.Listbox(win, bg="#202020", fg="white",
                             selectbackground="#2980b9", height=15)
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
                messagebox.showwarning("Válassz mentést",
                                       "Jelölj ki egy ZIP mentést.", parent=win)
                return
            archive_path = os.path.join(BACKUP_DIR, listbox.get(selected[0]))
            if not messagebox.askyesno("Visszaállítás",
                                       "A mentés felülírhat meglévő JSON, DB és data fájlokat. Folytatod?",
                                       parent=win):
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
                messagebox.showinfo("Visszaállítás",
                                    "A mentés visszaállt. A teljes alkalmazás újraindítása javasolt.",
                                    parent=win)
            except (OSError, zipfile.BadZipFile, ValueError) as error:
                messagebox.showerror("Visszaállítási hiba", str(error), parent=win)

        buttons = ctk.CTkFrame(win, fg_color="transparent")
        buttons.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(buttons, text=self.tr("backup_new"),
                      command=lambda: (self.create_backup(), refresh())).pack(side="left", padx=4)
        ctk.CTkButton(buttons, text=self.tr("backup_restore"),
                      fg_color="#d35400", command=restore).pack(side="left", padx=4)
        ctk.CTkButton(buttons, text=self.tr("refresh"),
                      command=refresh).pack(side="right", padx=4)

        refresh()
