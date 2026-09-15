import os
import json
import datetime
import time

import customtkinter as ctk

import modules.config as config


# =====================================================================
#  ACHIEVEMENT DEFINÍCIÓK — csak ikon + nyelvi kulcsok
# =====================================================================
ACHIEVEMENTS = {
    "first_start": {
        "icon": "🥇",
        "name_key": "ach_first_start_name",
        "desc_key": "ach_first_start_desc",
    },
    "first_backup": {
        "icon": "💾",
        "name_key": "ach_first_backup_name",
        "desc_key": "ach_first_backup_desc",
    },
    "first_plugin": {
        "icon": "🧩",
        "name_key": "ach_first_plugin_name",
        "desc_key": "ach_first_plugin_desc",
    },
    "first_commander": {
        "icon": "⚡",
        "name_key": "ach_first_commander_name",
        "desc_key": "ach_first_commander_desc",
    },
    "three_bots": {
        "icon": "🤖",
        "name_key": "ach_three_bots_name",
        "desc_key": "ach_three_bots_desc",
    },
    "five_bots": {
        "icon": "🎯",
        "name_key": "ach_five_bots_name",
        "desc_key": "ach_five_bots_desc",
    },
    "ten_bots": {
        "icon": "🚀",
        "name_key": "ach_ten_bots_name",
        "desc_key": "ach_ten_bots_desc",
    },
    "uptime_1h": {
        "icon": "⏱️",
        "name_key": "ach_uptime_1h_name",
        "desc_key": "ach_uptime_1h_desc",
    },
    "uptime_10h": {
        "icon": "⏳",
        "name_key": "ach_uptime_10h_name",
        "desc_key": "ach_uptime_10h_desc",
    },
    "uptime_100h": {
        "icon": "🏆",
        "name_key": "ach_uptime_100h_name",
        "desc_key": "ach_uptime_100h_desc",
    },
    "ten_backups": {
        "icon": "🗄️",
        "name_key": "ach_ten_backups_name",
        "desc_key": "ach_ten_backups_desc",
    },
    "error_free_day": {
        "icon": "✨",
        "name_key": "ach_error_free_day_name",
        "desc_key": "ach_error_free_day_desc",
    },
    "appearance_user": {
        "icon": "🎨",
        "name_key": "ach_appearance_user_name",
        "desc_key": "ach_appearance_user_desc",
    },
    "hotkey_user": {
        "icon": "⌨️",
        "name_key": "ach_hotkey_user_name",
        "desc_key": "ach_hotkey_user_desc",
    },
    "theme_switcher": {
        "icon": "🌗",
        "name_key": "ach_theme_switcher_name",
        "desc_key": "ach_theme_switcher_desc",
    },
}


