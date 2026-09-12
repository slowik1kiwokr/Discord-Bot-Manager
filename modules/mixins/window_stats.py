import os
import re
import json
import time
import datetime
from collections import Counter
from tkinter import filedialog, messagebox

import customtkinter as ctk
import psutil

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    MATPLOTLIB_ERROR = "A matplotlib csomag nem tölthető be."

import modules.config as config
from modules.languages import LANGUAGES


class WindowStatsMixin:
    def open_global_stats_window(self):
        win = ctk.CTkToplevel(self)
        win.title(self.tr("global_stats_title"))
        win.geometry("950x650")
        win.grab_set()
        tabs = ctk.CTkTabview(win)
        tabs.pack(fill="both", expand=True, padx=12, pady=12)
        overview_tab = tabs.add(self.tr("global_stats"))
        commands_tab = tabs.add(self.tr("command_stats"))
        ctk.CTkLabel(overview_tab, text=self.tr("global_stats_title"), font=("Arial", 18, "bold"), text_color="#3498db").pack(pady=15)
        scroll_frame = ctk.CTkScrollableFrame(overview_tab)
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        for k, bot in self.bots.items():
            card = ctk.CTkFrame(scroll_frame, fg_color=self.theme_colors["card_bg"])
            card.pack(fill="x", padx=5, pady=4)
            status_text = self.tr("online") if bot["is_running"] else self.tr("offline")
            ctk.CTkLabel(card, text=f"🤖 {k} | {status_text} | {self.tr('total_commands')}: {bot['total_commands']} | {self.tr('errors')}: {bot['error_count']}", font=("Consolas", 12), text_color=self.theme_colors["text"]).pack(anchor="w", padx=10, pady=10)

        daily, popular = self.get_command_usage_stats()
        ctk.CTkLabel(commands_tab, text=self.tr("daily_commands"), font=("Arial", 14, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        daily_box = ctk.CTkTextbox(commands_tab, height=170)
        daily_box.pack(fill="x", padx=12, pady=5)
        daily_lines = ["%s: %s" % (day, count) for day, count in sorted(daily.items())]
        daily_box.insert("1.0", "\n".join(daily_lines) or self.tr("no_command_data"))
        daily_box.configure(state="disabled")
        ctk.CTkLabel(commands_tab, text=self.tr("popular_commands"), font=("Arial", 14, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
        popular_box = ctk.CTkTextbox(commands_tab, height=170)
        popular_box.pack(fill="both", expand=True, padx=12, pady=5)
        popular_lines = ["%s: %s" % (command, count) for command, count in popular.most_common()]
        popular_box.insert("1.0", "\n".join(popular_lines) or self.tr("no_command_data"))
        popular_box.configure(state="disabled")

    def get_command_usage_stats(self):
        daily = {}
        popular = {}
        for bot in self.bots.values():
            for entry in bot.get("raw_logs", []):
                message = entry.get("msg", "")
                lowered = message.lower()
                if "command" not in lowered and "parancs" not in lowered and not re.search(r"(?:^|\s)/[a-zA-Z0-9_-]+", message):
                    continue
                date_key = entry.get("date", datetime.datetime.now().strftime("%Y-%m-%d"))
                daily[date_key] = daily.get(date_key, 0) + 1
                match = re.search(r"(?:command|parancs)\s*[:=]?\s*([/a-zA-Z0-9_-]+)", message, re.IGNORECASE)
                command_name = match.group(1) if match else (re.search(r"(/[a-zA-Z0-9_-]+)", message).group(1) if re.search(r"(/[a-zA-Z0-9_-]+)", message) else "unknown")
                popular[command_name] = popular.get(command_name, 0) + 1
        from collections import Counter
        return daily, Counter(popular)

    def update_stats_loop(self):
        bot = self.bots.get(self.active_bot_key)
        self.lbl_temperature.configure(text=self.get_temperature_text())
        if bot and bot["is_running"] and bot["process"] and bot["start_time"]:
            elapsed = int(time.time() - bot["start_time"])
            self.lbl_uptime.configure(text=str(datetime.timedelta(seconds=elapsed)))

            self.check_auto_restarts()

            bot["weekly_uptime_seconds"] += 1
            w_hours = bot["weekly_uptime_seconds"] // 3600
            w_mins = (bot["weekly_uptime_seconds"] % 3600) // 60
            self.lbl_weekly_uptime.configure(text=f"{w_hours}h {w_mins}m")

            try:
                proc = psutil.Process(bot["process"].pid)
                self.lbl_ram.configure(text=f"{proc.memory_info().rss / (1024 * 1024):.1f} MB")
                self.lbl_cpu.configure(text=f"{proc.cpu_percent(interval=None):.1f} %")
            except Exception:
                pass

            script_path = bot.get("path", "")
            if script_path and os.path.exists(script_path):
                stats_file = os.path.join(os.path.dirname(script_path), "bot_stats.json")
                if os.path.exists(stats_file):
                    try:
                        with open(stats_file, "r", encoding="utf-8") as f:
                            stats = json.load(f)
                            self.lbl_servers.configure(text=str(stats.get("guilds", 0)))
                            self.lbl_users.configure(text=str(stats.get("users", 0)))
                            api_p = stats.get("api_ping", stats.get("ping", 0))
                            msg_p = stats.get("msg_ping", stats.get("message_ping", 0))
                            self.lbl_api_ping.configure(text=f"API: {api_p}ms")
                            self.lbl_msg_ping.configure(text=f"Msg: {msg_p}ms")
                    except Exception:
                        pass
        self.after(1000, self.update_stats_loop)