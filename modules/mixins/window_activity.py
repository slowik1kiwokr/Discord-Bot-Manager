import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog

import modules.config as config


class WindowActivityMixin:
    def open_activity_editor(self):
        bot = self.bots[self.active_bot_key]
        win = ctk.CTkToplevel(self)
        win.title(self.tr("activity_loop"))
        win.geometry("720x520")
        win.grab_set()
        ctk.CTkLabel(win, text=self.tr("activity_loop"), font=("Arial", 16, "bold")).pack(pady=10)
        enabled = ctk.CTkSwitch(win, text=self.tr("activity_enabled"))
        enabled.pack(anchor="w", padx=18, pady=4)
        if bot.get("activity_enabled", True):
            enabled.select()
        interval_frame = ctk.CTkFrame(win, fg_color="transparent")
        interval_frame.pack(anchor="w", padx=18, pady=4)
        ctk.CTkLabel(interval_frame, text=self.tr("activity_interval")).pack(side="left", padx=(0, 8))
        interval_entry = ctk.CTkEntry(interval_frame, width=80)
        interval_entry.insert(0, str(bot.get("activity_interval_minutes", 5)))
        interval_entry.pack(side="left")
        rows_frame = ctk.CTkScrollableFrame(win, height=300)
        rows_frame.pack(fill="both", expand=True, padx=12, pady=8)
        rows = []
        saved_loop = bot.get("activity_loop", []) or []
        if not saved_loop and bot.get("activity_text", ""):
            saved_loop = [{"type": bot.get("activity_type", "Playing"), "text": bot.get("activity_text", "")}]
        if not saved_loop:
            saved_loop = [{"type": "Playing", "text": ""}]

        def add_row(activity_type="Playing", activity_text=""):
            row = ctk.CTkFrame(rows_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)
            type_var = ctk.StringVar(value=activity_type)
            # ⚠️ Ezek az értékek a bot számára kellenek — NEM fordítjuk!
            ctk.CTkComboBox(row, values=["Playing", "Listening", "Watching", "Streaming"], variable=type_var, width=130).pack(side="left", padx=4)
            text_entry = ctk.CTkEntry(row, placeholder_text=self.tr("activity_text"))
            text_entry.insert(0, activity_text)
            text_entry.pack(side="left", fill="x", expand=True, padx=4)
            row_data = {"row": row, "type": type_var, "text": text_entry}
            rows.append(row_data)
            ctk.CTkButton(row, text=self.tr("remove"), width=32, command=lambda: remove_row(row_data)).pack(side="right", padx=4)

        def remove_row(row_data):
            if len(rows) <= 1:
                return
            rows.remove(row_data)
            row_data["row"].destroy()

        for item in saved_loop:
            add_row(item.get("type", "Playing"), item.get("text", ""))
        ctk.CTkButton(win, text=self.tr("add_activity"), command=add_row).pack(anchor="w", padx=18, pady=4)

        def save():
            try:
                interval = max(1, int(interval_entry.get()))
            except ValueError:
                messagebox.showwarning(self.tr("common_error_title"),
                                       self.tr("activity_interval_invalid"), parent=win)
                return
            loop = [{"type": item["type"].get(), "text": item["text"].get().strip()} for item in rows if item["text"].get().strip()]
            bot["activity_enabled"] = bool(enabled.get())
            bot["activity_interval_minutes"] = interval
            bot["activity_loop"] = loop
            if loop:
                bot["activity_type"], bot["activity_text"] = loop[0]["type"], loop[0]["text"]
            self.save_config()
            win.destroy()
        ctk.CTkButton(win, text=self.tr("common_save_btn"), fg_color="#27ae60", command=save).pack(pady=10)