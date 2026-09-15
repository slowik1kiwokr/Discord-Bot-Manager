import os
import json
import time

import customtkinter as ctk
import psutil


# (name_key, icon, desc_key) — a szövegek a languages.py-ból jönnek
WIDGET_CATALOG = {
    "uptime":        ("widget_uptime_name",        "⏱️", "widget_uptime_desc"),
    "cpu":           ("widget_cpu_name",           "💻", "widget_cpu_desc"),
    "ram":           ("widget_ram_name",           "💾", "widget_ram_desc"),
    "active_bots":   ("widget_active_bots_name",   "🟢", "widget_active_bots_desc"),
    "total_bots":    ("widget_total_bots_name",    "🤖", "widget_total_bots_desc"),
    "error_count":   ("widget_error_count_name",   "⚠️", "widget_error_count_desc"),
    "commands":      ("widget_commands_name",      "⚡", "widget_commands_desc"),
    "temperature":   ("widget_temperature_name",   "🌡️", "widget_temperature_desc"),
    "server_count":  ("widget_server_count_name",  "🌐", "widget_server_count_desc"),
    "user_count":    ("widget_user_count_name",    "👥", "widget_user_count_desc"),
    "recent_logs":   ("widget_recent_logs_name",   "📝", "widget_recent_logs_desc"),
}


