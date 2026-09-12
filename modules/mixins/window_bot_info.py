import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog

import modules.config as config
from modules.languages import LANGUAGES


class WindowBotInfoMixin:
    def open_bot_info_editor(self):
        metadata = self.read_bot_metadata()
        win = ctk.CTkToplevel(self)
        win.title(self.tr("bot_data"))
        win.geometry("520x360")
        win.grab_set()
        fields = []
        for label, key, show in ((self.tr("bot_name"), "name", None), (self.tr("bot_version"), "version", None), ("Bot Token", "token", "*")):
            ctk.CTkLabel(win, text=label).pack(anchor="w", padx=24, pady=(14, 3))
            entry = ctk.CTkEntry(win, show=show, width=430)
            entry.insert(0, metadata[key])
            entry.pack(anchor="w", padx=24)
            fields.append(entry)
        ctk.CTkLabel(win, text=self.tr("bot_token_warning"), text_color="#e67e22").pack(anchor="w", padx=24, pady=12)
        def save():
            self.save_bot_metadata(fields[0].get(), fields[1].get(), fields[2].get())
            win.destroy()
        ctk.CTkButton(win, text="Mentés", fg_color="#27ae60", command=save).pack(pady=12)