class AchievementsMixin:
    """Achievement rendszer."""

    # ==================================================================
    #  INICIALIZÁLÁS
    # ==================================================================
    def init_achievements(self):
        self.achievements_file = os.path.join(config.SCRIPT_DIR, "achievements.json")
        self.achievements = self._load_achievements()
        self._check_achievements()

    def _load_achievements(self):
        if os.path.exists(self.achievements_file):
            try:
                with open(self.achievements_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass
        return {}

    def _save_achievements(self):
        try:
            with open(self.achievements_file, "w", encoding="utf-8") as f:
                json.dump(self.achievements, f, ensure_ascii=False, indent=4)
        except OSError:
            pass

    # ==================================================================
    #  FELOLDÁS
    # ==================================================================
    def unlock_achievement(self, key):
        """Achievement feloldása + toast értesítés."""
        if key in self.achievements:
            return False
        if key not in ACHIEVEMENTS:
            return False

        ach = ACHIEVEMENTS[key]
        icon = ach["icon"]
        name = self.tr(ach["name_key"])
        desc = self.tr(ach["desc_key"])

        self.achievements[key] = {
            "unlocked_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        self._save_achievements()

        # Toast
        try:
            self.notify(
                self.tr("ach_unlocked_toast", icon=icon, name=name),
                "success", 4000
            )
        except Exception:
            pass

        # Log
        self.log_event("EVENT", self.tr("ach_unlocked_log", name=name, desc=desc))
        return True

    # ==================================================================
    #  AUTOMATIKUS ELLENŐRZÉS
    # ==================================================================
    def _check_achievements(self):
        try:
            # Bot alapú achievement-ek
            if self.bots:
                self.unlock_achievement("first_start")
                n = len(self.bots)
                if n >= 3:
                    self.unlock_achievement("three_bots")
                if n >= 5:
                    self.unlock_achievement("five_bots")
                if n >= 10:
                    self.unlock_achievement("ten_bots")

                # Uptime achievement-ek
                for bot in self.bots.values():
                    weekly = bot.get("weekly_uptime_seconds", 0)
                    if weekly >= 3600:
                        self.unlock_achievement("uptime_1h")
                    if weekly >= 36000:
                        self.unlock_achievement("uptime_10h")
                    if weekly >= 360000:
                        self.unlock_achievement("uptime_100h")

            # Backup achievement-ek
            backup_dir = config.BACKUP_DIR
            if os.path.isdir(backup_dir):
                zips = [f for f in os.listdir(backup_dir) if f.endswith(".zip")]
                if zips:
                    self.unlock_achievement("first_backup")
                if len(zips) >= 10:
                    self.unlock_achievement("ten_backups")

            # Plugin achievement
            if os.path.isdir(config.PLUGINS_DIR):
                plugins = [f for f in os.listdir(config.PLUGINS_DIR)
                           if f.endswith(".py") and not f.startswith("_")]
                if plugins:
                    self.unlock_achievement("first_plugin")

            # Emoji / szín achievement
            for bot in self.bots.values():
                if (bot.get("emoji", "🤖") != "🤖" or
                        bot.get("color", "#5865F2") != "#5865F2"):
                    self.unlock_achievement("appearance_user")
                    break
        except Exception:
            pass

        try:
            self.after(60000, self._check_achievements)
        except Exception:
            pass

    # ==================================================================
    #  ABLAK
    # ==================================================================
    def open_achievements_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("achievements_title"))
        win.geometry("780x680")
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 780) // 2
        y = (win.winfo_screenheight() - 680) // 2
        win.geometry(f"780x680+{x}+{y}")

        unlocked = len(self.achievements)
        total = len(ACHIEVEMENTS)

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#f39c12", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_text = self.tr(
            "achievements_header_text",
            unlocked=unlocked, total=total
        )
        ctk.CTkLabel(
            header,
            text=header_text,
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(side="left", padx=20, pady=16)

        progress = ctk.CTkProgressBar(header, width=200)
        progress.pack(side="right", padx=20, pady=28)
        progress.set(unlocked / total if total > 0 else 0)

        # --- Lista ---
        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=12, pady=12)

        for key, ach in ACHIEVEMENTS.items():
            icon = ach["icon"]
            name = self.tr(ach["name_key"])
            desc = self.tr(ach["desc_key"])
            is_unlocked = key in self.achievements

            bg = "#1f2f1f" if is_unlocked else "#1e2129"
            border = "#2ecc71" if is_unlocked else "#2f3542"

            card = ctk.CTkFrame(
                scroll,
                fg_color=bg,
                corner_radius=10,
                border_width=1,
                border_color=border,
            )
            card.pack(fill="x", padx=4, pady=4)

            # Ikon vagy lakat
            ctk.CTkLabel(
                card,
                text=icon if is_unlocked else "🔒",
                font=("Arial", 26),
            ).pack(side="left", padx=14, pady=10)

            # Szövegek
            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True, padx=6, pady=8)

            ctk.CTkLabel(
                text_frame,
                text=name,
                font=("Arial", 13, "bold"),
                text_color="#2ecc71" if is_unlocked else "#aaa",
                anchor="w",
            ).pack(fill="x")

            ctk.CTkLabel(
                text_frame,
                text=desc,
                font=("Arial", 10),
                text_color="#888",
                anchor="w",
            ).pack(fill="x")

            # Feloldás dátuma
            if is_unlocked:
                when = self.achievements[key].get("unlocked_at", "")
                ctk.CTkLabel(
                    card,
                    text=f"✅ {when}",
                    font=("Arial", 9),
                    text_color="#2ecc71",
                ).pack(side="right", padx=14)

        ctk.CTkButton(
            win,
            text=self.tr("close_btn"),
            fg_color="#555555",
            width=120,
            command=win.destroy,
        ).pack(pady=(0, 12))