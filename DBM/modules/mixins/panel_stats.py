import os
import json
import time
import datetime
import functools

import customtkinter as ctk

import modules.config as config


# Feature ID → nyelvi kulcs a megjelenített névhez
FEATURE_NAME_KEYS = {
    "open_settings_window_v2": "feat_settings",
    "open_backup_manager": "feat_backup",
    "open_sqlite_viewer": "feat_sqlite",
    "open_broadcast_window": "feat_broadcast",
    "open_commander_window": "feat_commander",
    "open_plugins_window": "feat_plugins",
    "open_servers_window": "feat_servers",
    "open_global_stats_window": "feat_global_stats",
    "open_monthly_report_window": "feat_monthly_report",
    "open_tutorial_window": "feat_tutorial",
    "open_alapok_window": "feat_basics",
    "open_bot_info_editor": "feat_bot_info",
    "open_activity_editor": "feat_activity",
    "open_performance_charts_window": "feat_perf_charts",
    "open_bot_appearance_editor": "feat_appearance",
    "open_animated_charts_window": "feat_animated_charts",
    "open_dashboard_window": "feat_dashboard",
}


class PanelStatsMixin:
    """Panel használati statisztikák követése és megjelenítése."""

    def init_panel_stats(self):
        self.stats_file = os.path.join(config.SCRIPT_DIR, "panel_stats.json")
        self.stats_data = self._load_panel_stats()
        self.session_start = time.time()

        self.stats_data["opens"] = self.stats_data.get("opens", 0) + 1
        self.stats_data["last_opened"] = datetime.datetime.now().isoformat(timespec="seconds")
        if "first_opened" not in self.stats_data:
            self.stats_data["first_opened"] = datetime.datetime.now().isoformat(timespec="seconds")
        if "feature_usage" not in self.stats_data:
            self.stats_data["feature_usage"] = {}
        if "total_seconds" not in self.stats_data:
            self.stats_data["total_seconds"] = 0

        self._stats_save_counter = 0
        self._save_panel_stats()
        self._wrap_for_tracking()
        self._stats_tick()

    def _stats_tick(self):
        try:
            if self.winfo_exists() and self.state() != "iconic":
                self.stats_data["total_seconds"] = self.stats_data.get("total_seconds", 0) + 5
                self._stats_save_counter = getattr(self, "_stats_save_counter", 0) + 1
                if self._stats_save_counter >= 12:  # 1 percenként
                    self._stats_save_counter = 0
                    self._save_panel_stats()
        except Exception:
            pass
        try:
            self.after(5000, self._stats_tick)
        except Exception:
            pass

    def _load_panel_stats(self):
        if not os.path.exists(self.stats_file):
            return {}
        try:
            with open(self.stats_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {}

    def _save_panel_stats(self):
        try:
            with open(self.stats_file, "w", encoding="utf-8") as f:
                json.dump(self.stats_data, f, ensure_ascii=False, indent=4)
        except OSError:
            pass

    def save_stats_on_exit(self):
        self._save_panel_stats()

    def _wrap_for_tracking(self):
        features = [
            "open_settings_window_v2", "open_backup_manager", "open_sqlite_viewer",
            "open_broadcast_window", "open_commander_window", "open_plugins_window",
            "open_servers_window", "open_global_stats_window", "open_monthly_report_window",
            "open_tutorial_window", "open_alapok_window", "open_bot_info_editor",
            "open_activity_editor", "open_performance_charts_window",
            "open_bot_appearance_editor", "open_animated_charts_window",
            "open_dashboard_window",
        ]

        for name in features:
            if not hasattr(self, name):
                continue
            original = getattr(self, name)

            def make_wrapper(orig, fname):
                @functools.wraps(orig)
                def wrapper(*args, **kwargs):
                    self._track_feature(fname)
                    return orig(*args, **kwargs)
                return wrapper

            setattr(self, name, make_wrapper(original, name))

    def _track_feature(self, feature):
        try:
            usage = self.stats_data.setdefault("feature_usage", {})
            usage[feature] = usage.get(feature, 0) + 1
        except Exception:
            pass

    # ------------------------------------------------------------------
    #  Statisztika ablak
    # ------------------------------------------------------------------
    def open_panel_stats_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("pstats_title"))
        win.geometry("820x680")
        win.minsize(700, 500)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 820) // 2
        y = (win.winfo_screenheight() - 680) // 2
        win.geometry(f"820x680+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#8e44ad", corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=self.tr("pstats_header"),
                     font=("Arial", 18, "bold"), text_color="white").pack(pady=18)

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=14)

        ctk.CTkLabel(scroll, text=self.tr("pstats_overview"),
                     font=("Arial", 14, "bold"), anchor="w").pack(fill="x", pady=(0, 8))

        cards_row = ctk.CTkFrame(scroll, fg_color="transparent")
        cards_row.pack(fill="x", pady=(0, 16))

        def make_card(parent, icon, title, value, color):
            c = ctk.CTkFrame(parent, fg_color="#1e2129", corner_radius=10,
                             border_width=1, border_color="#2f3542")
            c.pack(side="left", fill="both", expand=True, padx=4)
            ctk.CTkLabel(c, text=f"{icon}  {title}",
                         font=("Arial", 10, "bold"), text_color="#888").pack(pady=(12, 4))
            ctk.CTkLabel(c, text=str(value),
                         font=("Arial", 20, "bold"), text_color=color).pack(pady=(0, 12))

        def fmt_time(sec):
            h = sec // 3600
            m = (sec % 3600) // 60
            return self.tr("pstats_time_format", hours=h, minutes=m)

        opens = self.stats_data.get("opens", 0)
        total_sec = self.stats_data.get("total_seconds", 0)
        session_sec = int(time.time() - self.session_start)

        make_card(cards_row, "🚀", self.tr("pstats_card_opens"), opens, "#2ecc71")
        make_card(cards_row, "⏱️", self.tr("pstats_card_total"), fmt_time(total_sec), "#3498db")
        make_card(cards_row, "⚡", self.tr("pstats_card_session"), fmt_time(session_sec), "#f39c12")

        ctk.CTkLabel(scroll, text=self.tr("pstats_dates_section"),
                     font=("Arial", 14, "bold"), anchor="w").pack(fill="x", pady=(8, 8))

        info_card = ctk.CTkFrame(scroll, fg_color="#1e2129", corner_radius=10)
        info_card.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(info_card,
                     text=self.tr("pstats_first_opened",
                                  value=self.stats_data.get("first_opened", "—")),
                     font=("Consolas", 11), anchor="w").pack(fill="x", padx=16, pady=(10, 4))
        ctk.CTkLabel(info_card,
                     text=self.tr("pstats_last_opened",
                                  value=self.stats_data.get("last_opened", "—")),
                     font=("Consolas", 11), anchor="w").pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkLabel(scroll, text=self.tr("pstats_top_features"),
                     font=("Arial", 14, "bold"), anchor="w").pack(fill="x", pady=(8, 8))

        feature_usage = self.stats_data.get("feature_usage", {})
        if not feature_usage:
            ctk.CTkLabel(scroll, text=self.tr("pstats_no_data"),
                         font=("Arial", 11), text_color="#666").pack(pady=10)
        else:
            sorted_features = sorted(feature_usage.items(), key=lambda x: x[1], reverse=True)
            max_count = sorted_features[0][1] if sorted_features else 1

            for feat_id, count in sorted_features:
                name_key = FEATURE_NAME_KEYS.get(feat_id)
                display_name = self.tr(name_key) if name_key else feat_id

                row = ctk.CTkFrame(scroll, fg_color="#1e2129", corner_radius=8)
                row.pack(fill="x", pady=3)

                ctk.CTkLabel(row, text=display_name,
                             font=("Arial", 12), anchor="w", width=200).pack(side="left", padx=12, pady=10)

                bar_width = int((count / max_count) * 300)
                bar = ctk.CTkFrame(row, height=18, width=max(bar_width, 4),
                                   fg_color="#5865F2", corner_radius=4)
                bar.pack(side="left", padx=8)
                bar.pack_propagate(False)

                ctk.CTkLabel(row, text=f"{count}x",
                             font=("Consolas", 11, "bold"),
                             text_color="#2ecc71").pack(side="left", padx=10)

        btns = ctk.CTkFrame(win, fg_color="transparent")
        btns.pack(fill="x", padx=16, pady=10)

        def reset_stats():
            from tkinter import messagebox
            if not messagebox.askyesno(self.tr("pstats_reset_title"),
                                       self.tr("pstats_reset_confirm"),
                                       parent=win):
                return
            self.stats_data = {
                "opens": 0, "total_seconds": 0,
                "first_opened": datetime.datetime.now().isoformat(timespec="seconds"),
                "feature_usage": {},
            }
            self._save_panel_stats()
            win.destroy()
            self.open_panel_stats_window()

        ctk.CTkButton(btns, text=self.tr("pstats_save_btn"),
                      fg_color="#27ae60", hover_color="#2ecc71", width=160,
                      command=lambda: (self._save_panel_stats(),
                                       self.notify(self.tr("pstats_saved"), "success", 1500))
                      ).pack(side="left", padx=4)

        ctk.CTkButton(btns, text=self.tr("pstats_reset_btn"),
                      fg_color="#c0392b", hover_color="#e74c3c", width=180,
                      command=reset_stats).pack(side="left", padx=4)

        ctk.CTkButton(btns, text=self.tr("common_close_btn"),
                      fg_color="#555555", hover_color="#666666",
                      width=100, command=win.destroy).pack(side="right", padx=4)