class DashboardWidgetsMixin:
    """Testreszabható dashboard widgetekkel."""

    def _default_dashboard_layout(self):
        return [
            {"id": "uptime",       "visible": True},
            {"id": "cpu",          "visible": True},
            {"id": "ram",          "visible": True},
            {"id": "active_bots",  "visible": True},
            {"id": "error_count",  "visible": True},
            {"id": "commands",     "visible": True},
        ]

    def init_dashboard_widgets(self):
        if not hasattr(self, "dashboard_layout") or not self.dashboard_layout:
            self.dashboard_layout = self._default_dashboard_layout()

    def open_dashboard_window(self):
        if not getattr(self, "dashboard_layout", None):
            self.dashboard_layout = self._default_dashboard_layout()

        win = ctk.CTkToplevel(self)
        win.title(self.tr("dashboard_title"))
        win.geometry("1000x680")
        win.minsize(700, 500)
        win.grab_set()
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 1000) // 2
        y = (win.winfo_screenheight() - 680) // 2
        win.geometry(f"1000x680+{x}+{y}")

        header = ctk.CTkFrame(win, fg_color="#5865F2", corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=self.tr("dashboard_header"),
                     font=("Arial", 17, "bold"), text_color="white").pack(side="left", padx=20, pady=14)

        container = ctk.CTkScrollableFrame(win, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkButton(header, text=self.tr("dashboard_widgets_btn"), fg_color="#2c3e50",
                      hover_color="#34495e", width=120,
                      command=lambda: self._open_widget_manager(win, container)
                      ).pack(side="right", padx=8, pady=14)
        ctk.CTkButton(header, text=self.tr("dashboard_refresh_btn"), fg_color="#27ae60",
                      hover_color="#2ecc71", width=110,
                      command=lambda: self._render_dashboard(container)
                      ).pack(side="right", padx=8, pady=14)

        self._render_dashboard(container)

    def _render_dashboard(self, container):
        for child in container.winfo_children():
            child.destroy()

        visible = [w for w in self.dashboard_layout if w.get("visible", True)]
        if not visible:
            ctk.CTkLabel(container,
                         text=self.tr("dashboard_no_widgets"),
                         font=("Arial", 14), text_color="#888").pack(pady=60)
            return

        row, col = 0, 0
        for conf in visible:
            w_id = conf.get("id")
            if w_id not in WIDGET_CATALOG:
                continue
            name_key, icon, desc_key = WIDGET_CATALOG[w_id]
            name = self.tr(name_key)
            desc = self.tr(desc_key)
            card = self._build_widget_card(container, w_id, name, icon, desc)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            col += 1
            if col >= 3:
                col = 0
                row += 1

        for i in range(3):
            container.grid_columnconfigure(i, weight=1)

    def _build_widget_card(self, parent, w_id, name, icon, desc):
        card = ctk.CTkFrame(parent, fg_color="#1e2129", corner_radius=10,
                            border_width=1, border_color="#2f3542",
                            width=280, height=140)
        card.grid_propagate(False)

        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(head, text=f"{icon}  {name}",
                     font=("Arial", 12, "bold"), text_color="#aaa").pack(side="left")

        value_label = ctk.CTkLabel(card, text="...",
                                    font=("Arial", 26, "bold"),
                                    text_color="#5865F2")
        value_label.pack(pady=6)

        ctk.CTkLabel(card, text=desc, font=("Arial", 9),
                     text_color="#666").pack(pady=(0, 10))

        self._update_widget_value(value_label, w_id)
        return card

    def _update_widget_value(self, label, w_id):
        try:
            if not label.winfo_exists():
                return
        except Exception:
            return

        try:
            bot = self.bots.get(self.active_bot_key, {})

            if w_id == "uptime":
                if bot.get("is_running") and bot.get("start_time"):
                    sec = int(time.time() - bot["start_time"])
                    h, rem = divmod(sec, 3600)
                    m, s = divmod(rem, 60)
                    label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
                else:
                    label.configure(text="—")

            elif w_id == "cpu":
                cpu = psutil.cpu_percent(interval=None)
                label.configure(text=f"{cpu:.1f}%",
                                text_color="#2ecc71" if cpu < 50 else
                                           "#f39c12" if cpu < 80 else "#e74c3c")

            elif w_id == "ram":
                ram = psutil.virtual_memory().percent
                label.configure(text=f"{ram:.1f}%",
                                text_color="#2ecc71" if ram < 60 else
                                           "#f39c12" if ram < 85 else "#e74c3c")

            elif w_id == "active_bots":
                running = sum(1 for b in self.bots.values() if b.get("is_running"))
                label.configure(text=f"{running} / {len(self.bots)}")

            elif w_id == "total_bots":
                label.configure(text=str(len(self.bots)))

            elif w_id == "error_count":
                total = sum(b.get("error_count", 0) for b in self.bots.values())
                label.configure(text=str(total),
                                text_color="#e74c3c" if total > 0 else "#2ecc71")

            elif w_id == "commands":
                total = sum(b.get("total_commands", 0) for b in self.bots.values())
                label.configure(text=str(total))

            elif w_id == "temperature":
                label.configure(text=self.get_temperature_text())

            elif w_id == "server_count":
                script_path = bot.get("path", "")
                if script_path:
                    stats_file = os.path.join(os.path.dirname(script_path), "bot_stats.json")
                    if os.path.exists(stats_file):
                        with open(stats_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        label.configure(text=str(data.get("guilds", 0)))
                    else:
                        label.configure(text="0")
                else:
                    label.configure(text="—")

            elif w_id == "user_count":
                script_path = bot.get("path", "")
                if script_path:
                    stats_file = os.path.join(os.path.dirname(script_path), "bot_stats.json")
                    if os.path.exists(stats_file):
                        with open(stats_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        label.configure(text=str(data.get("users", 0)))
                    else:
                        label.configure(text="0")
                else:
                    label.configure(text="—")

            elif w_id == "recent_logs":
                logs = bot.get("raw_logs", [])[-5:]
                label.configure(text=self.tr("dashboard_recent_logs_count", count=len(logs)),
                                font=("Arial", 18))

        except Exception:
            pass

        try:
            label.after(1500, lambda: self._update_widget_value(label, w_id))
        except Exception:
            pass

    def _open_widget_manager(self, parent_win, container):
        mgr = ctk.CTkToplevel(parent_win)
        mgr.title(self.tr("dashboard_manager_title"))
        mgr.geometry("500x600")
        mgr.grab_set()
        mgr.update_idletasks()
        x = (mgr.winfo_screenwidth() - 500) // 2
        y = (mgr.winfo_screenheight() - 600) // 2
        mgr.geometry(f"500x600+{x}+{y}")

        ctk.CTkLabel(mgr, text=self.tr("dashboard_manager_header"),
                     font=("Arial", 16, "bold")).pack(pady=(14, 4))
        ctk.CTkLabel(mgr, text=self.tr("dashboard_manager_hint"),
                     font=("Arial", 11), text_color="#888").pack(pady=(0, 10))

        list_frame = ctk.CTkScrollableFrame(mgr)
        list_frame.pack(fill="both", expand=True, padx=14, pady=6)

        visible_ids = {w["id"] for w in self.dashboard_layout if w.get("visible", True)}
        vars_map = {}

        for w_id, (name_key, icon, desc_key) in WIDGET_CATALOG.items():
            row = ctk.CTkFrame(list_frame, fg_color="#1e2129", corner_radius=8)
            row.pack(fill="x", padx=4, pady=3)

            var = ctk.BooleanVar(value=w_id in visible_ids)
            vars_map[w_id] = var

            ctk.CTkCheckBox(row, text=f"{icon}  {self.tr(name_key)}",
                            variable=var, font=("Arial", 12, "bold")).pack(
                side="left", padx=12, pady=10)
            ctk.CTkLabel(row, text=self.tr(desc_key), font=("Arial", 9),
                         text_color="#888").pack(side="right", padx=12)

        def save_and_close():
            existing_ids = [w["id"] for w in self.dashboard_layout]
            new_layout = []
            for w_id in existing_ids:
                if w_id in vars_map:
                    conf = next((w for w in self.dashboard_layout if w["id"] == w_id), {})
                    conf["visible"] = vars_map[w_id].get()
                    new_layout.append(conf)
            for w_id, var in vars_map.items():
                if w_id not in existing_ids and var.get():
                    new_layout.append({"id": w_id, "visible": True})

            self.dashboard_layout = new_layout
            self.save_config()
            self._render_dashboard(container)
            mgr.destroy()

        ctk.CTkButton(mgr, text=self.tr("dashboard_save_btn"), fg_color="#27ae60",
                      hover_color="#2ecc71", height=40,
                      command=save_and_close).pack(pady=12, padx=14, fill="x")