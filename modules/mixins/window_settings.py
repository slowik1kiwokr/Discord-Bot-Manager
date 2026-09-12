import customtkinter as ctk
from tkinter import messagebox

import modules.config as config
from modules.languages import LANGUAGES


class WindowSettingsMixin:
    """A Settings ablakhoz tartozó metódusok."""

    def open_settings_window_v2(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("settings"))
        win.geometry("560x620")
        win.grab_set()

        tabs = ctk.CTkTabview(win)
        tabs.pack(fill="both", expand=True, padx=12, pady=12)
        panel_tab = tabs.add(self.tr("panel_settings"))
        bot_tab = tabs.add(self.tr("bot_settings"))

        ctk.CTkLabel(panel_tab, text=self.tr("panel_settings"), font=("Arial", 17, "bold")).pack(pady=(12, 8))
        ctk.CTkLabel(panel_tab, text=f"{self.tr('panel_id')}: {PANEL_ID}").pack(anchor="w", padx=20, pady=5)
        ctk.CTkLabel(panel_tab, text="Panel password (empty = disabled)").pack(anchor="w", padx=20, pady=(10, 2))
        password_entry = ctk.CTkEntry(panel_tab, show="*", width=280, placeholder_text="Password")
        if self.panel_password:
            password_entry.insert(0, self.panel_password)
        password_entry.pack(anchor="w", padx=20)
        ctk.CTkLabel(panel_tab, text=self.tr("language")).pack(anchor="w", padx=20, pady=(12, 2))
        language_var = ctk.StringVar(value=self.current_language)
        ctk.CTkComboBox(panel_tab, values=["English", "Magyar"], variable=language_var, width=280, command=self.apply_language).pack(anchor="w", padx=20)
        tray_switch = ctk.CTkSwitch(panel_tab, text=self.tr("minimize_tray"))
        tray_switch.pack(anchor="w", padx=20, pady=12)
        if self.minimize_to_tray_enabled:
            tray_switch.select()
        rpc_switch = ctk.CTkSwitch(panel_tab, text=self.tr("rpc"))
        rpc_switch.pack(anchor="w", padx=20, pady=5)
        if self.rpc_enabled:
            rpc_switch.select()
        ctk.CTkLabel(panel_tab, text=self.tr("log_level")).pack(anchor="w", padx=20, pady=(12, 2))
        log_var = ctk.StringVar(value=self.log_save_level)
        ctk.CTkComboBox(panel_tab, values=["Mindent mentse", "Csak hibák", "Csak események", "Sikeres interakciók"], variable=log_var, width=280).pack(anchor="w", padx=20)

        backup_enabled_switch = ctk.CTkSwitch(panel_tab, text=self.tr("backup_auto"))
        backup_enabled_switch.pack(anchor="w", padx=20, pady=(14, 4))
        if self.backup_enabled:
            backup_enabled_switch.select()
        backup_start_switch = ctk.CTkSwitch(panel_tab, text=self.tr("backup_start"))
        backup_start_switch.pack(anchor="w", padx=20, pady=4)
        if self.backup_on_start:
            backup_start_switch.select()
        ctk.CTkLabel(panel_tab, text=self.tr("backup_interval")).pack(anchor="w", padx=20, pady=(8, 2))
        backup_interval_entry = ctk.CTkEntry(panel_tab, width=100)
        backup_interval_entry.insert(0, str(self.backup_interval_hours))
        backup_interval_entry.pack(anchor="w", padx=20)
        ctk.CTkLabel(panel_tab, text=f"{self.tr('panel_id')}: {config.PANEL_ID}").pack(anchor="w", padx=20, pady=5)

        bot = self.bots[self.active_bot_key]
        ctk.CTkLabel(bot_tab, text=f"{self.tr('bot_settings')}: {self.active_bot_key}", font=("Arial", 17, "bold")).pack(pady=(12, 8))
        ctk.CTkLabel(bot_tab, text=self.tr("max_ram")).pack(anchor="w", padx=20, pady=(8, 2))
        ram_entry = ctk.CTkEntry(bot_tab, width=180)
        ram_entry.insert(0, str(self.max_ram_mb))
        ram_entry.pack(anchor="w", padx=20)
        test_switch = ctk.CTkSwitch(bot_tab, text=self.tr("test_mode"))
        test_switch.pack(anchor="w", padx=20, pady=12)
        if bot.get("test_mode", False):
            test_switch.select()
        ctk.CTkLabel(bot_tab, text=self.tr("testers")).pack(anchor="w", padx=20, pady=(8, 2))
        testers_entry = ctk.CTkEntry(bot_tab, width=420, placeholder_text="123456789012345678, 987654321098765432")
        testers_entry.insert(0, ", ".join(str(value) for value in bot.get("allowed_discord_ids", [])))
        testers_entry.pack(anchor="w", padx=20)
        ctk.CTkLabel(bot_tab, text=self.tr("testers_help"), text_color="#aaaaaa").pack(anchor="w", padx=20, pady=5)
        crash_switch = ctk.CTkSwitch(bot_tab, text=self.tr("crash_restart"))
        crash_switch.pack(anchor="w", padx=20, pady=(12, 4))
        if bot.get("auto_restart_on_crash", False):
            crash_switch.select()
        ctk.CTkLabel(bot_tab, text=self.tr("crash_delay")).pack(anchor="w", padx=20, pady=(6, 2))
        crash_delay_entry = ctk.CTkEntry(bot_tab, width=100)
        crash_delay_entry.insert(0, str(bot.get("crash_restart_delay", 10)))
        crash_delay_entry.pack(anchor="w", padx=20)

        def save_settings():
            self.current_language = language_var.get()
            self.panel_password = password_entry.get().strip()
            self.minimize_to_tray_enabled = bool(tray_switch.get())
            self.rpc_enabled = bool(rpc_switch.get())
            self.log_save_level = log_var.get()
            self.backup_enabled = bool(backup_enabled_switch.get())
            self.backup_on_start = bool(backup_start_switch.get())
            try:
                self.backup_interval_hours = max(0, int(backup_interval_entry.get()))
            except ValueError:
                messagebox.showwarning("Hiba", "A backup gyakorisága egész szám legyen.", parent=win)
                return
            bot["test_mode"] = bool(test_switch.get())
            bot["auto_restart_on_crash"] = bool(crash_switch.get())
            try:
                bot["crash_restart_delay"] = max(1, int(crash_delay_entry.get()))
            except ValueError:
                messagebox.showwarning("Hiba", "A crash várakozási idő egész szám legyen.", parent=win)
                return
            bot["allowed_discord_ids"] = [value.strip() for value in testers_entry.get().split(",") if value.strip().isdigit()]
            try:
                self.max_ram_mb = max(50, int(ram_entry.get()))
            except ValueError:
                messagebox.showwarning("Hiba", "A RAM értéke egész szám legyen.", parent=win)
                return
            self.save_config()
            self.switch_bot(self.active_bot_key)
            self.update_ui_texts()
            win.destroy()

        ctk.CTkButton(win, text=self.tr("save"), command=save_settings, fg_color="#27ae60").pack(pady=(0, 12))

    def open_settings_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("settings"))
        win.geometry("480x720")
        win.grab_set()

        ctk.CTkLabel(win, text=self.tr("panel_settings"), font=("Arial", 16, "bold")).pack(pady=15)
        
        chk_tray = ctk.CTkSwitch(win, text=self.tr("minimize_tray"))
        chk_tray.pack(pady=5)
        if self.minimize_to_tray_enabled:
            chk_tray.select()

        ctk.CTkLabel(win, text=self.tr("password_label"), font=("Arial", 11, "bold")).pack(pady=(10, 2))
        pwd_entry = ctk.CTkEntry(win, show="*", width=260, placeholder_text=self.tr("new_password"))
        pwd_entry.pack(pady=2)
        if self.panel_password:
            pwd_entry.insert(0, self.panel_password)

        ctk.CTkLabel(win, text=self.tr("log_level"), font=("Arial", 12, "bold")).pack(pady=(10, 2))
        log_lvl_var = ctk.StringVar(value=self.log_save_level)
        ctk.CTkComboBox(win, values=["Mindent mentse", "Csak hibák", "Csak események", "Sikeres interakciók"], variable=log_lvl_var, width=260).pack(pady=2)

        ctk.CTkLabel(win, text=self.tr("max_ram"), font=("Arial", 12, "bold")).pack(pady=(10, 2))
        ram_spin = ctk.CTkSpinbox(win, from_=50, to=2048, increment=50, width=150) if hasattr(ctk, "CTkSpinbox") else ctk.CTkEntry(win, width=150)
        if hasattr(ram_spin, "set"):
            ram_spin.set(self.max_ram_mb)
        else:
            ram_spin.insert(0, str(self.max_ram_mb))
        ram_spin.pack(pady=2)

        chk_task_kill = ctk.CTkSwitch(win, text=self.tr("task_kill"))
        chk_task_kill.pack(pady=5)
        if self.task_kill_enabled:
            chk_task_kill.select()

        chk_rpc = ctk.CTkSwitch(win, text=self.tr("rpc"))
        chk_rpc.pack(pady=5)
        if self.rpc_enabled:
            chk_rpc.select()

        ctk.CTkLabel(win, text=self.tr("language"), font=("Arial", 12, "bold")).pack(pady=(10, 2))
        lang_var = ctk.StringVar(value=self.current_language)
        ctk.CTkComboBox(win, values=["English", "Magyar"], variable=lang_var, width=260, command=self.apply_language).pack(pady=2)

        ctk.CTkLabel(win, text=self.tr("error_sound"), font=("Arial", 12, "bold")).pack(pady=(10, 2))
        sound_var = ctk.StringVar(value=self.selected_error_sound)
        ctk.CTkComboBox(win, values=["Alap (Beep)", "Dupla Pittyogás", "Mély Hiba (Buzz)"], variable=sound_var, width=260).pack(pady=2)

        ctk.CTkLabel(win, text=self.tr("theme"), font=("Arial", 12, "bold")).pack(pady=(10, 2))
        theme_var = ctk.StringVar(value=self.current_theme)
        ctk.CTkComboBox(win, values=["Discord Sötét (Alap)", "Discord Világos", "Discord Blurple (Lila-Kék)", "Discord Zöld (Hacker)"], variable=theme_var, width=260).pack(pady=2)

        def save_and_close():
            self.minimize_to_tray_enabled = bool(chk_tray.get())
            self.panel_password = pwd_entry.get().strip()
            self.current_language = lang_var.get()
            self.selected_error_sound = sound_var.get()
            self.log_save_level = log_lvl_var.get()
            self.task_kill_enabled = bool(chk_task_kill.get())
            self.rpc_enabled = bool(chk_rpc.get())
            
            try:
                if hasattr(ram_spin, "get"):
                    self.max_ram_mb = int(ram_spin.get())
                else:
                    self.max_ram_mb = int(ram_spin.get())
            except Exception:
                pass

            selected_t = theme_var.get()
            if selected_t != self.current_theme:
                self.apply_theme_setting(selected_t)

            self.save_config()
            self.update_ui_texts()
            win.destroy()

        ctk.CTkButton(win, text="Mentés & Bezárás", command=save_and_close, fg_color="#27ae60").pack(pady=15)
