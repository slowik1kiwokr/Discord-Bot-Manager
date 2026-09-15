import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog

import modules.config as config


class WindowBotInfoMixin:
    def open_bot_info_editor(self):
        metadata = self.read_bot_metadata()
        win = ctk.CTkToplevel(self)
        win.title(self.tr("bot_data"))
        win.geometry("540x480")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 540) // 2
        y = (win.winfo_screenheight() - 480) // 2
        win.geometry(f"540x480+{x}+{y}")

        # Fejléc
        header = ctk.CTkFrame(win, fg_color="#8e44ad", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="🤖  " + self.tr("bot_data"),
            font=("Arial", 16, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=16)

        # Mezők
        fields = []
        field_defs = (
            (self.tr("bot_name"), "name", None, "Main Bot"),
            (self.tr("bot_version"), "version", None, "1.0.0"),
            (self.tr("bot_prefix"), "prefix", None, "/"),
            ("Bot Token", "token", "*", self.tr("bot_info_token_placeholder")),
        )

        for label, key, show, placeholder in field_defs:
            ctk.CTkLabel(
                win, text=label, font=("Arial", 11, "bold"), anchor="w"
            ).pack(fill="x", padx=24, pady=(14, 3))
            entry = ctk.CTkEntry(win, show=show, width=460, height=38,
                                   placeholder_text=placeholder)
            entry.insert(0, metadata.get(key, ""))
            entry.pack(anchor="w", padx=24)
            fields.append(entry)

        ctk.CTkLabel(
            win,
            text=self.tr("bot_info_hint"),
            font=("Arial", 10), text_color="#e67e22",
            justify="left",
        ).pack(anchor="w", padx=24, pady=(14, 6))

        def save():
            self.save_bot_metadata(
                fields[0].get(),   # name
                fields[1].get(),   # version
                fields[3].get(),   # token
                fields[2].get(),   # prefix
            )
            win.destroy()

        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(pady=14)

        ctk.CTkButton(btns, text="💾  " + self.tr("save"),
                       fg_color="#27ae60", hover_color="#2ecc71",
                       width=180, height=42, font=("Arial", 13, "bold"),
                       command=save).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="❌  " + self.tr("close"),
                       fg_color="#555555", hover_color="#666666",
                       width=120, height=42,
                       command=win.destroy).pack(side="left", padx=6)