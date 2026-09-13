import os
import json
import uuid
from tkinter import messagebox

import customtkinter as ctk

import modules.config as config
from modules.config import BROADCAST_REQUESTS_FILE
from modules.languages import LANGUAGES



class WindowBroadcastMixin:
    def open_broadcast_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("broadcast_title"))
        win.geometry("620x520")
        win.grab_set()
        ctk.CTkLabel(win, text=self.tr("broadcast_help"), font=("Arial", 16, "bold")).pack(pady=12)
        ctk.CTkLabel(win, text=self.tr("message")).pack(anchor="w", padx=20)
        message_box = ctk.CTkTextbox(win, height=130)
        message_box.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(win, text=self.tr("channel_mapping"), wraplength=570).pack(anchor="w", padx=20, pady=(8, 3))
        channels_box = ctk.CTkTextbox(win, height=120, font=("Consolas", 10))
        channels_box.pack(fill="x", padx=20, pady=6)
        def send():
            message = message_box.get("1.0", "end").strip()
            if not message:
                messagebox.showwarning("Broadcast", "Az üzenet nem lehet üres.", parent=win)
                return
            channels = {}
            for line in channels_box.get("1.0", "end").splitlines():
                if "=" in line:
                    guild_id, channel_id = [part.strip() for part in line.split("=", 1)]
                    if guild_id.isdigit() and channel_id.isdigit():
                        channels[guild_id] = channel_id
            try:
                pending = []
                if os.path.exists(BROADCAST_REQUESTS_FILE):
                    with open(BROADCAST_REQUESTS_FILE, "r", encoding="utf-8") as request_file:
                        pending = json.load(request_file)
                pending.append({"id": uuid.uuid4().hex, "bot": self.active_bot_key, "message": message, "channels": channels})
                temporary_path = BROADCAST_REQUESTS_FILE + ".tmp"
                with open(temporary_path, "w", encoding="utf-8") as request_file:
                    json.dump(pending, request_file, ensure_ascii=False)
                os.replace(temporary_path, BROADCAST_REQUESTS_FILE)
                self.append_log("EVENT", "Broadcast várólistára téve a(z) %s bothoz." % self.active_bot_key)
                messagebox.showinfo("Broadcast", "Az üzenet elküldési várólistára került.", parent=win)
                win.destroy()
            except (OSError, json.JSONDecodeError) as error:
                messagebox.showerror("Broadcast hiba", str(error), parent=win)
        ctk.CTkButton(win, text=self.tr("send_broadcast"), fg_color="#c0392b", command=send).pack(pady=12)